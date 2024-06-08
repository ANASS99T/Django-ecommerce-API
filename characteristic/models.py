from django.db import models
from django.utils import timezone
from product.models import Product


class Characteristic(models.Model):
    key = models.CharField(max_length=50)
    value = models.CharField(max_length=250)
    product = models.ForeignKey(Product, related_name='characteristics', on_delete=models.CASCADE)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    def delete(self, *args, **kwargs):
        self.deleted_at = timezone.now()
        self.status = False
        self.save()
