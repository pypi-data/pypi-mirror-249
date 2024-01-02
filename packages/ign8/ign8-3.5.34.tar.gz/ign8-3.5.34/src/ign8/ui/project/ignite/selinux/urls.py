
from django.urls import path, include
from .views import selinux_list, selinux_event_list , UploadSelinuxDataView, UploadSElinuxEventView
from rest_framework.routers import DefaultRouter



urlpatterns = [
    path('', selinux_list, name='selinux_list'),
    path('selinux_list/', selinux_list, name='selinux_list'),
    path('selinux_event_list/', selinux_event_list, name='selinux_event_list'),
    path('selinux_event_list/<int:pk>/', selinux_event_list, name='selinux_event_list'),
    path('upload_selinux_data/', UploadSelinuxDataView.as_view(), name='upload_selinux_data'),
    path('upload_selinux_event/', UploadSElinuxEventView.as_view(), name='upload_selinux_event'),
]
