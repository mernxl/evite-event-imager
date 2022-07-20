# syntax=docker/dockerfile:1

FROM python:3.9-slim-buster

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY config event_imager protobufs utils.py ./

CMD [ "python3", "event_imager/event_imager_service.py"]
