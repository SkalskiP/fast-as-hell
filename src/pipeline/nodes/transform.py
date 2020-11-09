from __future__ import annotations

import argparse

import cv2
import numpy as np

from src.entities import Rect, Image, Point


class ViewTransformer:
    def __init__(self, M: np.array) -> None:
        self.__M = M

    @classmethod
    def initialize(cls, source: Rect, target: Rect) -> ViewTransformer:
        source_np = np.array(source, dtype="float32")
        target_np = np.array(target, dtype="float32")
        return cls(M=cv2.getPerspectiveTransform(source_np, target_np))

    def transform_point(self, point: Point) -> Point:
        point_3d = np.array([point[0], point[1], 1])
        transformed_point_3d = self.__M.dot(point_3d)
        return np.true_divide(transformed_point_3d, transformed_point_3d[-1])[:2]

    def transform_image(self, image: Image, width: int, height: int) -> Image:
        return cv2.warpPerspective(image, self.__M, (width, height))


if __name__ == "__main__":
    parser = argparse.ArgumentParser('Transform image')

    parser.add_argument(
        "--image",
        help="Path to source image file",
        type=str,
        required=True
    )
    parser.add_argument(
        "--coordinates",
        help="Comma separated list of coordinates of points in the image",
        type=str,
        required=True
    )
    parser.add_argument(
        "--width",
        help="Width of generated output image",
        type=int,
        required=True
    )
    parser.add_argument(
        "--height",
        help="Height of generated output image",
        type=int,
        required=True
    )
    args = parser.parse_args()

    source_rect = eval(args.coordinates)
    target_rect = [
        [0, 0],
        [args.width - 1, 0],
        [args.width - 1, args.height - 1],
        [0, args.height - 1]
    ]
    transformer = ViewTransformer.initialize(source=source_rect, target=target_rect)
    source_image = cv2.imread(args.image)
    result_image = transformer.transform_image(image=source_image, width=args.width, height=args.height)

    cv2.imshow("Source image", source_image)
    cv2.imshow("Target image", result_image)
    cv2.waitKey(0)
