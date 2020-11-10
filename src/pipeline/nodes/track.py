from __future__ import annotations

from typing import List, Dict, Optional

from src.entities import TransformedObject
from src.utils.general import exists
from src.utils.iou import calculate_iou

ActiveObjectsMap = Dict[int, TransformedObject]


class ObjectTracker:

    def __init__(self, objects_map: ActiveObjectsMap, history_steps: int = 5) -> None:
        self.__objects_map = objects_map
        self.__objects_index = 0
        self.__history_steps = history_steps
        self.__history = []

    @classmethod
    def initialize(cls, history_steps: int = 5) -> ObjectTracker:
        return cls(objects_map={}, history_steps=history_steps)

    def submit_frame(self, objects: List[TransformedObject]) -> None:
        prev_object_map = self.__objects_map
        self.__objects_map = {}

        for next_object in objects:
            index = ObjectTracker.match_with_highest_iou(objects_map=prev_object_map, next_object=next_object)
            if exists(index):
                self.__objects_map[index] = next_object
                del prev_object_map[index]
                continue

            historical_match = False
            for step_index in range(len(self.__history)):
                index = ObjectTracker.match_with_highest_iou(
                    objects_map=self.__history[step_index],
                    next_object=next_object
                )
                if exists(index):
                    self.__objects_map[index] = next_object
                    del self.__history[step_index][index]
                    historical_match = True
                    break

            if not historical_match:
                self.__objects_map[self.__objects_index] = next_object
                self.__objects_index += 1

        self.__update_history(objects_map=prev_object_map)

    def __update_history(self, objects_map: ActiveObjectsMap) -> None:
        self.__history = [objects_map] + self.__history[:self.__history_steps - 1]

    @property
    def objects(self) -> ActiveObjectsMap:
        return self.__objects_map

    @staticmethod
    def match_with_highest_iou(objects_map: ActiveObjectsMap, next_object: TransformedObject) -> Optional[int]:
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
