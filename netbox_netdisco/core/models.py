from .utilities import AttributeResolve, sum_inconsistent, merge_dicts, get_orm
from .netdisco import Netdisco
from .config import configuration, defaults

import dcim.models
import ipam.models
import openapi_netdisco.models

class CommonModel():
    def __init__(self, netdisco, netbox, attr_config):
        self.netdisco = netdisco
        self.netbox = netbox

        self.attrs = AttributeResolve(
            self.netdisco,
            self.netbox,
            attr_config.get("ATTRIBUTE_MAP", {}), 
            attr_config.get("ATTRIBUTE_VERBOSE", {}),
            attr_config.get("NETDISCO_ATTR_CONVERT", {}), 
            attr_config.get("NETBOX_ATTR_CONVERT", {})
        )

    @property
    def in_netbox(self):
        return self.netbox != None

    @property
    def is_consistent(self):
        for key in self.attrs.attribute_map:            
            if self.attrs.attr_consistent(key) == False:
                return False
        return True

    @property        
    def to_dict(self):
        return merge_dicts(self.netdisco.to_dict(), {"in_netbox": self.in_netbox, "is_consistent": self.is_consistent})



class Device(CommonModel):
    objects = {}

    attr_config = getattr(configuration, "DEVICE", getattr(defaults, "DEVICE"))

    def __init__(self, device_netdisco):        
        super().__init__(
            device_netdisco,
            get_orm(Device.attr_config.get("ORM_MAP"), device_netdisco, dcim.models.Device.objects),
            Device.attr_config
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
        return [Device.get(device.ip) for device in Netdisco.search.api_v1_search_device_get(**kwargs) if Device._is_searchmodel(device)]

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

    attr_config = getattr(configuration, "PORT", getattr(defaults, "PORT"))

    def __init__(self, port_netdisco):       
        super().__init__(
            port_netdisco,
            get_orm(Port.attr_config.get("ORM_MAP"), port_netdisco, dcim.models.Interface.objects),
            Port.attr_config
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

    attr_config = getattr(configuration, "ADDRESS", getattr(defaults, "ADDRESS"))
    
    def __init__(self, address_netdisco):               
        super().__init__(
            address_netdisco,
            get_orm(Address.attr_config.get("ORM_MAP"), address_netdisco, ipam.models.IPAddress.objects),
            Address.attr_config,
        )
        
        Address.objects.setdefault(address_netdisco.ip, {})[address_netdisco.alias] = self

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
    def all():
        return [addr for addr_dict in Address.objects.values() for addr in addr_dict.values()]

    @staticmethod
    def get(ip, alias):
        return Address.objects.get(ip, {}).get(alias)


class Vlan(CommonModel):
    objects = {}

    attr_config = getattr(configuration, "VLAN", getattr(defaults, "VLAN"))

    def __init__(self, vlan_netdisco): 
        super().__init__(
            vlan_netdisco,
            get_orm(Vlan.attr_config.get("ORM_MAP"), vlan_netdisco, ipam.models.VLAN.objects),
            Vlan.attr_config,
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
    