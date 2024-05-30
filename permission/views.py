from rest_framework import viewsets, status
from rest_framework.response import Response

from helpers.permission_helpers import unauthorized, check_permissions, check_auth
from permission.models import Permission
from permission.serializer import PermissionSerializer


class PermissionViewSet(viewsets.ModelViewSet):
    queryset = Permission.objects.all()
    serializer_class = PermissionSerializer

    def create(self, request, *args, **kwargs):
        if not check_permissions(request, 'can_create_permission'):
            return unauthorized()

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        if not check_permissions(request, 'can_update_permission'):
            return unauthorized()
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        if not check_permissions(request, 'can_delete_permission'):
            return unauthorized()
        return super().destroy(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        if not check_permissions(request, 'can_view_permission_list'):
            return unauthorized()
        return super().list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        if not check_permissions(request, 'can_view_permission'):
            return unauthorized()
        return super().retrieve(request, *args, **kwargs)