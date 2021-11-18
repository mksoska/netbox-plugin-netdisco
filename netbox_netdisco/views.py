from django.shortcuts import render
from django.views.generic import View
from .core.models import PortUtilization, Device
from .tables import DeviceTable
from django_tables2 import RequestConfig


class NetdiscoDeviceListView(View):
    """Display list of devices that are present in Netdisco."""
    
    queryset = [device.to_dict() for device in PortUtilization.get()]

    def get(self, request):
        "Get device list."
        table = DeviceTable(self.queryset, order_by="-ports_inconsistent")
        RequestConfig(request, paginate={"per_page": 25}).configure(table)

        return render(
            request, "netbox_netdisco/device_list.html", {"table": table}
        )


class NetdiscoDeviceView(View):
    """Display Netdisco device details."""

    def get(self, request, ip):
        """Get device."""
        device = Device.get(ip)

        return render(
            request, "netbox_netdisco/device.html", {"device": device}
        )


class NetdiscoPortListView(View):
    """Display list of ports that belong to a device in Netdisco."""
    
    queryset = "queryset"


class NetdiscoPortView(View):
    """Display Netdisco port details."""
    
    queryset = "queryset"
