from __future__ import annotations

import argparse
from typing import List

import numpy as np
from tqdm import tqdm

from src.entities import Frame, Image, DetectedObject, TransformedObject, Rect, Point, BoundingBox
from src.pipeline.config import TRACKED_CLASSES, SOURCE_RECT, TARGET_RECT
from src.pipeline.nodes import ViewTransformer
from src.pipeline.nodes.infer import InferenceEngine
from src.pipeline.nodes.speed import SpeedEstimator
from src.pipeline.nodes.track import ObjectTracker
from src.pipeline.nodes.visualize import ViewVisualizer
from src.sources.video import VideoSource
from src.targets.video import VideoTarget
from src.utils.draw import draw_bounding_box


class Pipeline:
    def __init__(
        self,
        model: InferenceEngine,
        tracker: ObjectTracker,
        transformer: ViewTransformer,
        estimator: SpeedEstimator,
        visualizer: ViewVisualizer,
        source_rect: Rect,
        target_rect: Rect
    ) -> None:
        self.__model = model
        self.__tracker = tracker
        self.__transformer = transformer
        self.__estimator = estimator
        self.__visualizer = visualizer
        self.__source_rect = source_rect
        self.__target_rect = target_rect

    @classmethod
    def initialize_default(cls) -> Pipeline:
        return cls(
            model=InferenceEngine(class_names=TRACKED_CLASSES),
            tracker=ObjectTracker.initialize(),
            transformer=ViewTransformer.initialize(source=SOURCE_RECT, target=TARGET_RECT),
            estimator=SpeedEstimator(),
            visualizer=ViewVisualizer.initialize_default(),
            source_rect=SOURCE_RECT,
            target_rect=TARGET_RECT
        )

    def next_frame(self, frame: Frame) -> Image:
        image = np.copy(frame.image)
        detected_objects = self.__model.infer(frame.image)
        transformed_objects = self.__transform(detected_objects=detected_objects)
        transformed_objects = self.__drop_objects_outside_target_rect(transformed_objects=transformed_objects)

        self.__tracker.submit_frame(objects=transformed_objects)
        objects = self.__tracker.objects
        self.__estimator.submit_frame(objects=objects, timestamp=frame.timestamp)

        image = self.__visualizer.draw(image=image)
        for index, data in objects.items():
            speed = self.__estimator.get_speed(index=index)
            image = draw_bounding_box(
                image=image,
                bounding_box=data.bounding_box,
                text=f"{data.name} | {speed:.0f} km/h"
            )
            anchor = data.bounding_box.anchor
            image = draw_bounding_box(
                image=image,
                bounding_box=BoundingBox(
                    x0=anchor[0] - 5,
                    y0=anchor[1] - 5,
                    x1=anchor[0] + 5,
                    y1=anchor[1] + 5
                ),
                thickness=-1,
                color=(255, 255, 255)
            )

        return image

    def __transform(self, detected_objects: List[DetectedObject]) -> List[TransformedObject]:
        return [
            TransformedObject.from_detected_object(
                detected_object=detected_object,
                position=self.__transformer.transform_point(detected_object.bounding_box.anchor)
            )
            for detected_object
            in detected_objects
        ]

    def __drop_objects_outside_target_rect(
        self, transformed_objects: List[TransformedObject]
    ) -> List[TransformedObject]:
        def validate_point(rect: Rect, point: Point) -> bool:
            return all([
                rect[0][0] < point[0],
                rect[2][0] > point[0],
                rect[0][1] < point[1],
                rect[2][1] > point[1]
            ])

        return [
            transformed_object
            for transformed_object
            in transformed_objects
            if validate_point(rect=self.__target_rect, point=transformed_object.position)
        ]


if __name__ == "__main__":
    parser = argparse.ArgumentParser('Fast as Hell')

    parser.add_argument(
        "--source_video_path", "-s",
        help="Path to source video file in mp4 format",
        type=str,
        required=True
    )
    parser.add_argument(
        "--target_video_path", "-t",
        help="Path to target video file in mp4 format",
        type=str,
        required=True
    )
    args = parser.parse_args()

    pipeline = Pipeline.initialize_default()
    video_source = VideoSource(input_file=args.source_video_path)
    video_config = video_source.config
    with VideoTarget(target_path=args.target_video_path, config=video_config) as target:
        for frame in tqdm(video_source.generate_frames(), total=video_config.frames_count):
            target.write(pipeline.next_frame(frame=frame))
