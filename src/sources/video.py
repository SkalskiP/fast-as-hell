from typing import Generator

import cv2

from src.entities import Frame


class VideoSource:

    def __init__(self, input_file: str) -> None:
        self.__input_file = input_file
        self.__video_capture = None
        self.__frame_index = 0

    @property
    def input_file(self) -> str:
        return self.__input_file

    def generate_frames(self) -> Generator[Frame, None, None]:
        if self.__frame_index > 0:
            self.__load_video_source()

        while self.__captured_video.isOpened():
            status, image = self.__captured_video.read()
            timestamp = self.__captured_video.get(cv2.CAP_PROP_POS_MSEC)
            if not status:
                break

            frame = Frame(image=image, index=self.__frame_index, timestamp=timestamp)
            self.__frame_index += 1
            yield frame

        self.__close_video_source()

    def __close_video_source(self) -> None:
        self.__captured_video.release()
        self.__captured_video = None

    def __load_video_source(self) -> None:
        self.__captured_video = cv2.VideoCapture(self.__input_file)
        self.__frame_index = 0
