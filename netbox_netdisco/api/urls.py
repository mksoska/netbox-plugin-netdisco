from django.urls import path
from . import views

urlpatterns = [
    path('collect/', views.inventory_collect, name='inventory_collect'),
    path('notify/', views.inventory_notify, name='inventory_notify'),

    path('collect/device/', views.collect_devices, name='collect_devices'),
    path('collect/device/<ip>/', views.collect_device, name='collect_device'),

    path('collect/port/', views.collect_ports, name='collect_ports'),
    path('collect/device/<ip>/port/', views.collect_device_ports, name='collect_device_ports'),
    path('collect/device/<ip>/port/<port>/', views.collect_port, name='collect_port'),

    path('collect/address/', views.collect_addresses, name='collect_addresses'),
    path('collect/device/<ip>/address/', views.collect_device_addresses, name='collect_device_addresses'),

    path('collect/vlan/', views.collect_vlans, name='collect_vlans'),
    path('collect/device/<ip>/vlan/', views.collect_device_vlans, name='collect_device_vlans')
]