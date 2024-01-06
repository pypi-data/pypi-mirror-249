from typing import Callable, Dict, Final, Optional, Tuple

import numpy as np

from explainer.models.base import XAI_Map, XAI_Method, XAI_MethodType

__all__ = ["compute_relevances"]


def create_top_percentile_reduction_fn(
    percent: float, reduction_fn: Callable
) -> Callable:
    """
    Creates a function that reduces the top percentile of values using a specified reduction function.

    Args:
        percent (float): the percentile to consider for reduction
        reduction_fn (Callable): the function to use for reduction
    """

    def top_percentile_reduction_fn(values: np.ndarray) -> float:
        """
        Dynamic top percent reduction function.

        Args:
            values (np.ndarray): the values to reduce
        """

        # Calculate the threshold for the top percentile (flattening the array first)
        percentile_threshold = np.percentile(values, percent)

        # Get the values that are in the top percentile
        top_percentile_values = values[values >= percentile_threshold]

        # Fail-safe: If there are no values in the top percentile, return the maximum value
        if len(top_percentile_values) == 0:
            return np.max(values)

        # Apply the reduction function to the top percentile values
        return reduction_fn(top_percentile_values)

    return top_percentile_reduction_fn


def identity(x):
    """Identity function"""
    return x


DEFAULT_METHODS: Final[Dict[XAI_MethodType, Dict]] = {
    XAI_MethodType.HEATMAP: {
        "preprocessor": identity,
        "filter_fn": lambda _: True,
        "reduction_fn": np.mean,
    },
    XAI_MethodType.EDGEMAP: {
        "preprocessor": lambda x: np.clip(x, -1, 1),  # np.tanh,  #
        "filter_fn": lambda _: True,
        "reduction_fn": np.mean,  # create_top_percentile_reduction_fn(90, np.mean),
    },
}

SPECIFIC_METHODS: Final[Dict[Tuple[str, str], Dict]] = {}


def get_handle_for(m: XAI_Method, target_fun: str) -> Callable:
    """
    Get the handle for the given method and target function.

    Args:
        m (XAI_Method): the XAI method
        target_fun (str): the target function (preprocessor, filter_fn, reduction_fn)
    """
    m_type, m_name = m.method_type, m.name
    if (m_type, m_name) in SPECIFIC_METHODS:
        return SPECIFIC_METHODS[(m_type, m_name)][target_fun]

    return DEFAULT_METHODS[m_type][target_fun]


def get_preprocessor(m: XAI_Method) -> Callable:
    return get_handle_for(m, "preprocessor")


def get_filter_fn(m: XAI_Method) -> Callable:
    return get_handle_for(m, "filter_fn")


def get_reduction_fn(m: XAI_Method) -> Callable:
    return get_handle_for(m, "reduction_fn")


def compute_segment_score(segment_values, x_method) -> float:
    segment_values = list(filter(get_filter_fn(x_method), segment_values))
    score = get_reduction_fn(x_method)(segment_values)
    return float(min(1, max(0, score)))


def normalize_scores(scores):
    total_sum = sum(scores.values())

    eps = 1e-10  # to avoid division by zero
    if total_sum < eps:
        n_segs = len(scores)
        evaluation = {k: 1 / n_segs for k, _ in scores.items()}
    else:
        evaluation = {
            k: v / total_sum if total_sum != 0 else 0 for k, v in scores.items()
        }

    return evaluation


def compute_relevances(
    xai_map: XAI_Map, segmentation: np.ndarray, normalize: Optional[bool] = True
) -> Dict[int, float]:
    """
    Compute the relevances for each segment in the given segmentation.

    Args:
        xai_map (XAI_Map): the XAI map
        segmentation (np.ndarray): the segmentation
        normalize (bool, optional): whether to normalize the relevances. Defaults to True.

    Returns:
        Dict[int, float]: the relevances for each segment, indexed by the segment id. Relevances are between 0 and 1 and sum up to 1.
    """
    x_map, x_method = xai_map.map, xai_map.method
    unique_segments = [
        int(x) for x in np.unique(segmentation)
    ]  # fix types to match spec

    from explainer.parts_extraction.extraction import DEBUGGING_LEVEL, DEBUGGING_LOGGER

    if DEBUGGING_LEVEL == 2:
        label_idx = xai_map.predicted_label
        DEBUGGING_LOGGER[
            f"object_{label_idx}/xai_methods/{x_method.name}/relevancy_computation/1_raw_map.png"
        ] = x_map

    x_map = get_preprocessor(x_method)(x_map)

    if DEBUGGING_LEVEL == 2:
        DEBUGGING_LOGGER[
            f"object_{label_idx}/xai_methods/{x_method.name}/relevancy_computation/2_preprocessed_map.png"
        ] = x_map

    scores = {
        segment_id: compute_segment_score(x_map[segmentation == segment_id], x_method)
        for segment_id in unique_segments
    }

    if DEBUGGING_LEVEL == 2:
        DEBUGGING_LOGGER[
            f"object_{label_idx}/xai_methods/{x_method.name}/relevancy_computation/3.1_raw_scores.json"
        ] = scores

    scores = normalize_scores(scores) if normalize else scores

    if DEBUGGING_LEVEL == 2:
        DEBUGGING_LOGGER[
            f"object_{label_idx}/xai_methods/{x_method.name}/relevancy_computation/3.2_normalized_scores.json"
        ] = scores

    return scores
