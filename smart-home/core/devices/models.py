from django.db import models

# Create your models here.


class Device(models.Model):
    name = models.CharField(max_length=255)
    protocol = models.CharField(max_length=255)
