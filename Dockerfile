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

COPY startup-script.sh startup-script.sh

RUN chmod +x startup-script.sh

CMD ["./startup-script.sh"]
