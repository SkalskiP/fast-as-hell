FROM python:3.8

COPY docker/requirements.txt /

RUN pip install -r /requirements.txt && \
    mkdir -p /project

COPY . /project
WORKDIR /project

ENTRYPOINT [ "/bin/bash" ]