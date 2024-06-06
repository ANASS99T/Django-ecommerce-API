from rest_framework import serializers
from .models import Characteristic


class CharacteristicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Characteristic
        fields = ['id', 'key', 'value', 'parent', 'product', 'status','created_at', 'updated_at', 'deleted_at']
