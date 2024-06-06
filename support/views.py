from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from helpers.permission_helpers import unauthorized, check_permissions, check_auth
from support.models import Support
from support.serializer import SupportSerializer


class SupportViewSet(viewsets.ModelViewSet):
    queryset = Support.objects.filter(deleted_at__isnull=True)
    serializer_class = SupportSerializer

    def create(self, request, *args, **kwargs):
        if check_auth(request):
            request.data['client'] = request.user.id
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        if not check_permissions(request, 'can_update_support'):
            return unauthorized()
        instance = self.get_object()
        if instance.client != request.user:
            return unauthorized()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    @action(detail=True, methods=['put'])
    def update_status(self, request, *args, **kwargs):
        if not check_permissions(request, 'can_update_support_status'):
            return unauthorized()
        instance = self.get_object()
        data = {
            'status': request.data.get('status')
        }
        serializer = self.get_serializer(instance, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        if not check_permissions(request, 'can_delete_support'):
            return unauthorized()
        role = self.get_object()
        role.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def list(self, request, *args, **kwargs):
        if not check_permissions(request, 'can_view_support_list'):
            return unauthorized()
        return super().list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        if not check_permissions(request, 'can_view_support'):
            return unauthorized()
        return super().retrieve(request, *args, **kwargs)
