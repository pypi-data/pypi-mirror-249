
from django.urls import path, include
from .views import  mainview
from rest_framework.routers import DefaultRouter



urlpatterns = [
    path('', mainview, name='selinux_list'),
]