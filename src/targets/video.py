from __future__ import annotations
from src.entities import VideoConfig, Image
import cv2

from src.targets.errors import VideoWriterNotInitialized
from src.utils.file import create_parent_dir
from src.utils.general import exists


class VideoTarget:

    def __init__(self, target_path: str, config: VideoConfig) -> None:
        self.__target_path = target_path
        self.__config = config
        self.__video_writer = None

    def __enter__(self):
        create_parent_dir(self.__target_path)
        self.__video_writer = cv2.VideoWriter(
                self.__target_path,
                fourcc=cv2.VideoWriter_fourcc(*"mp4v"),
                fps=self.__config.fps,
                frameSize=(self.__config.width, self.__config.height),
                isColor=True
            )
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.__video_writer.release()

    def write(self, frame: Image) -> None:
        if not exists(self.__video_writer):
            raise VideoWriterNotInitialized()
        self.__video_writer.write(frame)
