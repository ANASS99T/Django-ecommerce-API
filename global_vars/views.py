from rest_framework import viewsets, status
from rest_framework.response import Response

from helpers.permission_helpers import unauthorized, check_permissions, check_auth
from global_vars.models import Global_Vars
from global_vars.serializer import GlobalVarsSerializer


class GlobalVarsViewSet(viewsets.ModelViewSet):
    queryset = Global_Vars.objects.all()
    serializer_class = GlobalVarsSerializer

    def create(self, request, *args, **kwargs):
        if not check_permissions(request, 'can_create_global_vars'):
            return unauthorized()

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        if not check_permissions(request, 'can_update_global_vars'):
            return unauthorized()
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        if not check_permissions(request, 'can_delete_global_vars'):
            return unauthorized()
        return super().destroy(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        if not check_permissions(request, 'can_view_global_vars_list'):
            return unauthorized()
        return super().list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        if not check_permissions(request, 'can_view_global_vars'):
            return unauthorized()
        return super().retrieve(request, *args, **kwargs)
