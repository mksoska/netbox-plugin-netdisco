from extras.plugins import PluginConfig  

class NetboxNetdiscoConfig(PluginConfig):
    name = 'netbox_netdisco'
    verbose_name = 'NetBox plugin for Netdisco integration'
    description = ('A plugin for comparing and synchronizing Netdisco device'
    'inventory with NetBox')
    version = '0.1'
    author = 'Marek Soska'
    author_email = 'mareksoska22@gmail.com'
    base_url = 'netbox-plugin-netdisco'
    required_settings = []
    default_settings = {}

config = NetboxNetdiscoConfig
