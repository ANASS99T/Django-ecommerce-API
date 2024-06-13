from rest_framework import serializers
from .models import Cart


class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = ['id', 'client', 'status', 'created_at', 'updated_at', 'deleted_at']
