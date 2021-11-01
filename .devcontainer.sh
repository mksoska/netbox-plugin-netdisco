#!/bin/bash
source /opt/netbox/venv/bin/activate &&
python3 setup.py develop &&
sed -i "s|^PLUGINS = \[\(\s*\S+\s*\)\]|PLUGINS = \[\1, \"netbox_netdisco\"\]|g" /opt/netbox/netbox/netbox/configuration.py
sed -i "s|^PLUGINS = \[\s*\]|PLUGINS = \[\"netbox_netdisco\"\]|g" /opt/netbox/netbox/netbox/configuration.py
