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
    response = Inventory.notify()
    
    return HttpResponse(
        content=json.dumps({"notify": "Notification successfuly sent."}),
        status=200,
        content_type=response.headers['Content-Type']
    ) if response.status_code == 200 else HttpResponse(
        # TODO: Add better error message based on response content
        content=json.dumps({"notify": "Notification failed."}),
        status=500,
        content_type=response.headers['Content-Type']
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



# @api_view(['POST'])
# @permission_classes((permissions.AllowAny,))
# def collect_devices(request):
#     Inventory.collect_devices()
#     return collect_response("Devices ")

# @api_view(['POST'])
# @permission_classes((permissions.AllowAny,))
# def collect_ports(request):
#     Inventory.collect_ports()
#     return collect_response("Ports ")

# @api_view(['POST'])
# @permission_classes((permissions.AllowAny,))
# def collect_device_ports(request, ip):
#     Inventory.collect_device_ports(ip)
#     return collect_response("Ports of device {ip} ")


# @api_view(['POST'])
# @permission_classes((permissions.AllowAny,))
# def collect_port(request, ip, port):
#     Inventory.collect_port(ip, port)
#     return collect_response("Port {port} of device {ip} ")


# @api_view(['POST'])
# @permission_classes((permissions.AllowAny,))
# def collect_addresses(request):
#     Inventory.collect_addresses()
#     return collect_response("IP addresses ")


# @api_view(['POST'])
# @permission_classes((permissions.AllowAny,))
# def collect_device_addresses(request, ip):
#     Inventory.collect_device_addresses(ip)
#     return collect_response("IP addresses of device {ip} ")


# @api_view(['POST'])
# @permission_classes((permissions.AllowAny,))
# def collect_vlans(request):
#     Inventory.collect_vlans()
#     return collect_response("VLANs of device {ip} ")

# @api_view(['POST'])
# @permission_classes((permissions.AllowAny,))
# def collect_device_vlans(request, ip):
#     Inventory.collect_device_vlans(ip)
#     return collect_response("VLANs of device {ip} ")

