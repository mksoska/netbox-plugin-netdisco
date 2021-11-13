from openapi_netdisco.models import port
from .utilities import cast, list_cast
from .netdisco import Netdisco
from openapi_netdisco import models
import dcim.models

class Device(models.Device):   
    def __new__(cls, model):
        return cast(cls, super(), model)

    def __init__(self, _):
        #Handle with try catch
        self.netbox = dcim.models.Device.objects.get(primary_ip4__address=self.ip)
        self.ports = self.ports_get()   
        
    @classmethod
    def get(cls, ip, **kwargs):
        return cls(Netdisco.objects.api_v1_object_device_ip_get(ip, **kwargs))

    @classmethod
    def search(cls, **kwargs):
        return list_cast(cls, Netdisco.search.api_v1_search_device_get(**kwargs))

    def ports_get(self, **kwargs):
        return list_cast(Port, Netdisco.objects.api_v1_object_device_ip_ports_get(self.ip, **kwargs))

    #TODO
    def ports_search(self, partial=True, **kwargs):
        return [port for port in self.ports if port.attribute_map]
    
    #TODO
    @property
    def is_consistent(self):
        pass



class Port(models.Port):
    def __new__(cls, model):
        return cast(cls, super(), model)

    def __init__(self, _):
        #Handle with try catch
        self.netbox = dcim.models.Interface.objects.get(name=self.name)

    @classmethod
    def get(cls, ip, port, **kwargs):
        return cls(Netdisco.objects.api_v1_object_device_ip_port_port_get(ip, port, **kwargs))  
    
    @classmethod
    def search(cls, **kwargs):
        return list_cast(cls, Netdisco.search.api_v1_search_port_get(**kwargs))
    
    #TODO
    @property
    def is_consistent(self):
        pass


class PortUtilization(models.PortUtilization):
    def __new__(cls, model):
        return cast(cls, super(), model)
    
    def __init__(self, _):
        self.device = Device.get(self.ip)

    @classmethod
    def get(cls, **kwargs):
        return list_cast(cls, Netdisco.reports.api_v1_report_device_portutilization_get(**kwargs))
        #return cast(cls, Netdisco.reports.api_v1_report_device_portutilization_get(**kwargs))  

    