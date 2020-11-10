import math

from src.entities import Point


# km / h
def calculate_speed(start_ft: Point, end_ft: Point, time_delta_ms: float) -> float:
    distance_ft = math.sqrt(
        math.pow(end_ft[0] - start_ft[0], 2) +
        math.pow(end_ft[1] - start_ft[1], 2)
    )
    distance_km = distance_ft * 0.0003048
    time_delta_h = time_delta_ms / 3600000
    return distance_km / time_delta_h
