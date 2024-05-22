# models.py
from django.db import models

class Global_Vars(models.Model):
    key = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)
    value = models.CharField(max_length=255)