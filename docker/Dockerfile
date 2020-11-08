FROM python:3.8

COPY docker/requirements.txt /

RUN apt-get update && apt-get upgrade -y && apt-get install -y libgl1-mesa-glx && \
    pip install -r /requirements.txt && \
    jupyter nbextension enable --py widgetsnbextension --sys-prefix && \
    jupyter contrib nbextension install --user && \
    mkdir -p /project

COPY . /project
WORKDIR /project

ENTRYPOINT [ "/bin/bash" ]