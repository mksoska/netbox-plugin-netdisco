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
    

def collect_error(message):
    return HttpResponse(
        content=json.dumps({"error": message}),
        status=500,
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
    error_response = Inventory.notify()

    if not error_response:
        content = json.dumps({"notify": "Notification successfuly sent."})
        status = 200
    else:
        # TODO: Add better error message based on response content
        content = json.dumps({"notify": "Notification failed."})
        status = 500
    
    return HttpResponse(
        content=content,
        status=status,
        content_type='Accept: application/json'
    )


@api_view(['POST'])
@permission_classes((permissions.AllowAny,))
def device_collect(request):
    body = json.loads(request.body)
    ip = body.get("ip")
    update = body.get("update")

    if not ip:
        return collect_error("Missing device IP address.")

    if not update:
        return collect_error("Missing update type.")

    if update == "device":
        Inventory.collect_device(ip)
        Inventory.collect_device_ports(ip)
        Inventory.collect_device_addresses(ip)
        Inventory.collect_device_vlans(ip)
        return collect_response(f"Device {ip} ")
    
    if update == "macs":
        Inventory.collect_device_ports(ip)
        return collect_response(f"Ports MAC addresses of device {ip} ")

    if update == "ips":
        Inventory.collect_device_addresses(ip)
        return collect_response(f"Ports IP addresses of device {ip} ")

    return collect_error(f"Unknown update type {update}.")


