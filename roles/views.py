from rest_framework import viewsets, status
from rest_framework.response import Response

from helpers.permission_helpers import unauthorized, check_permissions, check_auth
from roles.models import Role
from roles.serializer import RoleSerializer


class RoleViewSet(viewsets.ModelViewSet):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer

    def create(self, request, *args, **kwargs):
        if not check_permissions(request, 'can_create_role'):
            return unauthorized()
        if not request.data.get('permissions'):
            return Response({'permissions': 'To create a role, you need at least one permission'}, status=status.HTTP_400_BAD_REQUEST)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        if not check_permissions(request, 'can_update_role'):
            return unauthorized()
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        if not check_permissions(request, 'can_delete_role'):
            return unauthorized()
        role = self.get_object()
        role.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def list(self, request, *args, **kwargs):
        if not check_permissions(request, 'can_view_role_list'):
            return unauthorized()
        return super().list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        if not check_permissions(request, 'can_view_role'):
            return unauthorized()
        return super().retrieve(request, *args, **kwargs)