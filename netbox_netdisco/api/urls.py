from django.urls import path
from . import views

urlpatterns = [
    path('inventory/collect/', views.inventory_collect, name='inventory_collect'),
    path('inventory/notify/', views.inventory_notify, name='inventory_notify'),

    path('device/collect/', views.device_collect, name='device_collect')
]
