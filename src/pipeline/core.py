import argparse

import numpy as np
from tqdm import tqdm

from src.pipeline.nodes.infer import InferenceEngine
from src.pipeline.nodes.track import ObjectTracker
from src.sources.video import VideoSource
from src.targets.video import VideoTarget
from src.utils.draw import draw_bounding_box

if __name__ == "__main__":
    parser = argparse.ArgumentParser('Fast as Hell')

    parser.add_argument(
        "--source_video_path", "-s",
        help="Path to source video file in mp4 format",
        type=str,
        required=True
    )
    parser.add_argument(
        "--target_video_path", "-t",
        help="Path to target video file in mp4 format",
        type=str,
        required=True
    )
    args = parser.parse_args()

    inference_engine = InferenceEngine(class_names=['car'])
    video_source = VideoSource(input_file=args.source_video_path)
    video_config = video_source.config
    tacker = ObjectTracker.initialize()
    with VideoTarget(target_path=args.target_video_path, config=video_config) as target:
        for frame in tqdm(video_source.generate_frames(), total=video_config.frames_count):
            image = np.copy(frame.image)
            predictions = inference_engine.infer(frame.image)
            tacker.submit_frame(predictions)
            objects = tacker.objects
            for object_idx, object_data in objects.items():
                image = draw_bounding_box(
                    image=image,
                    bounding_box=object_data.bounding_box,
                    text=f"{object_data.name} id: {object_idx}"
                )
            target.write(image)
