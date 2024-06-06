from django.db import models
from django.utils import timezone
from product.models import Product


class Document(models.Model):

    DocumentType = (
        ('Image', 'Image'),
        ('Video', 'Video'),
        ('PDF', 'PDF'),
    )
    name = models.CharField(max_length=200)
    path = models.FileField(upload_to='documents/')
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
        self.save()
