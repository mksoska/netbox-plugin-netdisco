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

    "NETDISCO_ATTR_CONVERT": {},

    "NETBOX_ATTR_CONVERT": {
        "ip": lambda x: str(x).split('/')[0]
    },

    "VERBOSE_NAME": {
        "ip": "Management Address",
        "name": "System Hostname",
        "dns": "DNS",
        "location": "Location"
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

    "NETDISCO_ATTR_CONVERT": {
        "up": lambda x: x == "Up",
        "up_admin": lambda x: x == "Up"
    },

    "NETBOX_ATTR_CONVERT": {
        "ip": lambda x: str(x).split('/')[0],
        "remote_ip": lambda x: str(x).split('/')[0],
    },

    "VERBOSE_NAME": {
        "ip": "Device",
        "remote_ip": "Neighbor Device",
        "desc": "Description",
        "mac": "Mac Address",
        "mtu": "MTU",
        "pvid": "Native VLAN",
        "up_admin": "Enabled"
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
        "port": "interface.get(name=self.netdisco.port).name",
        "dns": "dns_name"            
    },

    "NETDISCO_ATTR_CONVERT": {
        "subnet_": lambda x: '/' + x.split('/')[1]
    },

    "NETBOX_ATTR_CONVERT": {
        "ip": lambda x: str(x).split('/')[0],
        "subnet_": lambda x: '/' + str(x).split('/')[1]
    },

    "VERBOSE_NAME": {
        "ip": "Device",
        "alias": "IP Address",
        "subnet_": "Mask"
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

    "NETDISCO_ATTR_CONVERT": {},

    "NETBOX_ATTR_CONVERT": {
        "ip": lambda x: str(x).split('/')[0]
    },

    "VERBOSE_NAME": {
        "ip": "Device",
        "vlan": "VLAN ID",
        "description": "Name"
    },

    "IGNORE": {}
}

