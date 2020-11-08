from typing import List, Optional
import torch

from src.entities import Image, DetectedObject, ClassName, ClassIdx, BoundingBox
from src.utils.general import get_or_else, exists


class InferenceEngine:

    def __init__(self, class_names: Optional[List[ClassName]] = None) -> None:
        model = torch.hub.load(
            github='ultralytics/yolov5',
            model='yolov5s',
            pretrained=True,
            verbose=False
        ).fuse().eval().autoshape()
        self.__model = model
        self.__class_names = get_or_else(item=class_names, default=[])

    def get_class_name(self, class_idx: ClassIdx) -> ClassName:
        return self.__model.names[class_idx]

    def infer(self, image: Image) -> List[DetectedObject]:
        with torch.no_grad():
            result: Optional[List[torch.tensor]] = self.__model(image)
            if not exists(result):
                return []

            return [
                DetectedObject(
                    name=name,
                    confidence=confidence,
                    bounding_box=BoundingBox.from_list(bounding_box_values=bounding_box_values)
                )
                for *bounding_box_values, confidence, cls
                in result[0].numpy()
                if (name := self.get_class_name(int(cls))) not in self.__class_names
            ]
