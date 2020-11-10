from typing import Tuple, Optional

import cv2
import numpy as np
from matplotlib import pyplot as plt

from src.entities import Image, BoundingBox, Color
from src.utils.general import exists


def draw_bounding_box(
    image: Image,
    bounding_box: BoundingBox,
    color: Color = (0, 0, 255),
    thickness: int = 1,
    text: Optional[str] = None
) -> Image:
    image = cv2.rectangle(image, bounding_box.top_left, bounding_box.bottom_right, color, thickness)
    if exists(text):
        image = cv2.putText(
            img=image,
            text=text,
            org=(int(bounding_box.x0), int(bounding_box.y0) - 5),
            fontFace=cv2.FONT_HERSHEY_SIMPLEX,
            fontScale=0.5,
            color=color,
            thickness=thickness,
            lineType=cv2.LINE_AA
        )
    return image


def draw_line(
    image: Image,
    start: Tuple[int, int],
    end: Tuple[int, int],
    color: Color = (255, 255, 255),
    thickness: int = 2
) -> Image:
    return cv2.line(image, start, end, color, thickness=thickness)


def notebook_plot(image: np.array, size: Tuple[int, int] = (20, 20)) -> None:
    plt.figure(figsize=size)
    plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    plt.show()
