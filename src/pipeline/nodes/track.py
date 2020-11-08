from __future__ import annotations

from typing import List, Dict, Optional

from src.entities import BoundingBox, DetectedObject

ActiveObjectsMap = Dict[int, DetectedObject]


class ObjectTracker:

    def __init__(self, objects_map: ActiveObjectsMap) -> None:
        self.__objects_map = objects_map
        self.__objects_index = 0

    @classmethod
    def initialize(cls) -> ObjectTracker:
        return cls(objects_map={})

    def submit_frame(self, objects: List[DetectedObject]) -> None:
        self.__add_new_objects(objects=objects)

    @property
    def objects(self) -> ActiveObjectsMap:
        return self.__objects_map

    def __add_new_objects(self, objects: List[DetectedObject]) -> None:
        for next_object in objects:
            self.__objects_map[self.__objects_index] = next_object
            self.__objects_index += 1

    @staticmethod
    def calculate_iou(bounding_box_a: BoundingBox, bounding_box_b: BoundingBox) -> float:
        bounding_box_a_cords = bounding_box_a.list
        bounding_box_b_cords = bounding_box_b.list

        x0 = max(bounding_box_a_cords[0], bounding_box_b_cords[0])
        y0 = max(bounding_box_a_cords[1], bounding_box_b_cords[1])
        x1 = min(bounding_box_a_cords[2], bounding_box_b_cords[2])
        y1 = min(bounding_box_a_cords[3], bounding_box_b_cords[3])

        intersection = max(0.0, x1 - x0) * max(0.0, y1 - y0)
        return intersection / float(bounding_box_a.area + bounding_box_b.area - intersection)

    @staticmethod
    def match_with_highest_iou(objects_map: ActiveObjectsMap, next_object: DetectedObject) -> Optional[int]:
        best_idx = None
        best_iou = 0
        for idx, last_object in objects_map.items():
            if last_object.name != next_object.name:
                continue

            iou = ObjectTracker.calculate_iou(
                bounding_box_a=last_object.bounding_box, 
                bounding_box_b=next_object.bounding_box
            )

            if iou > best_iou:
                best_idx = idx
                best_iou = iou

        return best_idx
