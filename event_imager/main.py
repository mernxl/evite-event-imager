from concurrent import futures

import grpc

from config.env import config
import event_imager_pb2_grpc
from event_imager_service import EventImagerService


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    event_imager_pb2_grpc.add_EventImagerServicer_to_server(EventImagerService(), server)

    server.add_insecure_port(f"{config.env.config['server_host']}:{config.env.config['server_port']}")
    print(f"Running GRPC Server at {config.env.config['server_host']}:{config.env.config['server_port']}")
    server.start()
    server.wait_for_termination()


if __name__ == "__main__":
    serve()
