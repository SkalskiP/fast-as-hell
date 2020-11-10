# fast-as-hell

## Pipeline specification

The processing pipeline is composed of five basic elements:
* `InferenceEngine`
* `ViewTransformer`
* `ObjectTracker`
* `SpeedEstimator`
* `ViewVisualizer`

### InferenceEngine

To detect objects moving along the road I used state-of-the-art object detection model - [yolo5][1], implemented in PyTorch. I packed the whole thing in Python class to make it easier to use the model inside the pipeline. Prediction with this model is relatively fast and used implementation does not require a graphic card to run. The model provides high quality predictions, but from time to time there are problems that have been largely eliminated:

* **false positives** - the model detects objects where they do not exist
* **false negatives** - the model does not detect objects even though they are visible
* **duplication of objects** - the model provides multiple bounding boxes, representing the same object

### ViewTransformer

### ObjectTracker

### SpeedEstimator

### ViewVisualizer

## Hit the ground running

### Run using Python Virtual Environment

```bash
virtualenv -p python3 .env
source .env/bin/activate
pip install -r docker/requirements.txt
```

### Run using Docker

```bash
docker build -t fast-as-hell -f docker/Dockerfile .
```

```bash
docker run -it \
-p 8888:8888 \
-v $PWD/notebooks:/project/notebooks \
-v $PWD/src:/project/src \
-v $PWD/tests:/project/tests \
-v $PWD/data:/project/data \
fast-as-hell:latest
```

### Run pipeline

``` bash
python -m src.pipeline.core \
--source_video_path "data/videos/video_01.mp4" \
--target_video_path "data/videos/tracking/video_01.mp4"
```

### Run Notebooks

```bash
jupyter notebook --ip=0.0.0.0 --allow-root --no-browser
```

### Run tests

```bash
pytest
```
[1]: https://github.com/ultralytics/yolov5
