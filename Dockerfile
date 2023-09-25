# syntax=docker/dockerfile:1

FROM python:3.11-slim-buster

RUN mkdir /service

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY event_imager /service/event_imager
COPY protobufs /service/protobufs

WORKDIR /service/event_imager

RUN python -m grpc_tools.protoc -I ../protobufs --python_out=. \
               --grpc_python_out=. ../protobufs/event_imager.proto

ENV OTEL_SERVICE_NAME=evite-event-imager
ENV OTEL_TRACES_EXPORTER=otlp
ENV OTEL_METRICS_EXPORTER=otlp
ENV OTEL_EXPORTER_OTLP_ENDPOINT=$NEW_RELIC_OTEL_ENDPOINT
ENV OTEL_EXPORTER_OTLP_HEADERS="api-key=$NEW_RELIC_API_KEY"

CMD [ "opentelemetry-instrument", "python", "main.py"]
