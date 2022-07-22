from concurrent import futures

import grpc

import config.env
import event_imager_pb2
import event_imager_pb2_grpc
from config.minio_config import setup_bucket
from utils import get_ticket_url


class EventImagerService(event_imager_pb2_grpc.EventImagerServicer):
    def getTicketUrl(self, request, context):
        ticket_info = event_imager_pb2.EventEviteTicketInfo(eviteId=request.eviteId)

        ticket_info.ticketUrl = get_ticket_url(
            event_id=request.eventId, evite_id=request.eviteId, ticket_meta=request.ticketMeta
        )

        return ticket_info


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    event_imager_pb2_grpc.add_EventImagerServicer_to_server(EventImagerService(), server)

    server.add_insecure_port(f"{config.env.config['server_host']}:{config.env.config['server_port']}")
    print(f"Running GRPC Server at {config.env.config['server_host']}:{config.env.config['server_port']}")
    server.start()
    server.wait_for_termination()


if __name__ == "__main__":
    serve()
    setup_bucket(config.env.config['bucket_name'])
