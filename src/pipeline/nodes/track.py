from __future__ import annotations

from typing import List, Dict, Optional

from src.entities import DetectedObject
from src.utils.general import exists
from src.utils.iou import calculate_iou

ActiveObjectsMap = Dict[int, DetectedObject]


class ObjectTracker:

    def __init__(self, objects_map: ActiveObjectsMap) -> None:
        self.__objects_map = objects_map
        self.__objects_index = 0

    @classmethod
    def initialize(cls) -> ObjectTracker:
        return cls(objects_map={})

    def submit_frame(self, objects: List[DetectedObject]) -> None:
        previous_object_map = self.__objects_map
        self.__objects_map = {}

        for next_object in objects:
            index = ObjectTracker.match_with_highest_iou(objects_map=previous_object_map, next_object=next_object)
            if exists(index):
                self.__objects_map[index] = next_object
                del previous_object_map[index]
            else:
                self.__objects_map[self.__objects_index] = next_object
                self.__objects_index += 1

    @property
    def objects(self) -> ActiveObjectsMap:
        return self.__objects_map

    @staticmethod
    def match_with_highest_iou(objects_map: ActiveObjectsMap, next_object: DetectedObject) -> Optional[int]:
        best_idx = None
        best_iou = 0
        for idx, last_object in objects_map.items():
            if last_object.name != next_object.name:
                continue

            iou = calculate_iou(
                bounding_box_a=last_object.bounding_box, 
                bounding_box_b=next_object.bounding_box
            )

            if iou > best_iou:
                best_idx = idx
                best_iou = iou

        return best_idx
