import django_tables2 as tables
from django.urls import reverse


def device_url(record):
    return reverse("plugins:netbox_netdisco:device", kwargs={"ip": record["ip"]})


def port_url(record):
    port = record["port"]
    if "@" in port:
        port = port.split("@")[1]
    return reverse("plugins:netbox_netdisco:port", kwargs={"port": port, "ip": record["ip"]})


def port_list_url(record):
    return reverse("plugins:netbox_netdisco:device_port_list", kwargs={"ip": record["ip"]})


def address_url(value):
    return reverse("plugins:netbox_netdisco:address", kwargs={"ip": value})


def address_list_url(record):
    return reverse("plugins:netbox_netdisco:device_address_list", kwargs={"ip": record["ip"]})


def vlan_url(record):
    return reverse("plugins:netbox_netdisco:vlan", kwargs={"id": record["vlan"], "ip": record["ip"]})


def vlan_list_url(record):
    return reverse("plugins:netbox_netdisco:device_vlan_list", kwargs={"ip": record["ip"]})


consistency_color = {
    "td": {
        "class": lambda value: "text-danger" if not value else "text-success"
    }
}

class DeviceTable(tables.Table):
    name = tables.Column(linkify=device_url, verbose_name="Device")
    location = tables.Column()
    ip = tables.Column(linkify=address_url, verbose_name="Management IP")
    dns = tables.Column(verbose_name="DNS")
    model = tables.Column()
    os = tables.Column(verbose_name="OS")
    serial = tables.Column()
    last_discover = tables.Column(verbose_name="Last Discovered")
    is_consistent = tables.Column(attrs=consistency_color)
    ports_inconsistent = tables.Column(linkify=port_list_url, verbose_name="Ports Inconsistent")
    addresses_inconsistent = tables.Column(linkify=address_list_url, verbose_name="IP Addresses Inconsistent")
    vlans_inconsistent = tables.Column(linkify=vlan_list_url, verbose_name="VLANs Inconsistent")

    class Meta:
        attrs = {
            'class': 'table table-hover object-list',
        }
        row_attrs = {
            'class': lambda record: "border-danger" if not record["is_consistent"] else ""
        } 


class PortTable(tables.Table):
    up = tables.Column()
    port = tables.Column(linkify=port_url)
    ip = tables.Column(linkify=device_url, verbose_name="Device")
    vlan = tables.Column(linkify=vlan_url, verbose_name="VLAN")
    speed = tables.Column()
    is_consistent = tables.Column(attrs=consistency_color)

    class Meta:
        attrs = {
            'class': 'table table-hover object-list',
        }
        row_attrs = {
            'class': lambda record: "border-danger" if not record["is_consistent"] else ""
        }


class AddressTable(tables.Table):
    alias = tables.Column(linkify=address_url, verbose_name="IP Address")
    subnet = tables.Column()
    ip = tables.Column(linkify=device_url, verbose_name="Device")
    port = tables.Column(linkify=port_url)
    dns = tables.Column(verbose_name="DNS")
    is_consistent = tables.Column(attrs=consistency_color)

    class Meta:
        attrs = {
            'class': 'table table-hover object-list',
        }   
        row_attrs = {
            'class': lambda record: "border-danger" if not record["is_consistent"] else ""
        }     


class VlanTable(tables.Table):
    vlan = tables.Column(verbose_name="VLAN ID")
    ip = tables.Column(linkify=device_url, verbose_name="Device")
    description = tables.Column()
    is_consistent = tables.Column(attrs=consistency_color)

    class Meta:
        attrs = {
            'class': 'table table-hover object-list',
        } 
        row_attrs = {
            'class': lambda record: "border-danger" if not record["is_consistent"] else ""
        }       


