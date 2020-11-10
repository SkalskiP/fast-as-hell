from __future__ import annotations

from src.entities import Image, Rect, Color
from src.pipeline.config import TRACKING_REGION_COLOR, SOURCE_RECT
from src.utils.draw import draw_line
import numpy as np


class ViewVisualizer:

    def __init__(self, tracking_region: Rect, color: Color) -> None:
        self.__tracking_region = tracking_region
        self.__color = color

    @classmethod
    def initialize_default(cls) -> ViewVisualizer:
        return cls(
            tracking_region=SOURCE_RECT,
            color=TRACKING_REGION_COLOR
        )

    def draw(self, image: Image) -> Image:
        image = self.draw_tracking_region(image)
        return image

    def draw_tracking_region(self, image: Image) -> Image:
        lines = np.array([
            [self.__tracking_region[0], self.__tracking_region[1]],
            [self.__tracking_region[1], self.__tracking_region[2]],
            [self.__tracking_region[2], self.__tracking_region[3]],
            [self.__tracking_region[3], self.__tracking_region[0]]
        ]).astype(int)
        for line in lines:
            image = draw_line(
                image=image,
                start=tuple(line[0]),
                end=tuple(line[1]),
                color=self.__color,
                thickness=1
            )
        return image
