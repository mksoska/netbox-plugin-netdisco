from .netdisco import Netdisco
from .monitoring import Icinga
from .models import *
from .utilities import sum_inconsistent
from netbox import settings


class Inventory():
    plugin_config = settings.PLUGINS_CONFIG.get("netbox_netdisco")

    device_set = "Netdisco.reports.api_v1_report_device_portutilization_get(**kwargs)"     

    @staticmethod
    def collect(**kwargs):
        Inventory.collect_devices(**kwargs)
        Inventory.collect_ports(**kwargs)
        Inventory.collect_addresses(**kwargs)
        Inventory.collect_vlans(**kwargs)

    @classmethod
    def collect_device(cls, ip, **kwargs):
        with Netdisco(cls.plugin_config):
            Device._get(ip, **kwargs)

    @classmethod
    def collect_devices(cls, **kwargs):
        Device.objects.clear()
        with Netdisco(cls.plugin_config):
            for device in eval(cls.device_set):
                Device._get(device.ip, **kwargs)

    @classmethod
    def collect_port(cls, ip, port, **kwargs): 
        with Netdisco(cls.plugin_config):
            Port._get(ip, port, **kwargs)
            

    @classmethod
    def collect_device_ports(cls, ip, **kwargs): 
        with Netdisco(cls.plugin_config):
            Port._get_ports(ip, **kwargs)

    @classmethod
    def collect_ports(cls, **kwargs):
        Port.objects.clear()
        with Netdisco(cls.plugin_config):
            for device in eval(cls.device_set):
                Port._get_ports(device.ip, **kwargs)

    @classmethod
    def collect_device_addresses(cls, ip, **kwargs):
        with Netdisco(cls.plugin_config):
            Address._get_addresses(ip, **kwargs)
            

    @classmethod
    def collect_addresses(cls, **kwargs):
        Address.objects.clear()
        with Netdisco(cls.plugin_config):
            for device in eval(cls.device_set):
                Address._get_addresses(device.ip, **kwargs)

    @classmethod
    def collect_device_vlans(cls, ip, **kwargs):
        with Netdisco(cls.plugin_config):
            Vlan._get_vlans(ip, **kwargs)

    @classmethod
    def collect_vlans(cls, **kwargs):
        Vlan.objects.clear()
        with Netdisco(cls.plugin_config):
            for device in eval(cls.device_set):
                Vlan._get_vlans(device.ip, **kwargs)
            
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
            
