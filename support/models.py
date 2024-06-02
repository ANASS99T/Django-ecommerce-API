from django.db import models
from django.utils import timezone

from user.models import Client


class Support(models.Model):
    MessageStatus = (
        ('Pending', 'Pending'),
        ('Resolved', 'Resolved'),
        ('Closed', 'Closed'),
    )

    client = models.ForeignKey(Client, on_delete=models.CASCADE, null=True, blank=True)
    message = models.TextField()
    full_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    status = models.CharField(max_length=100, choices=MessageStatus, default='Pending')
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    def delete(self, using=None, keep_parents=False):
        self.deleted_at = timezone.now()
        self.save()
