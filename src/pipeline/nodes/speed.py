import math
from collections import deque
from copy import deepcopy
from typing import Tuple

from src.entities import Point, TransformedObject
from src.pipeline.nodes.track import ActiveObjectsMap
from src.utils.general import exists

LogEntry = Tuple[float, TransformedObject]


class SpeedEstimator:

    def __init__(self, history_window_size: int = 60) -> None:
        self.__history_window_size = history_window_size
        self.__history = {}

    def submit_frame(self, objects: ActiveObjectsMap, timestamp: float) -> None:
        for index, data in deepcopy(objects).items():
            entry = (timestamp, data)
            if exists(self.__history.get(index)):
                self.__history.get(index).append(entry)
            else:
                self.__insert_new_object(index=index, entry=entry)

    def __insert_new_object(self, index: int, entry: LogEntry) -> None:
        self.__history[index] = deque([entry], maxlen=self.__history_window_size)

    def get_speed(self, index: int) -> float:
        if exists(self.__history.get(index)):
            log = list(self.__history.get(index))
            time_delta_ms = log[-1][0] - log[0][0]
            if time_delta_ms == 0.0:
                return 0.0

            return calculate_speed(
                start_ft=log[0][1].position,
                end_ft=log[-1][1].position,
                time_delta_ms=log[-1][0]-log[0][0]
            )
        else:
            return 0.0


# km / h
def calculate_speed(start_ft: Point, end_ft: Point, time_delta_ms: float) -> float:
    distance_ft = math.sqrt(
        math.pow(end_ft[0] - start_ft[0], 2) +
        math.pow(end_ft[1] - start_ft[1], 2)
    )
    distance_km = distance_ft * 0.0003048
    time_delta_h = time_delta_ms / 3600000
    return distance_km / time_delta_h
