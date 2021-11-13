from django.shortcuts import render
from django.views.generic import View


class NetdiscoDeviceListView(View):
    """Display list of devices that are present in Netdisco."""
    
    queryset = "queryset"


class NetdiscoDeviceView(View):
    """Display Netdisco device details."""

    queryset = "queryset"

    def get(self, request, ip):
        """Get device."""
        device = "device"

        return render(request, "netbox_netdisco/device.html", {
            "device": device,
        })
