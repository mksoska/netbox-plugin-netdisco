# Netdisco plugin for NetBox
A plugin designed for comparing and synchronizing Netdisco device inventory with NetBox.

---

This project is a prototype implementation in it's early stage, and is not ready for production usage yet. It covers basic features that are brought by integrating NetBox as a data center infrastructure management (DCIM) tool including IP address management (IPAM) with Netdisco - system for automatic multilayer (L2/L3) network topology detection.

The plugin is capable of fetching the Netdisco device inventory data and comparing the entries with NetBox objects. The fetched device/port/address/vlan is linked to corresponding (by primary IP address) NetBox model and their attributes are inspected for any differences. 

Before official release, a bunch of tests need to be carried on physical as well as virtual network topology. After resolving the issues, more functions are planned to be implemented (e.g., adding a discovered device into NetBox).

Some of the missing production-use features are:
- authentication (right now anyone can access the plugin from the NetBox's web-view)
- authorization (logging of user's changes on Netbox's data through the plugin - for instance, adding a device)
- more monitoring system modules for sending notifications; right now only Icinga2 is supported

Especially, exception handling of invalid API requests needs to be added as soon as possible.

In case, you are interested in contributing to this project, or just want to give it a try, here below is a short installation manual. Of course, you can open an issue, in case you found a bug.

---

## Installation

First, download the client library with git an install via setuptools into Netbox's python venv:
```
git clone https://github.com/mksoska/openapi-client-netdisco.git
cd openapi-client-netdisco
source /opt/netbox/venv/bin/activate
python3 setup.py install
```

Next, assuming the venv is still active, download and install the Netbox Plugin Netdisco:
```
git clone https://github.com/mksoska/netbox-plugin-netdisco.git
cd netbox-plugin-netdisco
python3 setup.py install
```

Then, configure the plugin as an installed plugin in Netbox configuration.py:
```
vim /opt/netbox/netbox/netbox/configuration.py
```
TODO: add the configuration


Setup Netdisco host in the configuration.py file:


Setup Icinga host:




At this point, everything should be on its place and should be working. If any problem during the installation occured, please submit an issue or contant me directly.  



