# Netdisco plugin for NetBox
A plugin designed for comparing and synchronizing Netdisco device inventory with NetBox.

---

This project is a prototype implementation in it's early stage, and is not ready for production usage yet. It covers basic features that are brought by integrating NetBox as a data center infrastructure management (DCIM) tool including IP address management (IPAM) with Netdisco - system for automatic multilayer (L2/L3) network topology detection.

The plugin is capable of fetching the Netdisco device inventory data and comparing the entries with NetBox objects. The fetched device/port/address/vlan is linked to corresponding (by primary IP address) NetBox model and their attributes are inspected for any differences. 

Insert GIFs of the usage.

Before official release, a bunch of tests need to be carried on physical as well as virtual network topology. After resolving the issues, more functions are planned to be implemented (e.g., adding a discovered device into NetBox plane).

Some of the missing production-use features are:
- authentication (right now anyone can access the plugin from the NetBox's web-view)
- authorization (logging of user's changes on Netbox's data through the plugin - for instance, adding a device)
- more monitoring system modules for sending notifications; right now only Icinga2 is supported

Especially, exception handling of invalid API requests needs to be added as soon as possible.

In case, you are interested in contributing to this project, or just want to give it a try, here below is a short installation manual. Of course, you can open an issue, if you found a defect, beside those already listed.

Add manual.





