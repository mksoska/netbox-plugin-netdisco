from extras.plugins import PluginMenuItem


menu_items = (
    PluginMenuItem(
        link="plugins:netbox_netdisco:device_list",
        link_text="Devices",
    ),
    PluginMenuItem(
        link="plugins:netbox_netdisco:port_list",
        link_text="Ports"
    ),
    PluginMenuItem(
        link="plugins:netbox_netdisco:address_list",
        link_text="IP Addresses"
    ),
    PluginMenuItem(
        link="plugins:netbox_netdisco:vlan_list",
        link_text="VLANs"
    )
)