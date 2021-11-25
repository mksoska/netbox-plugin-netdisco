from django.http import HttpResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework import permissions
from ..core import Inventory
import json

@api_view(['POST'])
@permission_classes((permissions.AllowAny,))
def inventory_collect(request):
    """Trigger Netdisco inventory data retrieval."""
    Inventory.collect()
    response = Inventory.notify()
    
    return HttpResponse(
        content=json.dumps({"collect": "Inventory collected.", "notify": "Notification successfuly sent."}),
        status=200,
        content_type=response.headers['Content-Type']
    ) if response.status_code == 200 else HttpResponse(
        content=json.dumps({ "collect": "Inventory collected.", "notify": "Notification failed."}),
        status=500,
        content_type=response.headers['Content-Type']
    )
