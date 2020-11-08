from src.entities import BoundingBox
from src.utils.iou import calculate_iou


def test_calculate_iou_when_no_intersection() -> None:
    # given
    bbox_a = BoundingBox(x0=0, y0=0, x1=1, y1=1)
    bbox_b = BoundingBox(x0=2, y0=2, x1=3, y1=3)

    # when
    result = calculate_iou(bounding_box_a=bbox_a, bounding_box_b=bbox_b)

    # then
    assert result == 0.0


def test_calculate_iou_when_bounding_boxes_are_equal() -> None:
    # given
    bbox_a = BoundingBox(x0=0, y0=0, x1=1, y1=1)
    bbox_b = BoundingBox(x0=0, y0=0, x1=1, y1=1)

    # when
    result = calculate_iou(bounding_box_a=bbox_a, bounding_box_b=bbox_b)

    # then
    assert result == 1.0


def test_calculate_iou_when_a_over_b() -> None:
    # given
    bbox_a = BoundingBox(x0=0, y0=0, x1=3, y1=3)
    bbox_b = BoundingBox(x0=0, y0=-1, x1=3, y1=2)

    # when
    result = calculate_iou(bounding_box_a=bbox_a, bounding_box_b=bbox_b)

    # then
    assert result == 0.5


def test_calculate_iou_when_b_over_a() -> None:
    # given
    bbox_a = BoundingBox(x0=0, y0=-1, x1=3, y1=2)
    bbox_b = BoundingBox(x0=0, y0=0, x1=3, y1=3)

    # when
    result = calculate_iou(bounding_box_a=bbox_a, bounding_box_b=bbox_b)

    # then
    assert result == 0.5
