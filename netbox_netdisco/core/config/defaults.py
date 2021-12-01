DEVICE = {
    "ORM_MAP": {
        "ip": "primary_ip4__address__contains"
    },

    #mangling supported  

    "NETBOX_ATTR": {
        "vendor": lambda x: x.device_type.manufacturer.name,
        "model": lambda x: x.device_type.model,
    },

    "VERBOSE_ATTR": {
        "ip": "Management Address",
        "name": "System Hostname",
        "dns": "DNS",
        "location": "Location"
    },

    "CONSISTENCY_TABLE": ["name", "location", "vendor", "model", "serial"],   
}


PORT = {
    "ORM_MAP": {
        "ip": "device__primary_ip4__address__contains",
        "port": "name"
    },

    #mangling supported

    "NETDISCO_ATTR": {
        "up": lambda x: x == "Up",
        "up_admin": lambda x: x == "Up"
    },

    "NETBOX_ATTR": {
        "remote_ip": lambda x: str(x._path.destination.device.primary_ip4.address).split('/')[0],
        "remote_name": lambda x: x._path.destination.device.name,
        "remote_port": lambda x: x._path.destination.name,
        "remote_type": lambda x: x._path.destination.type,
        "desc": lambda x: x.description,
        "mac": lambda x: x.mac_address,
        "pvid": lambda x: str(x.untagged_vlan_id),
        "up_admin": lambda x: str(x.enabled)
    },

    "VERBOSE_ATTR": {
        "ip": "Device",
        "remote_ip": "Neighbor Device IP",
        "remote_name": "Neighbor Device Name",
        "desc": "Description",
        "mac": "Mac Address",
        "mtu": "MTU",
        "pvid": "Native VLAN",
        "up_admin": "Enabled"
    },

    "IGNORE_ATTR": ["remote_name"],

    "CONSISTENCY_TABLE": ["remote_ip", "remote_name", "remote_port",  "remote_type", "desc", "type", "mac", "mtu",  "pvid", "up_admin"]
}


ADDRESS = {
    "ORM_MAP": {
        "alias": "address__contains",
    },

    #mangling supported

    "NETDISCO_ATTR": {
        "mask": lambda x: '/' + x.subnet.split('/')[1]
    },

    "NETBOX_ATTR": {
        "ip": lambda x: str(x.interface.first().device.primary_ip4.address).split('/')[0],
        "mask": lambda x: '/' + str(x.address).split('/')[1],
        "port": lambda x: x.interface.first().name,
        "dns": lambda x: x.dns_name
    },

    "VERBOSE_ATTR": {
        "ip": "Device",
        "alias": "IP Address",
    },

    "CONSISTENCY_TABLE": ["ip", "mask", "port", "dns"]
}


VLAN = {
    "ORM_MAP": {
        "vlan": "vid"
    },

    #mangling supported

    "NETBOX_ATTR": {
        "description": lambda x: x.name
    },

    "VERBOSE_ATTR": {
        "ip": "Device",
        "vlan": "VLAN ID",
        "description": "Description"
    },

    "CONSISTENCY_TABLE": ["description"]
}

