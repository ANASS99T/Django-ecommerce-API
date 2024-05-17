from rest_framework import serializers
from .models import Client

class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ['id', 'username', 'email', 'phone_number', 'date_of_birth', 'profile_picture', 'address', 'bio', 'gender', 'created_at', 'updated_at', 'deleted_at']
