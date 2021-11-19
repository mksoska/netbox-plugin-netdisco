from .models import *
from .netdisco import Netdisco

class Inventory():
    # Later add support for AsyncResult (maybe even HTTPResponse) returned from any get method of models

    @staticmethod
    def collect(**kwargs):
        Device.objects.clear()
        Port.objects.clear()
        Address.objects.clear()
        Vlan.objects.clear()

        with Netdisco() as _:
            Inventory._initialize_devices(**kwargs)
            

    #TODO: Make prettier (at least naming)
    @staticmethod
    def _initialize_devices(**kwargs): 
        for portutilization in Netdisco.reports.api_v1_report_device_portutilization_get(**kwargs):
            device = Device._get(portutilization.ip, **kwargs)
            if Device._is_apimodel(device):
                Device(device, **kwargs)

    #TODO: Find inconsistencies in inventory
    def compute():
        pass

    #TODO: Send inconsistencies notification to Icinga
    def notify():
        pass