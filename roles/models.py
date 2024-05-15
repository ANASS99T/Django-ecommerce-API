from django.db import models
from django.contrib.auth.models import Permission

class Role(models.Model):
    name = models.CharField(max_length=200)
    permissions = models.ManyToManyField(Permission)