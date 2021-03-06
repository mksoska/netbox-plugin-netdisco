from django.shortcuts import render
from django.views.generic import View
from netbox_netdisco.core.inventory import Inventory
from .core.models import *
from .tables import *
from django_tables2 import RequestConfig



def should_reload(state):
    return state == "reload"


class NetdiscoDeviceListView(View):
    """Display list of devices that are present in Netdisco."""
    
    def get(self, request):
        """Get device list."""

        if should_reload(request.GET.get("q")):
            Inventory.collect_devices()

        entryset = [device.to_dict for device in Device.all()]
        table = DeviceTable(entryset, order_by=("is_consistent, -ports_inconsistent", "-addresses_inconsistent", "-vlans_inconsistent"))
        table.paginate(page=request.GET.get("page", 1), per_page=25)

        return render(
            request, "netbox_netdisco/device_list.html", {"table": table}
        )


class NetdiscoDeviceSearchView(View):
    """Display list of searched devices that are present in Netdisco."""
    
    def get(self, request, search):
        """Get device list."""
        pass


class NetdiscoDeviceView(View):
    """Display Netdisco device details."""

    def get(self, request, ip):
        """Get device."""

        if should_reload(request.GET.get("q")):
            Inventory.collect_device(ip)

        device = Device.get(ip)        

        return render(
            request, "netbox_netdisco/device.html", {"device": device}
        )


class NetdiscoPortListView(View):
    """Display list of ports that are present in Netdisco."""

    def get(self, request):
        """Get port list.""" 

        if should_reload(request.GET.get("q")):
            Inventory.collect_ports()   

        entryset = [port.to_dict for port in Port.all()]
        table = PortTable(entryset, order_by="is_consistent")
        table.paginate(page=request.GET.get("page", 1), per_page=25)

        return render(
            request, "netbox_netdisco/port_list.html", {"table": table}
        )


class NetdiscoPortSearchView(View):
    """Display list of searched ports that are present in Netdisco."""
    
    def get(self, request, search):
        """Get port list."""
        pass

    
class NetdiscoDevicePortListView(View):
    """Display list of ports that are present in Netdisco."""

    def get(self, request, ip):
        """Get port list."""   

        if should_reload(request.GET.get("q")):
            Inventory.collect_device_ports(ip)

        device = Device.get(ip)
        entryset = [port.to_dict for port in device.ports]
        table = PortTable(entryset, order_by="is_consistent")
        RequestConfig(request, paginate={"per_page": 25}).configure(table)

        return render(
            request, "netbox_netdisco/port_list.html", {"device": device, "table": table}
        )


class NetdiscoPortView(View):
    """Display Netdisco port details."""
    
    def get(self, request, ip, port):
        """Get port."""

        if should_reload(request.GET.get("q")):
            Inventory.collect_port(ip, port)

        port = Port.get(ip, port)

        return render(
            request, "netbox_netdisco/port.html", {"port": port}
        )


class NetdiscoAddressListView(View):
    """Display list of addresses that are present in Netdisco."""

    def get(self, request):
        """Get address list."""

        if should_reload(request.GET.get("q")):
            Inventory.collect_addresses()

        entryset = [address.to_dict for address in Address.all()]
        table = AddressTable(entryset, order_by="is_consistent")
        RequestConfig(request, paginate={"per_page": 25}).configure(table)

        return render(
            request, "netbox_netdisco/address_list.html", {"table": table}
        )


class NetdiscoAddressSearchView(View):
    """Display list of searched addresses that are present in Netdisco."""
    
    def get(self, request, search):
        """Get address list."""
        pass


class NetdiscoDeviceAddressListView(View):
    """Display list of addresses that belong to a device in Netdisco."""

    def get(self, request, ip):
        """Get address list."""

        if should_reload(request.GET.get("q")):
            Inventory.collect_device_addresses(ip)

        device = Device.get(ip)
        entryset = [address.to_dict for address in device.addresses]
        table = AddressTable(entryset, order_by="is_consistent")
        RequestConfig(request, paginate={"per_page": 25}).configure(table)

        return render(
            request, "netbox_netdisco/address_list.html", {"device": device, "table": table}
        )


class NetdiscoAddressView(View):
    """Display Netdisco IP address details."""

    def get(self, request, ip, alias):
        """Get address."""

        if should_reload(request.GET.get("q")):
            Inventory.collect_device_addresses(ip)

        address = Address.get(ip, alias)

        return render(
            request, "netbox_netdisco/address.html", {"address": address}
        )


class NetdiscoVlanListView(View):
    """Display list of VLANs that are present in Netdisco."""

    def get(self, request):
        """Get VLAN list."""

        if should_reload(request.GET.get("q")):
            Inventory.collect_vlans()

        entryset = [vlan.to_dict for vlan in Vlan.all()]
        table = VlanTable(entryset, order_by="is_consistent")
        RequestConfig(request, paginate={"per_page": 25}).configure(table)

        return render(
            request, "netbox_netdisco/vlan_list.html", {"table": table}
        )


class NetdiscoVlanSearchView(View):
    """Display list of searched VLANs that are present in Netdisco."""
    
    def get(self, request, search):
        """Get VLAN list."""
        pass


class NetdiscoDeviceVlanListView(View):
    """Display list of VLANs that belong to a device in Netdisco."""

    def get(self, request, ip):
        """Get VLAN list."""

        if should_reload(request.GET.get("q")):
            Inventory.collect_device_vlans(ip)

        device = Device.get(ip)
        entryset = [vlan.to_dict for vlan in device.vlans]
        table = VlanTable(entryset, order_by="is_consistent")
        RequestConfig(request, paginate={"per_page": 25}).configure(table)

        return render(
            request, "netbox_netdisco/vlan_list.html", {"device": device, "table": table}
        )


class NetdiscoVlanView(View):
    """Display Netdisco VLAN details."""

    def get(self, request, ip, id):
        """Get VLAN."""

        if should_reload(request.GET.get("q")):
            Inventory.collect_device_vlans(ip)

        vlan = Vlan.get(ip, id)

        return render(
            request, "netbox_netdisco/vlan.html", {"vlan": vlan}
        )
