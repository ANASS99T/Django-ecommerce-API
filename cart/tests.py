from unittest.mock import patch

from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from user.models import Client
from .models import Cart
from django.utils import timezone


class CartViewSetTestCase(TestCase):
    def setUp(self):
        self.url = reverse('cart-list')
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

        self.data = {
            'client': self.client.id,
            'status': True
        }

    @patch('cart.views.check_permissions', return_value=True)
    def test_create_cart(self, mock_check_permissions):
        response = self.api_client.post(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        new_cart = response.data
        self.assertEqual(new_cart['client'], self.client.id)
        mock_check_permissions.assert_called()

    @patch('cart.views.check_permissions', return_value=True)
    def test_update_cart(self, mock_check_permissions):
        existing = Cart.objects.create(client=self.client, status=False)
        update_url = reverse('cart-detail', args=[existing.id])
        update_data = {
            'status': True,
        }
        response = self.api_client.put(update_url, update_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        updated_permission = response.data
        self.assertEqual(updated_permission['status'], True)
        mock_check_permissions.assert_called()

    @patch('cart.views.check_permissions', return_value=True)
    def test_delete_cart(self, mock_check_permissions):
        existing = Cart.objects.create(client=self.client, status=False)
        delete_url = reverse('cart-detail', args=[existing.id])
        response = self.api_client.delete(delete_url)
        existing.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(existing.deleted_at is None)
        self.assertFalse(existing.status is True)
        mock_check_permissions.assert_called()

    @patch('cart.views.check_permissions', return_value=True)
    def test_list_cart(self, mock_check_permissions):
        client2 = Client.objects.create(
            username='newclient 1',
            first_name='Exist 1',
            last_name='Client 1',
            email='email1@email.com',
            password='password',
            phone_number='1234567820',
            date_of_birth='1990-01-01'
        )
        Cart.objects.create(client=self.client, status=False)
        Cart.objects.create(client=client2, status=True)
        response = self.api_client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        mock_check_permissions.assert_called()

    @patch('cart.views.check_permissions', return_value=True)
    def test_retrieve_cart(self, mock_check_permissions):
        existing = Cart.objects.create(client=self.client, status=True)
        retrieve_url = reverse('cart-detail', args=[existing.id])
        response = self.api_client.get(retrieve_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], True)
        mock_check_permissions.assert_called()
