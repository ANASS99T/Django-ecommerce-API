from rest_framework import viewsets, status
from rest_framework.response import Response
from user.models import Client
from user.serializer import ClientSerializer
from helpers.permission_helpers import check_auth, check_permissions


class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer

    def create(self, request, *args, **kwargs):
        if not check_auth(request) and not check_permissions(request, 'can_create_client'):
            return Response({'message': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers) 