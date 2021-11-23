from .utilities import sum_consistent, AttributeMap, merge_dicts
from .netdisco import Netdisco

import dcim.models
import ipam.models
import openapi_netdisco.models

class CommonModel():
    def __init__(self, netdisco, netbox, attribute_map, attribute_tag, attribute_value_map):
        self.netdisco = netdisco
        self.netbox = netbox
        self.attribute_map = attribute_map
        self.attribute_tag = attribute_tag
        self.attribute_value_map = attribute_value_map

    
    @property
    def is_consistent(self):
        if not self.netbox:
            return
        for key in self.attribute_map:            
            if self.getattr_netdisco(key) != self.getattr_netbox(key):
                return False
        return True

    def getattr_netdisco(self, key):
        value_map = self.attribute_value_map.get(key, lambda x: x)        
        return value_map(getattr(self.netdisco, key, None)) 

    def getattr_netbox(self, key):           
        result = self.netbox
        for attr in self.attribute_map[key].split('__'):
            if not result:
                return
            result = getattr(result, attr, None)
        return result

    @property        
    def to_dict(self):
        return self.netdisco.to_dict()



class Device(CommonModel):
    objects = {}

    def __init__(self, device, **kwargs):
        attribute_map = AttributeMap({
            "ip": "primary_ip4__address",
            "name": "name",
            "location": "location",
            "vendor": "device_type__manufacturer__name",
            "model": "device_type__model",
            "serial": "serial"                    
        }, device)

        attribute_tag = {
            "ip": "Management Address",
            "name": "System Name",
            "dns": "DNS",
            "location": "Location"
        }

        attribute_value_map = {}
        
        super().__init__(
            device,
            dcim.models.Device.objects.filter(**attribute_map("ip")).first(),
            attribute_map.map_,
            attribute_tag,
            attribute_value_map
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

    def __init__(self, device, port):
        attribute_map = AttributeMap({
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
        }, port)

        attribute_tag = {
            "ip": "Device",
            "remote_ip": "Neighbor Device",
            "desc": "Description",
            "mac": "Mac Address",
            "mtu": "MTU",
            "pvid": "Native VLAN",
            "up_admin": "Enabled"
        }

        attribute_value_map = {
            "up": lambda x: x == "Up",
            "up_admin": lambda x: x == "Up"
        }
        
        super().__init__(
            port,
            dcim.models.Interface.objects.filter(**attribute_map("ip", "port")).first(),
            attribute_map.map_,
            attribute_tag,
            attribute_value_map
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

    def __init__(self, device, address):
        attribute_map = AttributeMap({
            "ip": "interface__device__primary_ip4__address",
            "alias": "address",
            "port": "interface__name",
            "dns": "dns_name"            
        }, address)

        attribute_tag = {
            "ip": "Device",
            "alias": "IP Address",
        }

        attribute_value_map = {}

        super().__init__(
            address,
            ipam.models.IPAddress.objects.filter(**attribute_map("alias")).first(),
            attribute_map.map_,
            attribute_tag,
            attribute_value_map
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

    def __init__(self, device, vlan):
        attribute_map = AttributeMap({
            "vlan": "vid",
            "description": "name"
        }, vlan)

        attribute_tag = {
            "ip": "Device",
            "vlan": "VLAN ID",
            "description": "Name"
        }

        attribute_value_map = {}

        super().__init__(
            vlan,
            ipam.models.VLAN.objects.filter(**attribute_map("vlan")).first(),
            attribute_map.map_,
            attribute_tag,
            attribute_value_map
        )

        self.device = device
        Vlan.objects[f"{vlan.ip}_{vlan.vlan}"] = self

    @staticmethod
    def _get_vlans(ip, **kwargs):
        return Netdisco.objects.api_v1_object_device_ip_vlans_get(ip, **kwargs)

    @staticmethod
    def _is_apimodel(instance):
        return isinstance(instance, openapi_netdisco.models.Vlan)
    