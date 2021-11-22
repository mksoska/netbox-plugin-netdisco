from django.urls import path
from . import views

urlpatterns = [
    path('', views.NetdiscoDeviceListView.as_view(), name='device_list'),
    path('device/<ip>/', views.NetdiscoDeviceView.as_view(), name="device"),

    path('port/', views.NetdiscoPortListView.as_view(), name="port_list"),
    path('device/<ip>/port/', views.NetdiscoDevicePortListView.as_view(), name="device_port_list"),
    path('device/<ip>/port/<port>/', views.NetdiscoPortView.as_view(), name="port"),

    path('address/', views.NetdiscoAddressListView.as_view(), name="address_list"),
    path('address/<ip>/', views.NetdiscoAddressView.as_view(), name="address"),
    path('device/<ip>/address/', views.NetdiscoDeviceAddressListView.as_view(), name="device_address_list"),

    path('vlan/', views.NetdiscoVlanListView.as_view(), name="vlan_list"),
    path('device/<ip>/vlan/', views.NetdiscoDeviceVlanListView.as_view(), name="device_vlan_list"),
    path('device/<ip>/vlan/<id>/', views.NetdiscoVlanView.as_view(), name="vlan")
]