# Evite Event Imager

Package generates and places a QR code on a ticket, for a specific evite.

### Configuring Opentelemetry
Followed the Auto-Instrumentation to setup, as seen [here](https://opentelemetry.io/docs/instrumentation/python/automatic/).

Run the following to auto-instrument
```shell
opentelemetry-bootstrap -a install
```

Run the application with auto-instrumentation, on local machine
```shell
OTEL_SERVICE_NAME=evite-event-imager \
OTEL_TRACES_EXPORTER=console,otlp \
OTEL_METRICS_EXPORTER=console,otlp \
OTEL_EXPORTER_OTLP_ENDPOINT=otlp.eu01.nr-data.net:4318 \
OTEL_EXPORTER_OTLP_HEADERS="api-key=<<API_KEY>>" \
opentelemetry-instrument \
    python event_imager/main.py
```