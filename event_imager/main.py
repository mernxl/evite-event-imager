import sys
from concurrent import futures
import logging

import grpc

from config.env import config
import event_imager_pb2_grpc
from event_imager_service import EventImagerService


def serve():
    # enable logging with INFO level @see https://docs.python.org/3/howto/logging.html#configuring-logging-for-a-library
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO, stream=sys.stdout
    )

    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    event_imager_pb2_grpc.add_EventImagerServicer_to_server(EventImagerService(), server)

    server.add_insecure_port(f"{config['server_host']}:{config['server_port']}")
    logging.info(f"Running GRPC Server at {config['server_host']}:{config['server_port']}")
    server.start()
    server.wait_for_termination()


if __name__ == "__main__":
    serve()
