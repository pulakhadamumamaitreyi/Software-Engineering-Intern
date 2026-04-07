from rest_framework.decorators import api_view
from rest_framework.response import Response
from .queue_manager import add_request
from .tasks import process_requests

@api_view(['POST'])
def send_request(request):
    customer_id = request.data.get("customer_id")
    payload = request.data.get("payload")

    add_request(customer_id, payload)

    # trigger async worker
    process_requests.delay()

    return Response({"message": "Request queued"})
