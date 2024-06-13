from rest_framework import serializers
from .models import Global_Vars


class GlobalVarsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Global_Vars
        fields = '__all__'
