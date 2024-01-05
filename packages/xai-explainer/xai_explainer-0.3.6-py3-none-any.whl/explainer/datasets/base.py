from abc import abstractstaticmethod
from typing import List

from PIL import Image
import torch

__all__ = ["VisionDataset", "ClassificationDataset"]


class StaticClassInstatiationError(Exception):
    pass


class VisionDataset:
    def __init__(self):
        raise StaticClassInstatiationError(
            "This class and its subclasses should not be instantiated. All methods are defined statically and should be called as such."
        )

    @abstractstaticmethod
    def transform(img: Image.Image) -> torch.Tensor:
        raise NotImplementedError

    @abstractstaticmethod
    def inverse_transform(tensor: torch.Tensor) -> Image.Image:
        """Not too important, but can be useful for debugging."""
        raise NotImplementedError


class ClassificationDataset(VisionDataset):
    @abstractstaticmethod
    def classes() -> List[str]:
        raise NotImplementedError

    @classmethod
    def class_index_to_name(cls, idx: int) -> str:
        return cls.classes()[idx]

    @classmethod
    def num_classes(cls) -> int:
        return len(cls.classes())
