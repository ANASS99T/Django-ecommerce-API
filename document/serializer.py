from rest_framework import serializers
from .models import Document


class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = ['id', 'name', 'path', 'product', 'product', 'document_type', 'size', 'dimension', 'status', 'is_main',
                  'created_at', 'updated_at', 'deleted_at']
