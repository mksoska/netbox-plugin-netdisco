import django_tables2 as tables
from django.urls import reverse


def get_device_url(value):
    return reverse("plugins:netbox_netdisco:device", kwargs={"ip": value})

def get_device_ports_url(record):
    return reverse("plugins:netbox_netdisco:port_list", kwargs={"ip": record["ip"]})

class DeviceTable(tables.Table):
    ip = tables.Column(linkify=get_device_url)
    dns = tables.Column()   
    port_count = tables.Column(linkify=get_device_ports_url)
    ports_in_use = tables.Column()
    ports_shutdown = tables.Column()
    ports_inconsistent = tables.Column()
    ports_unknown = tables.Column()


    class Meta:
        attrs = {
            'class': 'table table-hover object-list',
        }
        row_attrs = {
            # Add handling if ip not present in record
            #"onClick": lambda record: "document.location.href='/device/{0}';".format(record["ip"])
        }


