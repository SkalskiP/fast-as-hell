# fast-as-hell

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
