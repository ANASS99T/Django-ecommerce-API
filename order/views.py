from rest_framework import viewsets, status
from rest_framework.response import Response

from currency.models import Currency
from currency.serializer import CurrencySerializer
from helpers.permission_helpers import unauthorized, check_permissions, check_auth
from user.models import Client
from cart.models import Cart
from user.serializer import ClientSerializer
from .models import Order
from orderItem.models import OrderItem
from .serializer import OrderSerializer, OrderItemSerializer


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.filter(deleted_at__isnull=True)
    serializer_class = OrderSerializer

    def create(self, request, *args, **kwargs):
        if not check_permissions(request, 'can_create_order'):
            return unauthorized()
        total = 0

        client = Client.objects.get(id=request.user.id)
        order = Order.objects.create(client=client)
        if 'shipping_address' in request.data:
            order.shipping_address = request.data['shipping_address']
        if 'currency' in request.data:
            currency = Currency.objects.get(id=request.data['currency'])
            order.currency = currency
        if 'cart' in request.data:
            cart = Cart.objects.get(id=request.data['cart'])
        else:
            cart = Cart.objects.get(client=Client.objects.get(id=request.user.id))

        cart_items = cart.items.all()
        if not cart_items:
            return Response({'message': 'No items in the cart'}, status=status.HTTP_400_BAD_REQUEST)
        for item in cart_items:
            try:
                OrderItem.objects.create(order=order, product=item.product, quantity=item.quantity)
                if item.product.currency.code != order.currency.code:
                    return Response({'message': 'Currency mismatch'}, status=status.HTTP_400_BAD_REQUEST)
                total += item.product.price * item.quantity
            except Exception as e:
                return Response({'message': 'Error while creating Order Items', 'error': str(e)},
                                status=status.HTTP_400_BAD_REQUEST)
        order.total_price = total
        order.save()
        client = Client.objects.get(id=order.client.id)
        currency = Currency.objects.get(id=order.currency.id)
        order_items = OrderItem.objects.filter(order=order)
        data = {
            'order': OrderSerializer(order).data,
            'client': ClientSerializer(client).data,
            'currency': CurrencySerializer(currency).data,
            'items': OrderItemSerializer(order_items, many=True).data
        }
        return Response(data=data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        if not check_permissions(request, 'can_update_order'):
            return unauthorized()
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        if 'total_price' in serializer.validated_data:
            serializer.validated_data['total_price'] = instance.total_price
        if 'currency' in serializer.validated_data:
            serializer.validated_data['currency'] = instance.currency

        self.perform_update(serializer)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        if not check_permissions(request, 'can_delete_order'):
            return unauthorized()
        order = self.get_object()
        order.delete()
        order.items.all().delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def list(self, request, *args, **kwargs):
        if not check_permissions(request, 'can_view_order_list'):
            return unauthorized()

        data = []
        orders = Order.objects.all()
        for order in orders:
            client = Client.objects.get(id=order.client.id)
            currency = Currency.objects.get(id=order.currency.id)
            order_items = OrderItem.objects.filter(order=order)
            data.append({
                'order': OrderSerializer(order).data,
                'client': ClientSerializer(client).data,
                'currency': CurrencySerializer(currency).data,
                'items': OrderItemSerializer(order_items, many=True).data
            })
        return Response(data, status=status.HTTP_200_OK)

    def list_self(self, request, *args, **kwargs):
        if not check_permissions(request, 'can_view_order_list_self'):
            return unauthorized()
        orders = Order.objects.filter(client=Client.objects.get(user=request.user))
        return Response(OrderSerializer(orders, many=True).data, status=status.HTTP_200_OK)

    def retrieve(self, request, *args, **kwargs):
        if not check_permissions(request, 'can_view_order'):
            return unauthorized()
        return super().retrieve(request, *args, **kwargs)

    def retrieve_self(self, request, *args, **kwargs):
        if not check_permissions(request, 'can_view_order_self'):
            return unauthorized()
        order = Order.objects.get(id=kwargs['pk'], client=Client.objects.get(user=request.user))
        return Response(OrderSerializer(order).data, status=status.HTTP_200_OK)
