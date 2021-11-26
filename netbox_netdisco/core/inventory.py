from .netdisco import Netdisco
from .monitoring import Icinga
from .models import *
from .utilities import sum_inconsistent
from netbox import settings


class Inventory():      
   
    @staticmethod
    def clear_all():
        Device.objects.clear()
        Port.objects.clear()
        Address.objects.clear()
        Vlan.objects.clear()

    @staticmethod
    def collect(**kwargs):
        Inventory.clear_all()
        Inventory.collect_devices(**kwargs)
        for device in Device.all():
            Inventory.collect_addresses(device.netdisco.ip, **kwargs)
            Inventory.collect_ports(device.netdisco.ip, **kwargs)
            Inventory.collect_vlans(device.netdisco.ip, **kwargs)

    @staticmethod
    def collect_device(ip, **kwargs):
        with Netdisco(settings.PLUGINS_CONFIG.get("netbox_netdisco")):
            Device._get(ip, **kwargs)

    @staticmethod
    def collect_devices(**kwargs):
         with Netdisco(settings.PLUGINS_CONFIG.get("netbox_netdisco")):
            for portutilization in Netdisco.reports.api_v1_report_device_portutilization_get(**kwargs):
                Device._get(portutilization.ip, **kwargs)

    @staticmethod
    def collect_port(ip, port, **kwargs): 
        with Netdisco(settings.PLUGINS_CONFIG.get("netbox_netdisco")):
            Port._get(ip, port, **kwargs)

    @staticmethod
    def collect_ports(ip, **kwargs):
        with Netdisco(settings.PLUGINS_CONFIG.get("netbox_netdisco")):
            Port._get_ports(ip, **kwargs)

    @staticmethod
    def collect_addresses(ip, **kwargs):
        with Netdisco(settings.PLUGINS_CONFIG.get("netbox_netdisco")):
            Address._get_addresses(ip, **kwargs)

    @staticmethod
    def collect_vlans(ip, **kwargs):
        with Netdisco(settings.PLUGINS_CONFIG.get("netbox_netdisco")):
            Vlan._get_vlans(ip, **kwargs)
            
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
        comment = f"Inconsistent devices: {sum_inconsistent(Device.all())}\n"\
            + f"Inconsistent ports: {sum_inconsistent(Port.all())}\n"\
            + f"Inconsistent IP addresses: {sum_inconsistent(Address.all())}\n"\
            + f"Inconsistent VLANs: {sum_inconsistent(Vlan.all())}"
        return monitoring.send(comment)
            
