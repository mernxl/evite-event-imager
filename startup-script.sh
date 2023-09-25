#!/bin/bash
set -e

uvicorn_params=$1

# Start the chat-gateway process, use unbuffered prints
OTEL_SERVICE_NAME=evite-event-imager \
OTEL_TRACES_EXPORTER=otlp \
OTEL_METRICS_EXPORTER=otlp \
OTEL_EXPORTER_OTLP_ENDPOINT=$NEW_RELIC_OTEL_ENDPOINT \
OTEL_EXPORTER_OTLP_HEADERS="api-key=$NEW_RELIC_API_KEY" \
  opentelemetry-instrument python main.py

# Wait for any process to exit
wait -n

# Exit with status of process that exited first
exit $?