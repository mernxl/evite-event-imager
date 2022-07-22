import event_imager_pb2
import event_imager_pb2_grpc
from event_imager.utils import get_ticket_url


class EventImagerService(event_imager_pb2_grpc.EventImagerServicer):
    def getTicketUrl(self, request, context):
        ticket_info = event_imager_pb2.EventEviteTicketInfo(eviteId=request.eviteId)

        ticket_info.ticketUrl = get_ticket_url(
            event_id=request.eventId, evite_id=request.eviteId, ticket_meta=request.ticketMeta
        )

        return ticket_info
