# fast-as-hell

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
