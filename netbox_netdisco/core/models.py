from .utilities import AttributeResolve, sum_inconsistent, merge_dicts, get_orm
from .netdisco import Netdisco

import dcim.models
import ipam.models
import openapi_netdisco.models

class CommonModel():
    def __init__(self, netdisco, netbox, attr_class):
        self.netdisco = netdisco
        self.netbox = netbox

        self.attrs = AttributeResolve(
            self.netdisco,
            self.netbox,
            attr_class.attribute_map, 
            attr_class.attribute_verbose,
            attr_class.netdisco_attr_convert, 
            attr_class.netbox_attr_convert
        )

    @property
    def in_netbox(self):
        return self.netbox != None

    @property
    def is_consistent(self):
        for key in self.attribute_map:            
            if self.attrs.attr_consistent(key) == False:
                return False
        return True

    @property        
    def to_dict(self):
        return merge_dicts(self.netdisco.to_dict(), {"in_netbox": self.in_netbox, "is_consistent": self.is_consistent})



class Device(CommonModel):
    objects = {}

    attribute_map = {
        "ip": "primary_ip4.address",
        "name": "name",
        "location": "location",
        "vendor": "device_type.manufacturer.name",
        "model": "device_type.model",
        "serial": "serial"                    
    }

    attribute_verbose = {
        "ip": "Management Address",
        "name": "System Hostname",
        "dns": "DNS",
        "location": "Location"
    }

    netdisco_attr_convert = {}

    netbox_attr_convert = {
        "ip": lambda x: str(x).split('/')[0]
    }

    def __init__(self, device_netdisco):
        device_netbox = dcim.models.Device.objects.filter(**{
            get_orm(self.attribute_map["ip"]): device_netdisco.ip + Address.get_primary_mask(device_netdisco.ip)
        }).first()
        
        super().__init__(
            device_netdisco,
            device_netbox,
            Device
        )        

        Device.objects[device_netdisco.ip] = self  

    @property
    def to_dict(self):
        return merge_dicts(super().to_dict, {
            "ports_inconsistent": sum_inconsistent(self.ports),
            "addresses_inconsistent": sum_inconsistent(self.addresses),
            "vlans_inconsistent": sum_inconsistent(self.vlans)
        })

    @property
    def ports(self):
        return Port.objects.get(self.netdisco.ip, {}).values()

    @property
    def addresses(self):
        return Address.objects.get(self.netdisco.ip, {}).values()

    @property
    def vlans(self):
        return Vlan.objects.get(self.netdisco.ip, {}).values()

    @staticmethod
    def _get(ip, **kwargs):
        device = Netdisco.objects.api_v1_object_device_ip_get(ip, **kwargs)
        if Device._is_getmodel(device):
            return Device(device, **kwargs)

    @staticmethod
    def _search(**kwargs):
        return [Device.objects.get(device.ip) for device in Netdisco.search.api_v1_search_device_get(**kwargs) if Device._is_searchmodel(device)]

    @staticmethod
    def _is_getmodel(instance):
        # Later add support for AsyncResult (maybe even HTTPResponse) returned from any get method of models #  
        return isinstance(instance, openapi_netdisco.models.Device)

    @staticmethod
    def _is_searchmodel(instance):
        return isinstance(instance, openapi_netdisco.models.DeviceSearch)

    @staticmethod
    def all():
        return Device.objects.values()

    @staticmethod
    def get(ip):
        return Device.objects.get(ip)
         

    
class Port(CommonModel):
    objects = {}

    attribute_map = {
        "ip": "device.primary_ip4.address",
        "remote_ip": "_path.destination.device.primary_ip4.address",
        "port": "name",
        "remote_port": "_path.destination.name",
        "desc": "description",
        "type": "type",
        "remote_type": "_path.destination.type",
        "mac": "mac_address",
        "mtu": "mtu",
        "pvid": "untagged_vlan_id",
        "up_admin": "enabled"            
    }

    attribute_verbose = {
        "ip": "Device",
        "remote_ip": "Neighbor Device",
        "desc": "Description",
        "mac": "Mac Address",
        "mtu": "MTU",
        "pvid": "Native VLAN",
        "up_admin": "Enabled"
    }

    netdisco_attr_convert = {
        "up": lambda x: x == "Up",
        "up_admin": lambda x: x == "Up"
    }

    netbox_attr_convert = {
        "ip": lambda x: str(x).split('/')[0]
    }

    def __init__(self, port_netdisco):
        port_netbox = dcim.models.Interface.objects.filter(**{
            get_orm(self.attribute_map["ip"]): port_netdisco.ip + Address.get_primary_mask(port_netdisco.ip),
            get_orm(self.attribute_map["port"]): port_netdisco.port
        }).first()

        super().__init__(
            port_netdisco,
            port_netbox,
            Port
        )

        Port.objects.setdefault(port_netdisco.ip, {})[port_netdisco.port] = self


    @staticmethod
    def _get(ip, port, **kwargs):
        port = Netdisco.objects.api_v1_object_device_ip_port_port_get(ip, port, **kwargs)
        if Port._is_getmodel(port):
            return Port(port) 

    @staticmethod
    def _get_ports(ip, **kwargs):
        return [Port(port) for port in Netdisco.objects.api_v1_object_device_ip_ports_get(ip, **kwargs) if Port._is_getmodel(port)]
    
    @staticmethod
    def _search(**kwargs):
        return [Port.get(port.ip, port.port) for port in Netdisco.search.api_v1_search_port_get(**kwargs) if Port._is_searchmodel(port)]
    
    @staticmethod
    def _is_getmodel(instance):
        return isinstance(instance, openapi_netdisco.models.Port)

    @staticmethod
    def _is_searchmodel(instance):
        return isinstance(instance, openapi_netdisco.models.PortSearch)

    @staticmethod
    def all():
        return [port for port_dict in Port.objects.values() for port in port_dict.values()]

    @staticmethod
    def get(ip, port):
        return Port.objects.get(ip, {}).get(port)
        


