# fast-as-hell

## Run using Python Virtual Environment

```bash
virtualenv -p python3 .env
source .env/bin/activate
pip install -r docker/requirements.txt
```

## Run using Docker

```bash
docker build -t fast-as-hell -f docker/Dockerfile .
```

```bash
docker run -it \
-p 8888:8888 \
-v $PWD/notebooks:/project/notebooks \
-v $PWD/data:/project/data \
fast-as-hell:latest
```

## Run Notebooks

```bash
jupyter notebook --ip=0.0.0.0 --allow-root --no-browser
```
