from .utilities import AttributeResolve, sum_consistent, merge_dicts, get_filter
from .netdisco import Netdisco

import dcim.models
import ipam.models
import openapi_netdisco.models

class CommonModel():
    def __init__(self, netdisco, netbox_objects, netbox_keys, attr_class):
        self.netdisco = netdisco
        self.netbox = netbox_objects.filter(**get_filter(netdisco, attr_class.attribute_map, *netbox_keys)).first()

        self.attrs = AttributeResolve(
            self.netdisco,
            self.netbox,
            attr_class.attribute_map, 
            attr_class.attribute_verbose, 
            attr_class.attribute_convert
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
        return self.netdisco.to_dict()



class Device(CommonModel):
    objects = {}

    attribute_map = {
        "ip": "primary_ip4__address",
        "name": "name",
        "location": "location",
        "vendor": "device_type__manufacturer__name",
        "model": "device_type__model",
        "serial": "serial"                    
    }

    attribute_verbose = {
        "ip": "Management Address",
        "name": "System Name",
        "dns": "DNS",
        "location": "Location"
    }

    attribute_convert = {}

    def __init__(self, device, **kwargs):        
        super().__init__(
            device,
            dcim.models.Device.objects, ("ip",),
            Device
        )
        
        self.ports = [Port(self, port) for port in Port._get_ports(device.ip, **kwargs) if Port._is_apimodel(port)]
        self.addresses = [Address(self, address) for address in Address._get_addresses(device.ip, **kwargs) if Address._is_apimodel(address)]
        self.vlans = [Vlan(self, vlan) for vlan in Vlan._get_vlans(device.ip, **kwargs) if Vlan._is_apimodel(vlan)]

        Device.objects[device.ip] = self  

    @property
    def to_dict(self):
        return merge_dicts(super().to_dict, {
            "ports_inconsistent": sum_consistent(self.ports, False),
            "addresses_inconsistent": sum_consistent(self.addresses, False),
            "vlans_inconsistent": sum_consistent(self.vlans, False)
        })

    @staticmethod
    def _get(ip, **kwargs):
        return Netdisco.objects.api_v1_object_device_ip_get(ip, **kwargs)

    @staticmethod
    def _is_apimodel(instance):
        return isinstance(instance, openapi_netdisco.models.Device)
         

    
class Port(CommonModel):
    objects = {}

    attribute_map = {
        "ip": "device__primary_ip4__address",
        "remote_ip": "_path__destination__device__primary_ip4__address",
        "port": "name",
        "remote_port": "_path__destination__name",
        "desc": "description",
        "type": "type",
        "remote_type": "_path__destination__type",
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

    attribute_convert = {
        "up": lambda x: x == "Up",
        "up_admin": lambda x: x == "Up"
    }

    def __init__(self, device, port):
        super().__init__(
            port,
            dcim.models.Interface.objects, ("ip", "port"),
            Port
        )

        self.device = device
        Port.objects[f"{port.ip}_{port.port}"] = self

    @staticmethod
    def _get_ports(ip, **kwargs):
        return Netdisco.objects.api_v1_object_device_ip_ports_get(ip, **kwargs)
    
    @staticmethod
    def _is_apimodel(instance):
        return isinstance(instance, openapi_netdisco.models.Port)
        


class Address(CommonModel):
    objects = {}

    attribute_map = {
        "ip": "interface__device__primary_ip4__address",
        "alias": "address",
        "port": "interface__name",
        "dns": "dns_name"            
    }

    attribute_verbose = {
            "ip": "Device",
            "alias": "IP Address",
    }

    attribute_convert = {}

    def __init__(self, device, address):
        super().__init__(
            address,
            ipam.models.IPAddress.objects, ("alias",),
            Address,
        )

        self.device = device
        Address.objects[address.alias] = self

    @staticmethod
    def _get_addresses(ip, **kwargs):
        return Netdisco.objects.api_v1_object_device_ip_device_ips_get(ip, **kwargs)
    
    @staticmethod
    def _is_apimodel(instance):
        return isinstance(instance, openapi_netdisco.models.Address)



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

    attribute_convert = {}

    def __init__(self, device, vlan):
        super().__init__(
            vlan,
            ipam.models.VLAN.objects, ("vlan",),
            Vlan,
        )

        self.device = device
        Vlan.objects[f"{vlan.ip}_{vlan.vlan}"] = self

    @staticmethod
    def _get_vlans(ip, **kwargs):
        return Netdisco.objects.api_v1_object_device_ip_vlans_get(ip, **kwargs)

    @staticmethod
    def _is_apimodel(instance):
        return isinstance(instance, openapi_netdisco.models.Vlan)
    