class Address(CommonModel):
    objects = {}

    attribute_map = {
        "ip": 'interface.get(name=self.netdisco.port).device.primary_ip4.address',
        "alias": "address",
        "subnet": "address",
        "port": "interface.name",
        "dns": "dns_name"            
    }

    attribute_verbose = {
        "ip": "Device",
        "alias": "IP Address",
        "subnet": "Mask"
    }

    netdisco_attr_convert = {}

    netbox_attr_convert = {
        "ip": lambda x: str(x).split('/')[0],
        "alias": lambda x: str(x).split('/')[0],
        "subnet": lambda x: str(x).split('/')[1]
    }

    def __init__(self, address_netdisco):
        address_netbox = ipam.models.IPAddress.objects.filter(**{
            get_orm(self.attribute_map["alias"]): address_netdisco.alias + '/' + address_netdisco.subnet.split('/')[1]
        }).first()

        super().__init__(
            address_netdisco,
            address_netbox,
            Address,
        )
        
        Address.objects.setdefault(address_netdisco.ip, {})[address_netdisco.alias] = self

    @property
    def mask(self):
        return '/' + self.netdisco.subnet.split('/')[1]

    @staticmethod
    def _get_addresses(ip, **kwargs):
        return [Address(address) for address in Netdisco.objects.api_v1_object_device_ip_device_ips_get(ip, **kwargs) if Address._is_getmodel(address)]         

    @staticmethod
    def _search(ip):
        return [address for address in Address.all() if ip in address.alias]

    @staticmethod
    def _is_getmodel(instance):
        return isinstance(instance, openapi_netdisco.models.Address)

    @staticmethod
    def get_primary_mask(ip):
        return getattr(Address.get(ip, ip), "mask", "")

    @staticmethod
    def all():
        return [addr for addr_dict in Address.objects.values() for addr in addr_dict.values()]

    @staticmethod
    def get(ip, alias):
        return Address.objects.get(ip, {}).get(alias)


class Vlan(CommonModel):
    objects = {}

    attribute_map = {
        "vlan": "vid",
        "description": "name"
    }

    attribute_verbose = {
        "ip": "Device",
        "vlan": "VLAN ID",
        "description": "Name"
    }

    netdisco_attr_convert = {}

    netbox_attr_convert = {
        "ip": lambda x: str(x).split('/')[0]
    }

    def __init__(self, vlan_netdisco):
        vlan_netbox = ipam.models.VLAN.objects.filter(**{
            get_orm(self.attribute_map["vlan"]): vlan_netdisco.vlan
        }).first()

        super().__init__(
            vlan_netdisco,
            vlan_netbox,
            Vlan,
        )

        Vlan.objects.setdefault(vlan_netdisco.ip, {})[vlan_netdisco.vlan] = self

    @staticmethod
    def _get_vlans(ip, **kwargs):
        return [Vlan(vlan) for vlan in Netdisco.objects.api_v1_object_device_ip_vlans_get(ip, **kwargs) if Vlan._is_getmodel(vlan)]

    @staticmethod
    def _search(**kwargs):
        return [Vlan.get(vlan.ip, vlan.vlan) for vlan in Netdisco.search.api_v1_search_vlan_get(**kwargs) if Vlan._is_searchmodel(vlan)]

    @staticmethod
    def _is_getmodel(instance):
        return isinstance(instance, openapi_netdisco.models.Vlan)

    @staticmethod
    def _is_searchmodel(instance):
        return isinstance(instance, openapi_netdisco.models.VlanSearch)

    @staticmethod
    def all():
        return [vlan for vlan_dict in Vlan.objects.values() for vlan in vlan_dict.values()]

    @staticmethod
    def get(ip, vlan):
        return Vlan.objects.get(ip, {}).get(vlan)
    