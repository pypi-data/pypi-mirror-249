from django.shortcuts import render
from .models import maindata, services

from rest_framework import viewsets


def mainview(request):
    maindata_entries = maindata.objects.all()
    maindata_services = services.objects.all()
    return render(request, 'main.html', {'maindata_entries': maindata_entries, 'title': 'IGN8', 'maindata_services': maindata_services})
