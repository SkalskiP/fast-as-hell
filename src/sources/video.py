from typing import Generator

import cv2

from src.entities import Frame, VideoConfig
from src.utils.general import exists


class VideoSource:

    def __init__(self, input_file: str) -> None:
        self.__input_file = input_file
        self.__video_capture = None
        self.__frame_index = 0

    @property
    def input_file(self) -> str:
        return self.__input_file

    def generate_frames(self) -> Generator[Frame, None, None]:
        if self.__frame_index > 0 or not exists(self.__video_capture):
            self.__load_video_source()

        while self.__video_capture.isOpened():
            status, image = self.__video_capture.read()
            timestamp = self.__video_capture.get(cv2.CAP_PROP_POS_MSEC)
            if not status:
                break

            frame = Frame(image=image, index=self.__frame_index, timestamp=timestamp)
            self.__frame_index += 1
            yield frame

        self.__close_video_source()

    def __close_video_source(self) -> None:
        self.__video_capture.release()
        self.__video_capture = None

    def __load_video_source(self) -> None:
        self.__video_capture = cv2.VideoCapture(self.__input_file)
        self.__frame_index = 0

    @property
    def config(self) -> VideoConfig:
        if not exists(self.__video_capture):
            self.__load_video_source()
        return VideoConfig(
            fps=self.__video_capture.get(cv2.CAP_PROP_FPS),
            width=int(self.__video_capture.get(cv2.CAP_PROP_FRAME_WIDTH)),
            height=int(self.__video_capture.get(cv2.CAP_PROP_FRAME_HEIGHT)),
            frames_count=int(self.__video_capture.get(cv2.CAP_PROP_FRAME_COUNT))
        )
