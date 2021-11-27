DEVICE = {
    "ORM_MAP": {
        "ip": "primary_ip4__address__contains"
    },

    "ATTRIBUTE_MAP": {        
        "name": "name",
        "location": "location",
        "vendor": "device_type.manufacturer.name",
        "model": "device_type.model",
        "serial": "serial"                    
    },

    "ATTRIBUTE_VERBOSE": {
        "ip": "Management Address",
        "name": "System Hostname",
        "dns": "DNS",
        "location": "Location"
    },

    "NETDISCO_ATTR_CONVERT": {},

    "NETBOX_ATTR_CONVERT": {
        "ip": lambda x: str(x).split('/')[0]
    },

    "IGNORE": {}
}


PORT = {
    "ORM_MAP": {
        "ip": "device__primary_ip4__address__contains",
        "port": "name"
    }, 

    "ATTRIBUTE_MAP": {        
        "remote_ip": "_path.destination.device.primary_ip4.address",
        "remote_port": "_path.destination.name",
        "desc": "description",
        "type": "type",
        "remote_type": "_path.destination.type",
        "mac": "mac_address",
        "mtu": "mtu",
        "pvid": "untagged_vlan_id",
        "up_admin": "enabled"            
    },

    "ATTRIBUTE_VERBOSE": {
        "ip": "Device",
        "remote_ip": "Neighbor Device",
        "desc": "Description",
        "mac": "Mac Address",
        "mtu": "MTU",
        "pvid": "Native VLAN",
        "up_admin": "Enabled"
    },

    "NETDISCO_ATTR_CONVERT": {
        "up": lambda x: x == "Up",
        "up_admin": lambda x: x == "Up"
    },

    "NETBOX_ATTR_CONVERT": {
        "ip": lambda x: str(x).split('/')[0]
    },

    "IGNORE": {}
}


ADDRESS = {
    "ORM_MAP": {
        "alias": "address__contains",
    },

    "ATTRIBUTE_MAP": {
        "ip": 'interface.get(name=self.netdisco.port).device.primary_ip4.address',
        "subnet_": "address",
        "port": "interface.name",
        "dns": "dns_name"            
    },

    "ATTRIBUTE_VERBOSE": {
        "ip": "Device",
        "alias": "IP Address",
        "subnet_": "Mask"
    }, 

    "NETDISCO_ATTR_CONVERT": {
        "subnet_": lambda x: '/' + x.split('/')[1]
    },

    "NETBOX_ATTR_CONVERT": {
        "ip": lambda x: str(x).split('/')[0],
        "subnet_": lambda x: '/' + str(x).split('/')[1]
    },

    "IGNORE": {}
}


VLAN = {
    "ORM_MAP": {
        "vlan": "vid"
    },

    "ATTRIBUTE_MAP": {  
        #TODO: ip      
        "description": "name"
    },

    "ATTRIBUTE_VERBOSE": {
        "ip": "Device",
        "vlan": "VLAN ID",
        "description": "Name"
    },

    "NETDISCO_ATTR_CONVERT": {},

    "NETBOX_ATTR_CONVERT": {
        "ip": lambda x: str(x).split('/')[0]
    },

    "IGNORE": {}
}

