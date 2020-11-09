from __future__ import annotations
from dataclasses import dataclass
from typing import List, Tuple, Optional

import numpy as np

Image = np.array
ClassName = str
ClassIdx = int
Color = Tuple[int, int, int]
Point = Tuple[float, float]
Rect = Tuple[Point, Point, Point, Point]
Size = Tuple[float, float]


@dataclass(frozen=True)
class Frame:
    image: Image
    index: int
    timestamp: int


@dataclass(frozen=True)
class VideoConfig:
    fps: float
    width: int
    height: int
    frames_count: Optional[int] = None


@dataclass(frozen=True)
class BoundingBox:
    x0: float
    y0: float
    x1: float
    y1: float

    @classmethod
    def from_list(cls, bounding_box_values: List[float, float, float, float]) -> BoundingBox:
        return cls(*bounding_box_values)

    @property
    def list(self) -> List[float, float, float, float]:
        return[self.x0, self.y0, self.x1, self.y1]

    @property
    def top_left(self) -> Tuple[int, int]:
        return int(self.x0), int(self.y0)

    @property
    def bottom_right(self) -> Tuple[int, int]:
        return int(self.x1), int(self.y1)

    @property
    def anchor(self) -> Point:
        return (self.x0 + self.x1) / 2, self.y1

    @property
    def area(self) -> float:
        return (self.x1 - self.x0) * (self.y1 - self.y0)

    @property
    def size(self) -> Size:
        return self.x1 - self.x0, self.y1 - self.y0


@dataclass(frozen=True)
class DetectedObject:
    name: ClassName
    confidence: float
    bounding_box: BoundingBox
