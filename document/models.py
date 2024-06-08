from django.db import models
from django.utils import timezone

from ecommerce_api import settings
from product.models import Product
import os


class Document(models.Model):
    DocumentType = (
        ('Image', 'Image'),
        ('Video', 'Video'),
        ('PDF', 'PDF'),
    )
    name = models.CharField(max_length=200)
    path = models.FileField(upload_to=settings.MEDIA_ROOT)
    product = models.ForeignKey(Product, related_name='documents', on_delete=models.CASCADE)
    document_type = models.CharField(max_length=10, choices=DocumentType, default='Image')
    size = models.IntegerField()
    dimension = models.CharField(max_length=50, blank=True)
    status = models.BooleanField(default=True)
    is_main = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    def delete(self, *args, **kwargs):
        self.deleted_at = timezone.now()
        self.status = False
        try:
            # Check if running in a test environment
            if settings.TESTING:
                # Move the file to a temporary deleted directory for testing
                temp_deleted_media_root = os.path.join(settings.MEDIA_ROOT, 'temp_deleted')
                os.makedirs(temp_deleted_media_root, exist_ok=True)
                os.rename(self.path.path, os.path.join(temp_deleted_media_root, os.path.basename(self.path.path)))
            else:
                # Move the file to the actual deleted directory
                os.makedirs(settings.DELETED_MEDIA_ROOT, exist_ok=True)
                os.rename(self.path.path, os.path.join(settings.DELETED_MEDIA_ROOT, os.path.basename(self.path.path)))

            self.save()
            return True
        except Exception as e:
            print(e)
            return False
