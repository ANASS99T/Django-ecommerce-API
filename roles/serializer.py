from rest_framework import serializers
from .models import Role


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ['id', 'name','description','active', 'permissions', 'created_at', 'updated_at', 'deleted_at']


