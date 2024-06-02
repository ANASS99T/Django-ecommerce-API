from rest_framework import serializers
from .models import Support


class SupportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Support
        fields = ['id', 'client', 'message', 'full_name', 'email', 'status', 'parent', 'created_at', 'updated_at',
                  'deleted_at']
