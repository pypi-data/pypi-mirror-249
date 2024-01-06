from dataclasses import asdict, dataclass, field
from typing import List, Tuple, Union

from PIL.Image import Image
import numpy as np

__all__ = [
    "Part",
    "ExplanationMap",
    "Object",
    "Result",
]


@dataclass(frozen=True)
class Part:
    img: Image = field(repr=False)
    relevancy: Union[int, float]
    labels: List[int]
    rect: Tuple[int, int, int, int]


@dataclass(frozen=True)
class ExplanationMap:
    map: np.ndarray = field(repr=False)
    explanation_method: str


@dataclass(frozen=True)
class Object:
    heatmap: np.ndarray = field(repr=False)
    explanation_maps: List[ExplanationMap]
    label: str
    parts: List[Part]


@dataclass(frozen=True)
class Result:
    img: Image = field(repr=False)
    objects: List[Object]

    def as_dict(self):
        return asdict(self)
