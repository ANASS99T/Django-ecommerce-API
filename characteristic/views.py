from rest_framework import viewsets, status
from rest_framework.response import Response

from helpers.permission_helpers import unauthorized, check_permissions, check_auth
from characteristic.models import Characteristic
from characteristic.serializer import CharacteristicSerializer


class CharacteristicViewSet(viewsets.ModelViewSet):
    queryset = Characteristic.objects.filter(deleted_at__isnull=True)
    serializer_class = CharacteristicSerializer
