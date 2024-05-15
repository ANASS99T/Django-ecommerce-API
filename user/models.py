from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.utils import timezone


class Client(AbstractUser):
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    )

    phone_number = models.CharField(max_length=15, blank=True, null=True)
    date_of_birth = models.DateField(null=True, blank=True)
    profile_picture = models.ImageField(
        upload_to='profile_pictures/', null=True, blank=True)
    address = models.TextField(blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    gender = models.CharField(
        max_length=1, choices=GENDER_CHOICES, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    groups = models.ManyToManyField(
        Group, related_name='custom_client_groups', blank=True)
    user_permissions = models.ManyToManyField(
        Permission, related_name='custom_client_permissions', blank=True)

    def delete(self, *args, **kwargs):
        self.deleted_at = timezone.now()
        self.save()

    class Meta:
        app_label = 'user'
