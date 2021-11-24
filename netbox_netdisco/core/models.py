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
        
        self.ports = Port._get_ports(self, **kwargs)
        self.addresses = Address._get_addresses(self, **kwargs)
        self.vlans = Vlan._get_vlans(self, **kwargs)

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
        device = Netdisco.objects.api_v1_object_device_ip_get(ip, **kwargs)
        if Device._is_getmodel(device):
            return Device(device, **kwargs)

    @staticmethod
    def _search(**kwargs):
        return [Device.objects.get(device.ip) for device in Netdisco.search.api_v1_search_device_get(**kwargs) if Device._is_searchmodel(device)]

    @staticmethod
    def _is_getmodel(instance):
        return isinstance(instance, openapi_netdisco.models.Device)

    @staticmethod
    def _is_searchmodel(instance):
        return isinstance(instance, openapi_netdisco.models.DeviceSearch)


         

    
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
    def _get_ports(device, **kwargs):
        return [Port(device, port) for port in Netdisco.objects.api_v1_object_device_ip_ports_get(device.netdisco.ip, **kwargs) if Port._is_getmodel(port)]
    
    @staticmethod
    def _search(**kwargs):
        return [Port.objects.get(f"{port.ip}_{port.port}") for port in Netdisco.search.api_v1_search_port_get(**kwargs) if Port._is_searchmodel(port)]
    
    @staticmethod
    def _is_getmodel(instance):
        return isinstance(instance, openapi_netdisco.models.Port)

    @staticmethod
    def _is_searchmodel(instance):
        return isinstance(instance, openapi_netdisco.models.PortSearch)
        


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
    def _get_addresses(device, **kwargs):
        return [Address(device, address) for address in Netdisco.objects.api_v1_object_device_ip_device_ips_get(device.netdisco.ip, **kwargs) if Address._is_getmodel(address)]         

    @staticmethod
    def _search(ip):
        return [address for address in Address.objects.values() if ip in address.netdisco.alias]

    @staticmethod
    def _is_getmodel(instance):
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
    def _get_vlans(device, **kwargs):
        return [Vlan(device, vlan) for vlan in Netdisco.objects.api_v1_object_device_ip_vlans_get(device.netdisco.ip, **kwargs) if Vlan._is_getmodel(vlan)]

    @staticmethod
    def _search(**kwargs):
        return [Vlan.objects.get(f"{vlan.ip}_{vlan.vlan}") for vlan in Netdisco.search.api_v1_search_vlan_get(**kwargs) if Vlan._is_searchmodel(vlan)]

    @staticmethod
    def _is_getmodel(instance):
        return isinstance(instance, openapi_netdisco.models.Vlan)

    @staticmethod
    def _is_searchmodel(instance):
        return isinstance(instance, openapi_netdisco.models.VlanSearch)
    