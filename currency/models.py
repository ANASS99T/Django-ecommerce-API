from django.db import models
from django.utils import timezone


class Currency(models.Model):
    code = models.CharField(max_length=3)
    name = models.CharField(max_length=50)
    symbol = models.CharField(max_length=10)
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    def delete(self, *args, **kwargs):
        self.deleted_at = timezone.now()
        self.status = False
        self.save()

