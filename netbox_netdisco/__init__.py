from extras.plugins import PluginConfig
from .core import Inventory

"""
Temporary for development purposes 
(because of using setup.py debug mode, hence not installing this plugin)
"""
########################################################
from django.conf import settings
settings.configure(INSTALLED_APPS=('my_app',))
########################################################

class NetboxNetdiscoConfig(PluginConfig):
    name = 'netbox_netdisco'
    verbose_name = 'Netdisco'
    description = ('A plugin for comparing and synchronizing Netdisco device'
    'inventory with NetBox')
    version = '0.1'
    author = 'Marek Soska'
    author_email = 'mareksoska22@gmail.com'
    base_url = 'netbox-plugin-netdisco'
    required_settings = ["NETDISCO_HOST", "NETDISCO_USERNAME", "NETDISCO_PASSWORD"]
    default_settings = {"NETDISCO_HOST": "http://localhost:8000"}

config = NetboxNetdiscoConfig
Inventory.collect()



