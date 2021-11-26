from django.http import HttpResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework import permissions
from ..core import Inventory
import json


def collect_response(label):
    return HttpResponse(
        content=json.dumps({"collect": label + "collected."}),
        status=200,
        content_type='Accept: application/json'
    )


@api_view(['POST'])
@permission_classes((permissions.AllowAny,))
def inventory_collect(request):
    """Trigger Netdisco inventory data retrieval."""
    Inventory.collect()
    return collect_response("Inventory ")
    
@api_view(['POST'])
@permission_classes((permissions.AllowAny,))
def inventory_notify(request):
    response = Inventory.notify()
    
    return HttpResponse(
        content=json.dumps({"notify": "Notification successfuly sent."}),
        status=200,
        content_type=response.headers['Content-Type']
    ) if response.status_code == 200 else HttpResponse(
        content=json.dumps({"notify": "Notification failed."}),
        status=500,
        content_type=response.headers['Content-Type']
    )


@api_view(['POST'])
@permission_classes((permissions.AllowAny,))
def collect_devices(request):
    Inventory.collect_devices()
    return collect_response("Devices ")


@api_view(['POST'])
@permission_classes((permissions.AllowAny,))
def collect_device(request, ip):
    Inventory.collect_device(ip)
    return collect_response(f"Device {ip} ")

@api_view(['POST'])
@permission_classes((permissions.AllowAny,))
def collect_ports(request, ip):
    Inventory.collect_ports(ip)
    return collect_response("Ports of device {ip} ")


@api_view(['POST'])
@permission_classes((permissions.AllowAny,))
def collect_port(request, ip, port):
    Inventory.collect_port(ip, port)
    return collect_response("Port {port} of device {ip} ")


@api_view(['POST'])
@permission_classes((permissions.AllowAny,))
def collect_addresses(request, ip):
    Inventory.collect_addresses(ip)
    return collect_response("IP addresses of device {ip} ")


@api_view(['POST'])
@permission_classes((permissions.AllowAny,))
def collect_vlans(request, ip):
    Inventory.collect_vlans(ip)
    return collect_response("VLANs of device {ip} ")

