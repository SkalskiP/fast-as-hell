from src.entities import BoundingBox, DetectedObject
from src.pipeline.nodes.track import ObjectTracker
from src.utils.general import exists


def test_match_with_highest_iou_when_objects_map_empty() -> None:
    # given
    objects_map = {}
    next_object = DetectedObject(name='car', confidence=1.0, bounding_box=BoundingBox(x0=0, y0=0, x1=1, y1=1))

    # when
    result = ObjectTracker.match_with_highest_iou(objects_map=objects_map, next_object=next_object)

    # then
    assert not exists(result)


def test_match_with_highest_iou_when_no_object_from_objects_map_intersects() -> None:
    # given
    objects_map = {
        0: DetectedObject(name='car', confidence=1.0, bounding_box=BoundingBox(x0=-3, y0=-3, x1=-2, y1=-2)),
        1: DetectedObject(name='car', confidence=1.0, bounding_box=BoundingBox(x0=-2, y0=-2, x1=-1, y1=-1)),
        2: DetectedObject(name='car', confidence=1.0, bounding_box=BoundingBox(x0=-2, y0=-2, x1=0, y1=0))
    }
    next_object = DetectedObject(name='car', confidence=1.0, bounding_box=BoundingBox(x0=0, y0=0, x1=1, y1=1))

    # when
    result = ObjectTracker.match_with_highest_iou(objects_map=objects_map, next_object=next_object)

    # then
    assert not exists(result)


def test_match_with_highest_iou_when_object_from_objects_map_intersects_but_has_different_name() -> None:
    # given
    objects_map = {
        0: DetectedObject(name='car', confidence=1.0, bounding_box=BoundingBox(x0=-3, y0=-3, x1=-2, y1=-2)),
        1: DetectedObject(name='car', confidence=1.0, bounding_box=BoundingBox(x0=-2, y0=-2, x1=-1, y1=-1)),
        2: DetectedObject(name='bus', confidence=1.0, bounding_box=BoundingBox(x0=0, y0=0, x1=1, y1=1))
    }
    next_object = DetectedObject(name='car', confidence=1.0, bounding_box=BoundingBox(x0=0, y0=0, x1=1, y1=1))

    # when
    result = ObjectTracker.match_with_highest_iou(objects_map=objects_map, next_object=next_object)

    # then
    assert not exists(result)


def test_match_with_highest_iou_when_multiple_objects_from_objects_map_intersects() -> None:
    # given
    objects_map = {
        0: DetectedObject(name='car', confidence=1.0, bounding_box=BoundingBox(x0=0, y0=-1, x1=2, y1=1)),
        1: DetectedObject(name='car', confidence=1.0, bounding_box=BoundingBox(x0=-1, y0=-1, x1=1, y1=1)),
        2: DetectedObject(name='car', confidence=1.0, bounding_box=BoundingBox(x0=0, y0=0, x1=2, y1=2)),
        3: DetectedObject(name='car', confidence=1.0, bounding_box=BoundingBox(x0=0, y0=0, x1=1, y1=1))
    }
    next_object = DetectedObject(name='car', confidence=1.0, bounding_box=BoundingBox(x0=0, y0=0, x1=2, y1=2))

    # when
    result = ObjectTracker.match_with_highest_iou(objects_map=objects_map, next_object=next_object)

    # then
    assert exists(result)
    assert result == 2
