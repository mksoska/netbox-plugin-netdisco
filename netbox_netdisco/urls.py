from django.urls import path
from . import views

urlpatterns = [
    path('', views.NetdiscoDeviceListView.as_view(), name='device_list'),
]