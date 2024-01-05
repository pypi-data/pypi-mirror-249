from copy import deepcopy
from dataclasses import dataclass
from typing import Callable, List, Union

import PIL.Image  # import PIL.Image as Image doesn't work on my end for some reason
import cv2 as cv
import numpy as np
import torch
from torch import nn

from explainer.models import VisionModel, XAI_Result
from explainer.models._api import get_model
from explainer.parts_extraction.grabcut import Grabcut
from explainer.parts_extraction.graph_partition import get_partition_method
from explainer.parts_extraction.relevancies import compute_relevances
from explainer.parts_extraction.segmentation import (
    SegmentationWrapper,
    get_segmentation_method,
)
from explainer.util.return_types import ExplanationMap, Object, Part, Result

LAST_SEGMENTATION = None


class Extractor(nn.Module):
    def __init__(
        self,
        segmentation_method: Union[str, SegmentationWrapper],
        merge_method: str,
        parts_model: Union[str, VisionModel],
        use_grabcut: bool = True,
        discard_threshold: float = 0.25,
        overlap_ratio: float = 0.9,  # 0.75,
    ):
        super().__init__()

        if isinstance(segmentation_method, str):
            self.segmentation_method: SegmentationWrapper = get_segmentation_method(
                segmentation_method
            )
        else:
            # this can be useful if initialization is expensive and there is centralized caching
            assert isinstance(segmentation_method, SegmentationWrapper), (
                f"Expected segmentation_method to be of type SegmentationWrapper, "
                f"but got {type(segmentation_method)}"
            )
            self.segmentation_method = segmentation_method

        if use_grabcut:
            self.segmentation_method = Grabcut(self.segmentation_method)

        self.graph_merge: Callable = get_partition_method(merge_method)

        if isinstance(parts_model, str):
            self.parts_model: VisionModel = get_model(parts_model)
        else:
            # again, this can be useful if initialization is expensive and there is centralized caching
            assert isinstance(parts_model, VisionModel), (
                f"Expected parts_model to be of type VisionModel, "
                f"but got {type(parts_model)}"
            )
            self.parts_model = parts_model

        self.discard_threshold = discard_threshold
        self.overlap_ratio = overlap_ratio

    def forward(self, explainedInput: XAI_Result) -> Result:  # noqa: F405
        orig_img = explainedInput.original_image
        img = np.array(orig_img)
        objects = []

        for label_idx, xai_maps in explainedInput.group_py_label(
            resize_to_original_size=True
        ).items():
            try:
                segmentation = self.segmentation_method(
                    img, xai_maps
                )  # type: np.ndarray

            except torch.cuda.OutOfMemoryError:
                print("Out of memory error during segmentation")
                orig_device = self.parts_model.device
                self.parts_model = self.parts_model.cpu()
                torch.cuda.empty_cache()

                try:
                    print("Trying again after moving parts model to cpu")
                    segmentation = self.segmentation_method(img, xai_maps)
                except torch.cuda.OutOfMemoryError:
                    print("Out of memory error during segmentation")
                    print("Falling back to Slic-Segmentation")
                    segmentation = get_segmentation_method("slic")(img, xai_maps)
                finally:
                    self.parts_model = self.parts_model.to(orig_device)

            # TODO REMOVE
            global LAST_SEGMENTATION
            LAST_SEGMENTATION = deepcopy(segmentation)

            # TODO: if there is a segmentationmap (LIME), use this segmentation. Possibly in SegmenatationWrapper?

            weights = {segment_id: 0 for segment_id in np.unique(segmentation)}

            for xai_map in xai_maps:
                weighted_segments = compute_relevances(xai_map, segmentation)

                for segment_id in weighted_segments:
                    weights[segment_id] += weighted_segments[segment_id] / len(xai_maps)

                del weighted_segments

            # TODO: merge heatmaps, could also be computed after merging segmentation - check if this is better
            merged_heatmap = np.zeros(segmentation.shape)
            for segment_id in weights:
                merged_heatmap[segmentation == segment_id] = weights[segment_id]

            # TODO: Maybe prefer bigger segments over smaller ones (?) @Raphael. (e.g. multiply heatmap with segment size or something like that)

            merged_heatmap /= (
                merged_heatmap.sum()
            )  # normalize heatmap to sum to 1.0 (like a probability distribution)

            # discard segments with low relevance (i.e. set their pixels to 0)
            min_weight, max_weight = min(weights.values()), max(weights.values())
            range_weight = max_weight - min_weight
            theta = (
                min_weight + self.discard_threshold * range_weight
            )  # Threshold for discarding

            for segment_id in list(weights.keys()):
                if weights[segment_id] < theta:
                    segmentation[segmentation == segment_id] = 0  # set to background
                    del weights[segment_id]

            segmentation, weights = self._merge_segments(segmentation, weights)

            # extract_parts
            extracted_parts = self._extract(
                segmentation, img, weights, sum(weights.values())
            )

            # partsmodel
            parts = self._process_parts(extracted_parts)

            objects.append(
                Object(  # noqa: F405
                    merged_heatmap,
                    [
                        ExplanationMap(xai_map.map, xai_map.method.name)  # noqa: F405
                        for xai_map in xai_maps
                    ],
                    label_idx,
                    parts,
                )
            )

        return Result(orig_img, objects)  # noqa: F405

    def _merge_segments(self, segmentation: np.ndarray, weights) -> np.ndarray:
        """
        Merges neighboring segments.

        Parameters
        ----------
        segmentation : np.ndarray
            Segmentation to be filtered. Must be a 2D array of integers. Non-relevant segments must be set to 0.
        weights : dict
            Assigns a weight/relevance to each segment

        Returns
        -------
        np.ndarray
            Filtered segmentation.
        dict
            Weights for the filtered segmentation

        """

        relevant_segments = np.unique(segmentation)
        relevant_segments = sorted(relevant_segments)
        relevant_segments = [
            x for x in relevant_segments if x != 0
        ]  # remove background (0 values)
        segment_id_map = {
            segment_id: relevant_segments.index(segment_id)
            for segment_id in relevant_segments
        }

        adj_matrix = self._construct_neighbour_graph(
            segmentation, len(relevant_segments), segment_id_map
        )

        n_clusters, clustering = self.graph_merge(adj_matrix)

        merged_mapping = {}

        new_weights = {}

        for i in range(n_clusters):
            s_id = -1
            for s in relevant_segments:
                if clustering[segment_id_map[s]] == i:
                    if s_id < 0:
                        s_id = s
                        new_weights[s_id] = weights[s]
                    else:
                        new_weights[s_id] += weights[s]
                    merged_mapping[s] = s_id

        segmentation = deepcopy(segmentation)
        for segment_id in relevant_segments:
            segmentation[segmentation == segment_id] = merged_mapping[segment_id]

        return segmentation, new_weights

    def _construct_neighbour_graph(
        self,
        segmentation: np.ndarray,
        n_segments: int,
        segment_id_map: dict,
    ) -> np.ndarray:
        """
        Creates the neighbor graph
        The neighbor graph is a weighted undirected graph. It has one node for each relevant segment. The weight of an edge between two segments corresponds to the mean relevance along the border between these segments.

        Parameters
        ----------
        segmentation : np.ndarray
            Segmentation. Must be a 2D array of integers.
        n_segments: int
            number of relevant segments
        segment_id_map: dict
            assigns each segment which appears in segmentation a new id.
            id for relevant segments is between 0 (inclusive) and n_segments (exclusive)

        Returns
        -------
        np.ndarray
            graph as adjacency matrix

        """

        _directions_4 = [
            (0, 1),
            (1, 0),
            (0, -1),
            (-1, 0),
        ]  # neighbors for deciding if a pixel is a border or not
        _directions_8 = [
            (0, 1),
            (1, 1),
            (1, 0),
            (1, -1),
            (0, -1),
            (-1, -1),
            (-1, 0),
            (-1, 1),
        ]  # neighbors for discovering new pixels

        discovered_segments = {
            segment_id: False for segment_id in range(0, n_segments)
        }  # stores for each relevant segment if it was discovered so that every segment is only counted once in n_discovered
        discovered_pixel = np.full(
            segmentation.shape, False
        )  # stores for each pixel if it was discovered so that every pixel is added at most once to the stack
        n_discovered = 0  # number of discovered segments
        border_length = np.zeros(
            (n_segments, n_segments)
        )  # stores the length of the border between every segment-pair.
        stack = [
            (0, 0)
        ]  # stack of all discovered pixels which were not yet visited. Starts at (0,0) which is guaranteed to be a border pixel
        discovered_pixel[(0, 0)] = True

        # coordinates for linear search
        i = -1  # i starts at -1 because loop increments coordinates first
        j = 0
        while (
            n_discovered < n_segments
        ):  # iterate until every segment was discovered...
            # if the stack is empty, use linear search to find the next undiscovered segment.
            # this search will only execute in edge-cases, if there is one segment fully enclosing one or more other segments
            while not stack:
                # increment i,j
                i += 1
                if i >= segmentation.shape[0]:
                    i = 0
                    j += 1
                    assert (
                        j <= segmentation.shape[1]
                    )  # j > segmentation.shape[1] means that the entire area was searched. If this is false, then there was a segment id which is not on the segmentation.

                s = segmentation[i][j]
                if (
                    s in segment_id_map and not discovered_segments[segment_id_map[s]]
                ):  # new segment discovered
                    stack.append((i, j))  # add this segment
                    discovered_pixel[(i, j)] = True
                    break

            while stack:  # expore segments until stack is empty
                current = stack.pop()
                s = segmentation[current]

                # see if this is a border pixel
                is_border = False
                for direction in _directions_4:
                    neighbor = (current[0] + direction[0], current[1] + direction[1])
                    if (
                        neighbor[0] < 0
                        or neighbor[1] < 0
                        or neighbor[0] >= segmentation.shape[0]
                        or neighbor[1]
                        >= segmentation.shape[1]  # is neighbor within bounds?
                        or segmentation[neighbor]
                        != s  # belongs neighbor to a different segment?
                    ):
                        is_border = True
                        break

                # only visit border pixels
                if is_border:
                    # add all neighbors to the stack
                    for direction in _directions_8:
                        neighbor = (
                            current[0] + direction[0],
                            current[1] + direction[1],
                        )

                        if (
                            neighbor[0] < 0
                            or neighbor[1] < 0
                            or neighbor[0] >= segmentation.shape[0]
                            or neighbor[1] >= segmentation.shape[1]
                        ):
                            continue  # skip out-of-bounds neighbors

                        # add all undiscovered neighbors to stack
                        if not discovered_pixel[neighbor]:
                            stack.append(neighbor)
                            discovered_pixel[neighbor] = True
                        # Note: we explore the borders of all segments, not only the relevant segments. This is to improve runtime. Exploring all segments means that we will only have to do a linear search if there is a segment which fully encloses one or more segments.

                    if s in segment_id_map:  # if this segment is relevant...
                        # count this segment if this is the first time encountering it
                        if not discovered_segments[segment_id_map[s]]:
                            discovered_segments[segment_id_map[s]] = True
                            n_discovered += 1
                        # if this segment is relevant, look for borders with other relevant segments
                        for direction in _directions_4:
                            neighbor = (
                                current[0] + direction[0],
                                current[1] + direction[1],
                            )
                            if (
                                neighbor[0] < 0
                                or neighbor[1] < 0
                                or neighbor[0] >= segmentation.shape[0]
                                or neighbor[1] >= segmentation.shape[1]
                            ):
                                continue  # skip out-of-bounds neighbors

                            # increase edge-weight if neighbor belongs to different segment
                            s_n = segmentation[neighbor]
                            if s_n != s and s_n in segment_id_map:
                                s_id = segment_id_map[s]
                                s_n_id = segment_id_map[s_n]
                                border_length[(s_id, s_n_id)] += 1
                                # enforce symatrical matrix
                                border_length[(s_n_id, s_id)] += 1

        return border_length

    def _get_bounding_boxes(self, segmentation: np.ndarray, weights: dict):
        boxes = []

        for segment_id in np.unique(segmentation):
            if segment_id != 0:
                mask = (segmentation == segment_id).astype(np.uint8)  # shape: (H, W)
                weight = weights[segment_id]

                x, y, w, h = cv.boundingRect(
                    mask
                )  # x,y,w,h = cv.boundingRect(cnt), https://docs.opencv.org/3.4/dd/d49/tutorial_py_contour_features.html
                boxes.append(
                    self.ExtractedPart(x, y, x + w - 1, y + h - 1, [segment_id], weight)
                )

        return boxes

    def _extract_part(
        self, segmentation: np.ndarray, image: np.ndarray, part, relevance_sum
    ) -> np.ndarray:
        """
        Computes the part of a specified segment

        Parameters
        ----------
        segmentation : np.ndarray
            Segmentation to be processed. Must be a 2D array of integers.
        image : np.ndarray
            Image to be processed. Must be a 3D array of integers.
        part : Part
            Part to be cut
        relevance_sum: float
            Sum of the total relevance of the image

        Returns
        -------
        np.ndarray, float, (int,int,int,int)
            part as image, relevance, bounding rect
        """
        assert (
            segmentation.shape[0] == image.shape[0]
            and segmentation.shape[1] == image.shape[1]
        )

        in_segment = np.isin(segmentation, part.segment_ids)
        in_segment = in_segment.astype(np.uint8)
        rect = cv.boundingRect(in_segment)
        in_segment = cv.merge((in_segment, in_segment, in_segment))
        in_segment = in_segment.astype(bool)

        part_img = image[part.min[1] : part.max[1], part.min[0] : part.max[0]]
        in_segment = in_segment[part.min[1] : part.max[1], part.min[0] : part.max[0]]

        # fill = part_img
        # for _ in range(10):
        #    fill = cv.blur(fill, (5, 5))
        # fill = np.multiply(fill, np.invert(in_segment))
        part_img = np.multiply(part_img, in_segment)
        # part_img = part_img + fill

        return (part_img, part.relevance_sum / relevance_sum, rect)

    def _extract(
        self,
        segmentation: np.ndarray,
        image: np.ndarray,
        weights: dict,
        weight_sum: float,
    ) -> list[tuple]:
        """
        Computes all parts of a segmentation sorted by the heatmap

        Parameters
        ----------
        segmentation : np.ndarray
            Segmentation to be processed. Must be a 2D array of integers.
        image : np.ndarray
            Image to be processed. Must be a 2D array of integers with the same shape as segmentation
        weights : dict
            Assigns a weight/relevance to each segment
        weight_sum : float
            Sum of all weights, used for normilization

        Returns
        -------
        List[tuple]
            List of tuples containing the part, the relevance and the bounding box of the part. Sorted by relevance.
            The relevance is normalized akin to a probability distribution.
        """

        if (
            weight_sum == 0
        ):  # TODO: hotfix because some methods produce empty heatmaps, resulting in divion by zero.
            weight_sum = 1  # this should only happen when all the weights are zero

        parts = self._get_bounding_boxes(
            segmentation, weights
        )  # generate bounding boxes

        # eliminate overlapping parts
        running = True
        while running and len(parts) >= 2:
            best_i = parts[0]
            best_j = parts[1]
            best_score = best_i.merge_score(best_j)
            for i in parts:
                for j in parts:
                    if i != j:
                        s = i.merge_score(j)
                        if best_score < s:
                            best_score = s
                            best_i = i
                            best_j = j
            if best_score > self.overlap_ratio:
                best_i.merge(best_j)
                parts.remove(best_j)
            else:
                running = False

        # eliminate small parts
        min_area = 24**2
        min_side = 16
        for p in parts:
            if p.area() < min_area or p.shortest_side() < min_side:
                best_p2 = parts[0]
                best_score = best_p2.merge_score(p)
                for p2 in parts:
                    if p2 != p:
                        s = p2.merge_score(p)
                        if best_score < s:
                            best_score = s
                            best_p2 = p2
                if best_p2 != p and best_score > self.overlap_ratio / 2:
                    best_p2.merge(p)
                parts.remove(p)

        result = []

        # extract parts
        for p in parts:
            result.append(self._extract_part(segmentation, image, p, weight_sum))

        result = sorted(result, key=lambda x: x[1], reverse=True)
        return result

    def _process_parts(self, extracted_parts, **kwargs) -> List[Part]:  # noqa: F405
        """
        Outer loop for processing parts.

        Args:
            exctracted_parts (list): List of tuples (part_img, relevancy, bouning_rect).
            kwargs: Additional arguments.

        Returns:
            list: List of Part objects.
        """

        _parts_collector = []

        for i, (part_img, relevancy, rect) in enumerate(extracted_parts):
            part_img = PIL.Image.fromarray(part_img)

            part_labels = self.parts_model.predict(
                part_img,
                **kwargs,
            )

            _parts_collector.append(
                Part(  # noqa: F405
                    img=part_img,
                    relevancy=relevancy,
                    labels=part_labels,
                    rect=rect,
                )
            )

        return _parts_collector

    @dataclass
    class ExtractedPart:
        x_min: int
        y_min: int
        x_max: int
        y_max: int
        segment_ids: List[int]
        relevance_sum: float

        @property
        def min(self) -> (int, int):
            return (self.x_min, self.y_min)

        @min.setter
        def min(self, value: (int, int)) -> None:
            self.x_min, self.y_min = value

        @property
        def max(self) -> (int, int):
            return (self.x_max, self.y_max)

        @max.setter
        def max(self, value: (int, int)) -> None:
            self.x_max, self.y_max = value

        def __str__(self) -> str:
            return (
                f"(Temporary_Part Min:{self.min} Max:{self.max} IDs:{self.segment_ids})"
            )

        def overlap(self, other: "ExtractedPart") -> int:  # noqa: F405, F821
            intersection_min = (
                max(self.min[0], other.min[0]),
                max(self.min[1], other.min[1]),
            )
            intersection_max = (
                min(self.max[0], other.max[0]),
                min(self.max[1], other.max[1]),
            )
            return self._area(intersection_min, intersection_max)

        def merge_score(self, other: "ExtractedPart") -> float:  # noqa: F405, F821
            return self.overlap(other) / self.area()

        def area(self) -> int:
            return self._area(self.min, self.max)

        def shortest_side(self) -> int:
            return min(self.max[0] - self.min[0], self.max[1] - self.min[1]) + 1

        def _area(self, min_point: (int, int), max_point: (int, int)) -> int:
            dim = (max_point[0] - min_point[0] + 1, max_point[1] - min_point[1] + 1)
            if dim[0] >= 0 and dim[1] >= 0:
                return dim[0] * dim[1]
            else:
                return 0

        def merge(self, other: "ExtractedPart") -> None:  # noqa: F405, F821
            self.min = (min(self.min[0], other.min[0]), min(self.min[1], other.min[1]))
            self.max = (max(self.max[0], other.max[0]), max(self.max[1], other.max[1]))
            self.segment_ids += other.segment_ids
            self.relevance_sum += other.relevance_sum
