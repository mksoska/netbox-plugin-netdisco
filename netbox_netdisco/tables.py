import django_tables2 as tables
from netbox_netdisco.core import *

device_list = ""
data = [device.to_dict() for device in device_list]

class NameTable(tables.Table):
    ip = tables.Column()
    name = tables.Column()


    class Meta:
        attrs = {
            'class': 'table table-hover object-list',
        }
        row_attrs = {
            "onClick": lambda record: "document.location.href='/device/{0}';".format(record.ip)
        }

table = NameTable(data)

 