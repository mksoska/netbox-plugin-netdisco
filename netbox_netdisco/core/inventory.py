from .netdisco import Netdisco
from .monitoring import Icinga
from .models import *
from .utilities import sum_consistent
from netbox import settings


class Inventory():
    # Later add support for AsyncResult (maybe even HTTPResponse) returned from any get method of models

    @staticmethod
    def initialize(**kwargs):
        for portutilization in Netdisco.reports.api_v1_report_device_portutilization_get(**kwargs):
            Device._get(portutilization.ip, **kwargs)           
   
    @staticmethod 
    def clear_all():
        Device.objects.clear()
        Port.objects.clear()
        Address.objects.clear()
        Vlan.objects.clear()

    @staticmethod
    def collect(**kwargs):
        with Netdisco(settings.PLUGINS_CONFIG.get("netbox_netdisco")):
            Inventory.clear_all()
            Inventory.initialize(**kwargs)
    
            
    @staticmethod
    def notify():
        notification_modules = {
            "ICINGA2": Icinga
        }

        config = settings.PLUGINS_CONFIG.get("netbox_netdisco")
        for key in notification_modules:
            if config.get(key + "_HOST"):
                response = Inventory.notify_inconsistencies(notification_modules[key](config))
                if response.status_code != 200:
                    return response

    @staticmethod
    def notify_inconsistencies(monitoring):
        comment = f"Inconsistent devices: {sum_consistent(Device.objects.values(), False)}\n"\
            + f"Inconsistent ports: {sum_consistent(Port.objects.values(), False)}\n"\
            + f"Inconsistent IP addresses: {sum_consistent(Address.objects.values(), False)}\n"\
            + f"Inconsistent VLANs: {sum_consistent(Vlan.objects.values(), False)}"
        return monitoring.send(comment)
            
