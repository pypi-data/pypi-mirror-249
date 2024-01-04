from django.db import models

# Create your models here.

class maindata(models.Model):
    name = models.CharField(max_length=100)

class services(models.Model):
    name = models.CharField(max_length=100)
    status = models.CharField(max_length=100)
    description = models.CharField(max_length=100)

class users(models.Model):
    name = models.CharField(max_length=100)
    status = models.CharField(max_length=100)
    description = models.CharField(max_length=100)

class groups(models.Model):
    name = models.CharField(max_length=100)
    status = models.CharField(max_length=100)
    description = models.CharField(max_length=100)

