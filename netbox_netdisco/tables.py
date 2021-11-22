import django_tables2 as tables
from django.urls import reverse


def get_device_url(value):
    return reverse("plugins:netbox_netdisco:device", kwargs={"ip": value})


#TODO
class DeviceTable(tables.Table):
    ip = tables.Column(linkify=get_device_url)
    dns = tables.Column()

    class Meta:
        attrs = {
            'class': 'table table-hover object-list',
        }
        row_attrs = {
            # Add handling if ip not present in record
            #"onClick": lambda record: "document.location.href='/device/{0}';".format(record["ip"])
        }

#TODO
class PortTable(tables.Table):
    ip = tables.Column(linkify=get_device_url)
    port = tables.Column()

    class Meta:
        attrs = {
            'class': 'table table-hover object-list',
        }

#TODO
class AddressTable(tables.Table):
    ip = tables.Column(linkify=get_device_url)
    alias = tables.Column()

    class Meta:
        attrs = {
            'class': 'table table-hover object-list',
        }


#TODO
class VlanTable(tables.Table):
    ip = tables.Column(linkify=get_device_url)
    vlan = tables.Column(verbose_name="VLAN ID")

    class Meta:
        attrs = {
            'class': 'table table-hover object-list',
        }


