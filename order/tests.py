from unittest.mock import patch

from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from cart.models import Cart
from cartItem.models import CartItem
from category.models import Category
from currency.models import Currency
from orderItem.models import OrderItem
from product.models import Product
from user.tests import User
from .models import Order


class OrderViewSetTestCase(TestCase):
    def setUp(self):
        self.url = reverse('order-list')
        self.api_client = APIClient()
        self.user = User.objects.create_user(username='tester', password='password')

        self.category = Category.objects.create(name='Test Category')
        self.currency = Currency.objects.create(code='MAD', name='Moroccan Dirham', symbol='DH')
        self.product1 = Product.objects.create(name="Product Name", description="Product Description",
                                               category=self.category, currency=self.currency, price=1000.99,
                                               status=True)
        self.product2 = Product.objects.create(name="Product Name 2", description="Product Description 2",
                                               category=self.category, currency=self.currency, price=900.99,
                                               status=True)
        self.product3 = Product.objects.create(name="Product Name 3", currency=self.currency,
                                               description="Product Description 3",
                                               category=self.category, price=50.00, status=True)

        self.cart = Cart.objects.create(client=self.user, status=True)

        self.cartItem1 = CartItem.objects.create(cart=self.cart, product=self.product1, quantity=4)
        self.cartItem2 = CartItem.objects.create(cart=self.cart, product=self.product2, quantity=2)
        self.cartItem3 = CartItem.objects.create(cart=self.cart, product=self.product3, quantity=1)
        self.cart.items.add(self.cartItem1, self.cartItem2, self.cartItem3)
        self.cart.save()
        self.data = {
            'client': self.user.id,
            'shipping_address': 'Test Address',
            'currency': self.currency.id
        }

    @patch('order.views.check_permissions', return_value=True)
    def test_create_order(self, mock_check_permissions):
        self.api_client.force_authenticate(user=self.user)
        self.cart.save()
        response = self.api_client.post(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        new_cart = response.data
        self.assertEqual(new_cart['client']['id'], self.user.id)
        self.assertFalse(new_cart['order']['total_price'] == 0)
        mock_check_permissions.assert_called()

    @patch('order.views.check_permissions', return_value=True)
    def test_create_order_no_items(self, mock_check_permissions):
        self.api_client.force_authenticate(user=self.user)
        CartItem.objects.filter(cart=self.cart).delete()

        response = self.api_client.post(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue(response.data['message'] == 'No items in the cart')
        mock_check_permissions.assert_called()

    @patch('order.views.check_permissions', return_value=True)
    def test_create_order_currency_mismatch(self, mock_check_permissions):
        self.api_client.force_authenticate(user=self.user)
        self.currency2 = Currency.objects.create(code='USD', name='US Dollar', symbol='$')
        self.product4 = Product.objects.create(name="Product Name 4", description="Product Description 4",
                                               category=self.category, currency=self.currency2, price=1000.99,
                                               status=True)
        self.cartItem4 = CartItem.objects.create(cart=self.cart, product=self.product4, quantity=1)
        self.cart.items.add(self.cartItem4)
        self.cart.save()

        response = self.api_client.post(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue(response.data['message'] == 'Currency mismatch')
        mock_check_permissions.assert_called()

    @patch('order.views.check_permissions', return_value=True)
    def test_update_order_price(self, mock_check_permissions):
        self.api_client.force_authenticate(user=self.user)
        order = Order.objects.create(client=self.user)
        update_url = reverse('order-detail', args=[order.id])
        update_data = {
            'total_price': 2000.00,
        }
        response = self.api_client.put(update_url, update_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        updated_data = response.data
        self.assertFalse(updated_data['total_price'] == 2000.00)
        mock_check_permissions.assert_called()

    @patch('order.views.check_permissions', return_value=True)
    def test_update_order_currency(self, mock_check_permissions):
        self.api_client.force_authenticate(user=self.user)
        order = Order.objects.create(client=self.user)
        update_url = reverse('order-detail', args=[order.id])
        update_data = {
            'currency': self.currency.id,
        }
        response = self.api_client.put(update_url, update_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        updated_data = response.data
        self.assertFalse(updated_data['currency'] == self.currency.id)
        mock_check_permissions.assert_called()

    @patch('order.views.check_permissions', return_value=True)
    def test_update_order(self, mock_check_permissions):
        self.api_client.force_authenticate(user=self.user)
        order = Order.objects.create(client=self.user)
        update_url = reverse('order-detail', args=[order.id])
        update_data = {
            'shipping_address': 'Test Address',
        }
        response = self.api_client.put(update_url, update_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        updated_data = response.data
        self.assertEqual(updated_data['shipping_address'], 'Test Address')
        mock_check_permissions.assert_called()

    @patch('order.views.check_permissions', return_value=True)
    def test_delete_order(self, mock_check_permissions):
        self.api_client.force_authenticate(user=self.user)
        order = Order.objects.create(client=self.user)
        orderItem1 = OrderItem.objects.create(order=order, product=self.product1, quantity=4)
        orderItem2 = OrderItem.objects.create(order=order, product=self.product2, quantity=2)
        orderItem3 = OrderItem.objects.create(order=order, product=self.product3, quantity=1)
        order.total_price = self.product1.price * 4 + self.product2.price * 2 + self.product3.price
        order.items.add(orderItem1, orderItem2, orderItem3)
        order.save()
        delete_url = reverse('order-detail', args=[order.id])
        response = self.api_client.delete(delete_url)
        order.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(order.deleted_at is None)
        self.assertTrue(len(order.items.all()) == 0)
        mock_check_permissions.assert_called()

    @patch('order.views.check_permissions', return_value=True)
    def test_list_order(self, mock_check_permissions):
        self.api_client.force_authenticate(user=self.user)
        order = Order.objects.create(client=self.user)
        orderItem1 = OrderItem.objects.create(order=order, product=self.product1, quantity=4)
        orderItem2 = OrderItem.objects.create(order=order, product=self.product2, quantity=2)
        orderItem3 = OrderItem.objects.create(order=order, product=self.product3, quantity=1)
        order.total_price = self.product1.price * 4 + self.product2.price * 2 + self.product3.price
        order.items.add(orderItem1, orderItem2, orderItem3)
        order.currency = self.currency
        order.save()
        response = self.api_client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        mock_check_permissions.assert_called()

    @patch('order.views.check_permissions', return_value=True)
    def test_list_order_self(self, mock_check_permissions):
        self.api_client.force_authenticate(user=self.user)
        order = Order.objects.create(client=self.user)
        orderItem1 = OrderItem.objects.create(order=order, product=self.product1, quantity=4)
        orderItem2 = OrderItem.objects.create(order=order, product=self.product2, quantity=2)
        orderItem3 = OrderItem.objects.create(order=order, product=self.product3, quantity=1)
        order.total_price = self.product1.price * 4 + self.product2.price * 2 + self.product3.price
        order.items.add(orderItem1, orderItem2, orderItem3)
        order.currency = self.currency
        order.save()
        response = self.api_client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        mock_check_permissions.assert_called()

    @patch('order.views.check_permissions', return_value=True)
    def test_retrieve_order(self, mock_check_permissions):
        self.api_client.force_authenticate(user=self.user)
        order = Order.objects.create(client=self.user)
        orderItem1 = OrderItem.objects.create(order=order, product=self.product1, quantity=4)
        orderItem2 = OrderItem.objects.create(order=order, product=self.product2, quantity=2)
        orderItem3 = OrderItem.objects.create(order=order, product=self.product3, quantity=1)
        order.total_price = self.product1.price * 4 + self.product2.price * 2 + self.product3.price
        order.items.add(orderItem1, orderItem2, orderItem3)
        order.currency = self.currency
        order.save()
        retrieve_url = reverse('order-detail', args=[order.id])
        response = self.api_client.get(retrieve_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], order.id)
        mock_check_permissions.assert_called()