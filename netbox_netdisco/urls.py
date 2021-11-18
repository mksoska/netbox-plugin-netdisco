from django.urls import path
from . import views

urlpatterns = [
    path('', views.NetdiscoDeviceListView.as_view(), name='device_list'),
    path('device/<ip>/', views.NetdiscoDeviceView.as_view(), name="device"),
    path('device/<ip>/ports/', views.NetdiscoPortListView.as_view(), name="port_list"),
    path('device/<ip>/port/<port>/', views.NetdiscoPortView.as_view(), name="port")
]