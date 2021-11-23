from django.http import HttpResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework import permissions
from ..core import Inventory

@api_view(['POST'])
@permission_classes((permissions.AllowAny,))
def inventory_collect(request):
    """Trigger Netdisco inventory data retrieval."""
    Inventory.collect()
    response = Inventory.notify()
    return HttpResponse(
        content=response.content,
        status=response.status_code,
        content_type=response.headers['Content-Type']
    )
