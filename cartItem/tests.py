from unittest.mock import patch

from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from category.models import Category
from product.models import Product
from user.models import Client
from .models import CartItem
from cart.models import Cart


class CartItemViewSetTestCase(TestCase):
    def setUp(self):
        self.url = reverse('cartItem-list')
        self.api_client = APIClient()
        self.client = Client.objects.create(
            username='newclient',
            first_name='Exist',
            last_name='Client',
            email='email@email.com',
            password='password',
            phone_number='1234567890',
            date_of_birth='1990-01-01'
        )
        self.category = Category.objects.create(name='Test Category')
        self.product = Product.objects.create(name="Product Name", description="Product Description",
                                              category=self.category, price=1000.99, status=True)

        self.product2 = Product.objects.create(name="Product Name 2", description="Product Description 2",
                                               category=self.category, price=900.99, status=True)

        self.product3 = Product.objects.create(name="Product Name 3", description="Product Description 3",
                                               category=self.category, price=900.99, status=True)

        self.cart = Cart.objects.create(client=self.client, status=True)

        self.data = {
            'cart': self.cart.id,
            'product': self.product.id,
            'quantity': 3
        }

    @patch('cartItem.views.check_permissions', return_value=True)
    def test_create_cartItem(self, mock_check_permissions):
        response = self.api_client.post(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        new_cartItem = response.data
        self.assertEqual(new_cartItem['quantity'], 3)
        mock_check_permissions.assert_called()

    @patch('cartItem.views.check_permissions', return_value=True)
    def test_update_cartItem(self, mock_check_permissions):
        existing = CartItem.objects.create(cart=self.cart, product=self.product2, quantity=4)
        update_url = reverse('cartItem-detail', args=[existing.id])
        update_data = {
            'quantity': 1,
        }
        response = self.api_client.put(update_url, update_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        updated_permission = response.data
        self.assertEqual(updated_permission['quantity'], 1)
        mock_check_permissions.assert_called()

    @patch('cartItem.views.check_permissions', return_value=True)
    def test_delete_cartItem(self, mock_check_permissions):
        existing = CartItem.objects.create(cart=self.cart, product=self.product2, quantity=4)
        delete_url = reverse('cartItem-detail', args=[existing.id])
        response = self.api_client.delete(delete_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        mock_check_permissions.assert_called()

    @patch('cartItem.views.check_permissions', return_value=True)
    def test_list_cartItem(self, mock_check_permissions):
        CartItem.objects.create(cart=self.cart, product=self.product, quantity=4)
        CartItem.objects.create(cart=self.cart, product=self.product2, quantity=2)
        CartItem.objects.create(cart=self.cart, product=self.product3, quantity=1)
        response = self.api_client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)
        mock_check_permissions.assert_called()

    @patch('cartItem.views.check_permissions', return_value=True)
    def test_retrieve_cartItem(self, mock_check_permissions):
        CartItem.objects.create(cart=self.cart, product=self.product3, quantity=1)
        CartItem.objects.create(cart=self.cart, product=self.product2, quantity=2)
        existing = CartItem.objects.create(cart=self.cart, product=self.product, quantity=4)
        retrieve_url = reverse('cartItem-detail', args=[existing.id])
        response = self.api_client.get(retrieve_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['quantity'], 4)
        mock_check_permissions.assert_called()
