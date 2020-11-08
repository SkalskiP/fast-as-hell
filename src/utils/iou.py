from src.entities import BoundingBox


def calculate_iou(bounding_box_a: BoundingBox, bounding_box_b: BoundingBox) -> float:
    bounding_box_a_cords = bounding_box_a.list
    bounding_box_b_cords = bounding_box_b.list

    x0 = max(bounding_box_a_cords[0], bounding_box_b_cords[0])
    y0 = max(bounding_box_a_cords[1], bounding_box_b_cords[1])
    x1 = min(bounding_box_a_cords[2], bounding_box_b_cords[2])
    y1 = min(bounding_box_a_cords[3], bounding_box_b_cords[3])

    intersection = max(0.0, x1 - x0) * max(0.0, y1 - y0)
    return intersection / float(bounding_box_a.area + bounding_box_b.area - intersection)
