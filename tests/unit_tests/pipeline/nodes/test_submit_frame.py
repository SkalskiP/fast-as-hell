from src.entities import DetectedObject, BoundingBox
from src.pipeline.nodes.track import ObjectTracker


def test_initialize_tracker() -> None:
    # given
    tracker = ObjectTracker.initialize()

    # when
    result = tracker.objects

    # then
    assert result == dict()


def test_first_submit_frame() -> None:
    # given
    tracker = ObjectTracker.initialize()
    object_0 = DetectedObject(name='car', confidence=1.0, bounding_box=BoundingBox(x0=0, y0=0, x1=1, y1=1))
    object_1 = DetectedObject(name='bus', confidence=1.0, bounding_box=BoundingBox(x0=2, y0=2, x1=3, y1=3))
    objects = [object_0, object_1]
    expected_result = {
        0: object_0,
        1: object_1
    }

    # when
    tracker.submit_frame(objects=objects)
    result = tracker.objects

    # then
    assert result == expected_result
