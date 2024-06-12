from rest_framework import viewsets, status
from rest_framework.response import Response

from cart.models import Cart
from helpers.permission_helpers import unauthorized, check_permissions, check_auth
from user.models import Client
from .models import CartItem
from .serializer import CartItemSerializer


class CartItemViewSet(viewsets.ModelViewSet):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer

    def create(self, request, *args, **kwargs):
        if not check_permissions(request, 'can_create_cartItem'):
            return unauthorized()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        cart_id = request.data['cart']
        cart = Cart.objects.filter(id=cart_id).first()
        if not cart:
            return Response({'message': 'Cart does not exist'}, status=status.HTTP_400_BAD_REQUEST)
        if not cart.status:
            return Response({'message': 'Cart is not active'}, status=status.HTTP_400_BAD_REQUEST)

        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        if not check_permissions(request, 'can_update_cartItem'):
            return unauthorized()
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        if request.data['quantity'] == 0:
            self.perform_destroy(instance)
            return Response({'message': 'Item removed from cart'}, status=status.HTTP_200_OK)
        return Response(
            serializer.data)

    def destroy(self, request, *args, **kwargs):
        if not check_permissions(request, 'can_delete_cartItem'):
            return unauthorized()
        return super().destroy(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        if not check_permissions(request, 'can_view_cartItem_list'):
            return unauthorized()
        return super().list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        if not check_permissions(request, 'can_view_cartItem'):
            return unauthorized()
        return super().retrieve(request, *args, **kwargs)
