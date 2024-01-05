from dataclasses import dataclass
from typing import Callable, Dict, List, Union

from PIL import Image
import cv2 as cv
import numpy as np
import skimage.segmentation as seg
import torch.nn as nn

import explainer.models as _models
from explainer.models.base import VisionModel

__all__ = [
    "list_segmentation_methods",
    "get_segmentation_method",
]


class SegmentationWrapper(VisionModel):
    def __init__(
        self,
        fn: Union[Callable[[np.ndarray], np.ndarray], nn.Module],
        default_kwargs: Dict = dict(),
    ):
        super().__init__()
        self.fn = fn  # the function or nn.Module to wrap
        self.default_kwargs = default_kwargs

    def forward(self, img: np.ndarray, maps: List[_models.XAI_Map], **kwargs):
        """
        Runs the segmentation method on the image.

        Args:
            img: The image.
            maps: The maps to use for the segmentation.

        Returns:
            The segmentation. 0 is being used as an indicator for the background. The segmentation should be a 2D array of the same shape as the image.
        """

        kwargs = {**self.default_kwargs, **kwargs}
        # TODO: handle segmentationmap. If maps contains a segmentationmap, return this segmentation and don't call self.fn
        while True:
            try:
                return self.fn(img, **kwargs)
            except TypeError as e:
                if "unexpected keyword argument" in str(e):
                    # Remove unexpected keyword argument
                    unexpected_kwarg = str(e).split("'")[1]
                    kwargs.pop(unexpected_kwarg)

                    print(f"Removed unexpected keyword argument {unexpected_kwarg}.")

                else:
                    raise e


@dataclass(frozen=True)
class RegisteredSegmentationMethod:
    handle: Callable
    name: str
    is_builder: bool  # Flag to indicate if the handle is a builder function or can be called directly
    default_kwargs: Dict
    builder_kwargs: Dict
    hidden: bool

    def __post_init__(self):
        if not self.is_builder:
            assert (
                len(self.builder_kwargs) == 0
            ), "builder_kwargs should only be specified if is_builder is True."

    def initialize(self):
        handle = self.handle(**self.builder_kwargs) if self.is_builder else self.handle

        return SegmentationWrapper(handle, self.default_kwargs)


REGISTERED_SEGMENTATION_METHODS = {}  # type: Dict[str, RegisteredSegmentationMethod]


def register_segmentation_method(
    name: str = None,
    is_builder: bool = False,
    default_kwargs: Dict = dict(),
    builder_kwargs: Dict = dict(),
    hidden: bool = False,
) -> Callable[[Callable], Callable]:
    """
    Registers a segmentation method.

    Args:
        name: The name of the segmentation method. If None, the name of the function is used.
        is_builder: A flag to indicate if the handle is a builder function or can be called directly.
        default_kwargs: Default keyword arguments for the segmentation method.
        builder_kwargs: Keyword arguments for the builder function.
        hidden: A flag to indicate if the segmentation method should be hidden from the list_segmentation_methods function.

    Returns:
        A decorator that registers the segmentation method.
    """

    def decorator(fn: Callable):
        global REGISTERED_SEGMENTATION_METHODS
        nonlocal name

        if name is None:
            name = fn.__name__

        if name in REGISTERED_SEGMENTATION_METHODS:
            raise ValueError(
                f"A segmentation method with the name {name} has already been registered."
            )

        REGISTERED_SEGMENTATION_METHODS[name] = RegisteredSegmentationMethod(
            handle=fn,
            name=name,
            is_builder=is_builder,
            default_kwargs=default_kwargs,
            builder_kwargs=builder_kwargs,
            hidden=hidden,
        )
        return fn

    return decorator


def list_segmentation_methods():
    methods = list(REGISTERED_SEGMENTATION_METHODS.keys())
    methods = [m for m in methods if not REGISTERED_SEGMENTATION_METHODS[m].hidden]
    return methods


def get_segmentation_method(method_name: str) -> SegmentationWrapper:
    return REGISTERED_SEGMENTATION_METHODS[method_name].initialize()


# slic is needed as a backup if sam fails!
register_segmentation_method(
    default_kwargs={
        "n_segments": 1000,
        "start_label": 1,  # 0 is reserved for background, slic does not have a distinction between background and foreground
        "compactness": 10,
    },
    hidden=True,
)(
    seg.slic
)  # allows mask


@register_segmentation_method(
    default_kwargs={
        "ratio": 0.9,
        "kernel_size": 5,
        "max_dist": 25,
        "return_tree": False,
        "sigma": 0.5,
        "convert2lab": True,
        "rng": 42,
    },
    hidden=True,
)
def quickshift(img: np.ndarray, **kwargs):
    seg_res = seg.quickshift(img, **kwargs)  # no mask
    seg_res += 1
    assert seg_res.min() == 1, "quickshift should not return 0 as a label"

    return seg_res


@register_segmentation_method(hidden=True)
def watershed(img: np.ndarray, **kwargs):
    img = cv.cvtColor(img, cv.COLOR_RGB2GRAY)
    seg_res = seg.watershed(img, **kwargs)  # no mask
    assert seg_res.min() == 1, "watershed should not return 0 as a label"

    return seg_res


@register_segmentation_method(
    default_kwargs={"scale": 100, "sigma": 0.8, "min_size": 20}, hidden=True
)
def felzenszwalb(img: np.ndarray, **kwargs):
    img = cv.cvtColor(img, cv.COLOR_RGB2GRAY)
    seg_res = seg.felzenszwalb(img, **kwargs)  # no mask
    seg_res += 1  # 0 is reserved for background, felzenszwalb does not have a distinction between background and foreground

    return seg_res


@register_segmentation_method(hidden=True)
def chan_vese(img: np.ndarray):
    raise NotImplementedError("chan_vese is not working yet. @Daniel")
    img = cv.cvtColor(img, cv.COLOR_RGB2GRAY)
    seg_res = seg.chan_vese(img)  # no mask

    return seg_res


class SAM_Wrapper(nn.Module):  # no mask
    def __init__(self, sam):
        super().__init__()
        self.sam = sam

    def forward(self, img: np.ndarray):
        img = Image.fromarray(img)

        pred = self.sam.predict(img)

        return pred


for segmentation_model in _models.list_models(model_type="segmentation_model"):

    @register_segmentation_method(
        name=segmentation_model,
        is_builder=True,
        hidden=segmentation_model != "segment_anything_huge",  # only huge is visible
    )
    def build_sam():
        sam = _models.get_model(segmentation_model)
        sam = SAM_Wrapper(sam)
        return sam


def show_segmentation_on_image(
    img: np.ndarray, segmentation: np.ndarray
) -> Image.Image:
    """
    Shows the segmentation on the image.

    Args:
        img: The image.
        segmentation: The segmentation.

    Returns:
        The image with the segmentation overlayed.
    """
    from skimage.segmentation import mark_boundaries

    def _prepare_img(img) -> np.ndarray:
        if img.max() <= 1:
            img *= 255
            img = np.array(img, dtype=np.uint8)
        else:
            img = np.array(img, dtype=np.uint8)

        return img

    fig = mark_boundaries(img, segmentation)
    fig = _prepare_img(fig)

    return Image.fromarray(fig)
