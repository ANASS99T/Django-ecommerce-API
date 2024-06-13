from django.db import models
from django.utils import timezone
from product.models import Product
from user.models import Client


class Cart(models.Model):
    client = models.OneToOneField(Client, on_delete=models.CASCADE, related_name='cart')
    status = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    def delete(self, *args, **kwargs):
        self.deleted_at = timezone.now()
        self.status = False
        self.save()



