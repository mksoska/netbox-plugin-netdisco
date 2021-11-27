from django.urls import path, include
from netbox_netdisco.api import urls as api_urls
from . import views

urlpatterns = [
    path('device/', views.NetdiscoDeviceListView.as_view(), name='device_list'),
    #path('device/search/<search>', views.NetdiscoDeviceSearchView.as_view(), name='device_list'),
    path('device/<ip>/', views.NetdiscoDeviceView.as_view(), name="device"),

    path('port/', views.NetdiscoPortListView.as_view(), name="port_list"),
    #path('port/search/<search>', views.NetdiscoPortSearchView.as_view(), name="port_search"),
    path('device/<ip>/port/', views.NetdiscoDevicePortListView.as_view(), name="device_port_list"),
    path('port/<port>/device/<ip>/', views.NetdiscoPortView.as_view(), name="port"),

    path('address/', views.NetdiscoAddressListView.as_view(), name="address_list"),
    #path('address/search/<search>', views.NetdiscoAddressSearchView.as_view(), name="address_search"),
    path('device/<ip>/address/', views.NetdiscoDeviceAddressListView.as_view(), name="device_address_list"),
    path('address/<alias>/device/<ip>/', views.NetdiscoAddressView.as_view(), name="address"),

    path('vlan/', views.NetdiscoVlanListView.as_view(), name="vlan_list"),
    #path('vlan/search/<search>', views.NetdiscoVlanSearchView.as_view(), name="vlan_search"),
    path('device/<ip>/vlan/', views.NetdiscoDeviceVlanListView.as_view(), name="device_vlan_list"),
    path('vlan/<id>/device/<ip>/', views.NetdiscoVlanView.as_view(), name="vlan"),

    #path('api/', include((api_urls, 'api'), namespace="api")),

]