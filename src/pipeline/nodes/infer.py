from typing import List, Optional
import torch

from src.entities import Image, DetectedObject, ClassName, ClassIdx, BoundingBox
from src.utils.general import get_or_else, exists
from src.utils.iou import calculate_iou


class InferenceEngine:

    def __init__(self, class_names: Optional[List[ClassName]] = None, threshold_iou: float = 0.9) -> None:
        model = torch.hub.load(
            github='ultralytics/yolov5',
            model='yolov5s',
            pretrained=True,
            verbose=False
        ).fuse().eval().autoshape()
        self.__model = model
        self.__class_names = get_or_else(item=class_names, default=self.__model.names)
        self.__threshold_iou = threshold_iou

    def get_class_name(self, class_idx: ClassIdx) -> ClassName:
        return self.__model.names[class_idx]

    def infer(self, image: Image) -> List[DetectedObject]:
        with torch.no_grad():
            result: Optional[List[torch.tensor]] = self.__model(image)
            if not exists(result):
                return []

            return self.post_process([
                DetectedObject(
                    name=name,
                    confidence=confidence,
                    bounding_box=BoundingBox.from_list(bounding_box_values=bounding_box_values)
                )
                for *bounding_box_values, confidence, cls
                in result[0].numpy()
                if (name := self.get_class_name(int(cls))) in self.__class_names
            ])

    def post_process(self, objects: List[DetectedObject]) -> List[DetectedObject]:
        results = []
        for next_object in objects:
            drop = False
            for result in results:
                iou = calculate_iou(
                    bounding_box_a=result.bounding_box,
                    bounding_box_b=next_object.bounding_box
                )
                if iou > self.__threshold_iou and result.name == next_object.name:
                    drop = True
            if not drop:
                results.append(next_object)
        return results

