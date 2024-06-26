from rest_framework import viewsets, status
from rest_framework.response import Response

from helpers.permission_helpers import unauthorized, check_permissions, check_auth
from user.models import Client
from cart.models import Cart
from cart.serializer import CartSerializer


class CartViewSet(viewsets.ModelViewSet):
    queryset = Cart.objects.filter(deleted_at__isnull=True)
    serializer_class = CartSerializer

    def create(self, request, *args, **kwargs):
        if not check_permissions(request, 'can_create_cart'):
            return unauthorized()

        if 'client' not in request.data:
            return Response({'message': 'The client field is required.'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_id = request.data['client']
        user = Client.objects.filter(id=user_id).first()
        cart = Cart.objects.filter(client=user, deleted_at__isnull=True).first()
        if cart:
            return Response({'message': 'User already has a cart'}, status=status.HTTP_400_BAD_REQUEST)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        if not check_permissions(request, 'can_update_cart'):
            return unauthorized()
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(
            serializer.data)

    def destroy(self, request, *args, **kwargs):
        if not check_permissions(request, 'can_delete_cart'):
            return unauthorized()
        cart = self.get_object()
        cart.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def list(self, request, *args, **kwargs):
        if not check_permissions(request, 'can_view_cart_list'):
            return unauthorized()
        return super().list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        if not check_permissions(request, 'can_view_cart'):
            return unauthorized()
        return super().retrieve(request, *args, **kwargs)
