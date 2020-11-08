from typing import Tuple

import cv2
import numpy as np
from matplotlib import pyplot as plt

from src.entities import Image, BoundingBox, Color


def draw_bounding_box(image: Image, bounding_box: BoundingBox, color: Color = (255, 255, 255), thickness: int = 2) -> Image:
    image = cv2.rectangle(image, bounding_box.top_left, bounding_box.bottom_right, color, thickness)
    return image


def notebook_plot(image: np.array, size: Tuple[int, int] = (20, 20)) -> None:
    plt.figure(figsize=size)
    plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    plt.show()
