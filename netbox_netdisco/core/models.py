from .utilities import is_consistent
from .netdisco import Netdisco

#import dcim.models
import openapi_netdisco.models


class CommonModel():
    def __init__(self, netdisco, netbox, attribute_map):
        self.netdisco = netdisco
        self.netbox = netbox
        self.attribute_map = attribute_map
    
    @property
    def is_consistent(self):
        if self.netbox:           
            return is_consistent(self)

    def to_dict(self):
        return self.netdisco.to_dict()



class Device(CommonModel):
    objects = {}

    def __init__(self, device, **kwargs):
        attribute_map = {
            "ip": "primary_ip4__address",

            "name": "name"
        }

        #dcim.models.Device.objects.filter(**{self.attribute_map["ip"]: ip}).first()
        super().__init__(device, None, attribute_map)
        
        self.ports = [Port(self, port) for port in Port._get_ports(device.ip, **kwargs) if Port._is_apimodel(port)]
        self.addresses = [Address(self, address) for address in Address._get_addresses(device.ip, **kwargs) if Address._is_apimodel(address)]
        self.vlans = [Vlan(self, vlan) for vlan in Vlan._get_vlans(device.ip, **kwargs) if Vlan._is_apimodel(vlan)]

        Device.objects[device.ip] = self

    @staticmethod
    def _get(ip, **kwargs):
        return Netdisco.objects.api_v1_object_device_ip_get(ip, **kwargs)

    @staticmethod
    def _is_apimodel(instance):
        return isinstance(instance, openapi_netdisco.models.Device)


    
class Port(CommonModel):
    objects = {}

    def __init__(self, device, port):
        attribute_map = {
            "ip": "device__primary_ip4__address",
            "port": "name" # or maybe "name": "name"
        }

        #dcim.models.Interface.objects.filter(**{attribute_map["ip"]: ip, attribute_map["name"]: name}).first()
        super().__init__(port, None, attribute_map)

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
        attribute_map = {
            "alias": "address"
        }

        #ipam.models.IPAddress.objects.filter(**{attribute_map["alias"]: alias}).first()
        super().__init__(address, None, attribute_map)

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
        attribute_map = {
            "vlan": "vid"
        }

        #ipam.models.VLAN.objects.filter(**{attribute_map["vlan"]: vlan})
        super().__init__(vlan, None, attribute_map)

        self.device = device
        Vlan.objects[f"{vlan.ip}_{vlan.vlan}"] = self

    @staticmethod
    def _get_vlans(ip, **kwargs):
        return Netdisco.objects.api_v1_object_device_ip_vlans_get(ip, **kwargs)

    @staticmethod
    def _is_apimodel(instance):
        return isinstance(instance, openapi_netdisco.models.Vlan)
    