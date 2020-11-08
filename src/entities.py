from __future__ import annotations
from dataclasses import dataclass
from typing import List

import numpy as np

Image = np.array
ClassName = str
ClassIdx = int


@dataclass(frozen=True)
class Frame:
    image: Image
    index: int
    timestamp: int


@dataclass(frozen=True)
class BoundingBox:
    x: float
    y: float
    width: float
    height: float

    @classmethod
    def from_list(cls, bounding_box_values: List[float, float, float, float]) -> BoundingBox:
        return cls(*bounding_box_values)

    def to_list(self) -> List[float, float, float, float]:
        return[self.x, self.y, self.width, self.height]


@dataclass(frozen=True)
class DetectedObject:
    name: ClassName
    confidence: float
    bounding_box: BoundingBox
