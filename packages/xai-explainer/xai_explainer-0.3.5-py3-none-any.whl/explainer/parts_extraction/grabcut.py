from typing import List

import cv2 as cv
import numpy as np
import torch.nn as nn

import explainer.models as _models
from explainer.parts_extraction.segmentation import SegmentationWrapper

_segmentation_allows_mask = {
    "slic": True,
    "quickshift": False,
    "watershed": True,
    "chan_vese": False,
    "segment_anything_base": False,
    "segment_anything_huge": False,
    "segment_anything_large": False,
}  # TODO: make this nicer


class Grabcut(nn.Module):
    def __init__(
        self,
        segmentation_method: SegmentationWrapper,
        thresh_bgd: float = 0.4,
        thresh_fgd: float = 0.6,
        threshold: bool = False,
        segmentation_config: dict = dict(),
    ):
        """
        Parameters
        ----------
        segmentation_method: SegmentationWrapper
            segmentation method to be used
        thresh_bgd : float, optional
            threshold or quantile below which a pixel will be seen as sure backgrund. Default = 0.4
        thresh_fgd : float, optional
            threshold or quantile above which a pixel will be seen as sure foreground. Default = 0.6
        threshold: bool, optional
            if true, thresh_bgd and thresh_fgd will be interpreted as thresholds. Otherwise, they will be interpreted as quantiles. Default = False
        segmentation_config:dict, optional
            kwargs for the segmentation. Default: empty
        """
        super().__init__()
        self.segmentation_method = segmentation_method
        self.thresh_bgd: float = thresh_bgd
        self.thresh_fgd: float = thresh_fgd
        self.threshold: bool = threshold
        self.segmentation_config = segmentation_config

        self.allows_mask = (
            _segmentation_allows_mask[segmentation_method]
            if segmentation_method in _segmentation_allows_mask
            else False
        )
        if self.allows_mask:
            self.segmentation_config["n_segments"] = 100

    def forward(self, img: np.ndarray, maps: List[_models.XAI_Map]):
        """
        Extracts foreground with grabcut and segments it.

        Parameters
        ----------
        img: np.ndarray
            The Image
        maps: List[_models.XAI_Map]
            List of heatmaps
        Returns
        -------
        np.ndarray
            Segmentation with background = 0
        """

        heatmap = self._merge_heatmaps(maps, img)
        relevant_area = self._get_relevant_area(img, heatmap)
        if self.allows_mask:
            segmentation = self.segmentation_method(
                img, mask=relevant_area, **self.segmentation_config
            )
        else:
            segmentation = self.segmentation_method(img, **self.segmentation_config)
            segmentation = np.multiply(segmentation, relevant_area)
        return segmentation

    def contour_map_to_heatmap(
        contour_map: np.ndarray, num_segments=1000
    ) -> np.ndarray:
        return contour_map  # TODO: actually convert contour_map to heatmap

    def _merge_heatmaps(
        self, img: np.ndarray, maps: List[_models.XAI_Map]
    ) -> np.ndarray:  # TODO: better ways to merge heatmaps
        """
        Merges a list of heatmaps by taking the mean in each pixel.

        Parameters
        ----------
        img: np.ndarray
            The Image
        maps: List[_models.XAI_Map]
            List of heatmaps
        Returns
        -------
        np.ndarray
            Merged heatmap
        """
        heatmap = np.zeros_like(maps[0].map)
        for m in maps:
            if m.method.method_type == _models.XAI_MethodType.EDGEMAP:
                heatmap += self.contour_map_to_heatmap(m.map)
            else:
                heatmap += m.map
        heatmap /= len(maps)
        return heatmap

    def _get_relevant_area(self, img: np.ndarray, heatmap: np.ndarray) -> np.ndarray:
        """
        Applies grabcut to find the relevant area of the image

        Parameters
        ----------
        img: np.ndarray
            The Image
        heatmap: np.ndarray
            The heatmap
        Returns
        -------
        np.ndarray
            0-1-mask where relevant pixels are set to 1
        """
        q_fgd = (
            self.thresh_fgd if self.threshold else np.quantile(heatmap, self.thresh_fgd)
        )
        sure_fgd = cv.compare(heatmap, q_fgd, cv.CMP_GE)

        q_bgd = (
            self.thresh_bgd if self.threshold else np.quantile(heatmap, self.thresh_bgd)
        )
        sure_bgd = cv.compare(heatmap, q_bgd, cv.CMP_LE)

        mask = np.full(img.shape[:2], cv.GC_PR_BGD, np.uint8)
        mask[sure_fgd == 255] = cv.GC_FGD
        mask[sure_bgd == 255] = cv.GC_BGD

        bgdModel = np.zeros((1, 65), np.float64)
        fgdModel = np.zeros((1, 65), np.float64)

        mask, bgdModel, fgdModel = cv.grabCut(
            img, mask, None, bgdModel, fgdModel, 5, cv.GC_INIT_WITH_MASK
        )

        return np.where((mask == 2) | (mask == 0), 0, 1).astype("uint8")
