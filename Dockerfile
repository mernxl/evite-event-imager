# syntax=docker/dockerfile:1

FROM python:3.9-slim-buster

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY utils.py ./
COPY config ./config
COPY protobufs ./protobufs
COPY event_imager ./event_imager

CMD [ "python", "event_imager/event_imager_service.py"]
