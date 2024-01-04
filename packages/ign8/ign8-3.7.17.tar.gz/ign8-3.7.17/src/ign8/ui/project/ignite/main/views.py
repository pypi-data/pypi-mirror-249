from django.shortcuts import render
from .models import maindata
from rest_framework import viewsets


def mainview(request):
    maindata_entries = maindata.objects.all()
    return render(request, 'main.html', {'selinux_entries': maindata_entries})
