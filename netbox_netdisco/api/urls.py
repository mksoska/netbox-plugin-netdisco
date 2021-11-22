from django.urls import path
from . import views

urlpatterns = [
    path('collect/', views.inventory_collect, name='inventory_collect')
]