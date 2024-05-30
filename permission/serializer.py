from rest_framework import serializers
from .models import Permission


class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = ['id','name','description','active','created_at','updated_at']