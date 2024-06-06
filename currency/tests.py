from unittest.mock import patch

from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from .models import Currency
from django.utils import timezone


class CurrencyViewSetTestCase(TestCase):
    def setUp(self):
        self.url = reverse('currencies-list')
        self.api_client = APIClient()
        self.data = {
            'code': 'MDH',
            'name': 'Moroccan Dirham',
            'symbol': 'DH',
        }

    @patch('currency.views.check_permissions', return_value=True)
    def test_create_currency(self, mock_check_permissions):
        response = self.api_client.post(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        new_currency = response.data
        self.assertEqual(new_currency['code'], 'MDH')
        mock_check_permissions.assert_called()

    @patch('currency.views.check_permissions', return_value=True)
    def test_update_currency(self, mock_check_permissions):
        existing = Currency.objects.create(code='USD', name='United State Dollar', symbol='USD')
        update_url = reverse('currencies-detail', args=[existing.id])
        update_data = {
            'symbol': '$',
        }
        response = self.api_client.put(update_url, update_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        updated_permission = response.data
        self.assertEqual(updated_permission['symbol'], '$')
        mock_check_permissions.assert_called()

    @patch('currency.views.check_permissions', return_value=True)
    def test_delete_currency(self, mock_check_permissions):
        existing = Currency.objects.create(code='USD', name='United State Dollar', symbol='$')
        delete_url = reverse('currencies-detail', args=[existing.id])
        response = self.api_client.delete(delete_url)
        existing.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(existing.deleted_at is None)
        self.assertFalse(existing.status is True)
        mock_check_permissions.assert_called()

    @patch('currency.views.check_permissions', return_value=True)
    def test_list_currency(self, mock_check_permissions):
        Currency.objects.create(code='USD', name='United State Dollar', symbol='$')
        Currency.objects.create(code='EUR', name='Euro', symbol='€')
        Currency.objects.create(code='MAD', name='Moroccan Dirham', symbol='DH', deleted_at=timezone.now())
        response = self.api_client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        mock_check_permissions.assert_called()

    @patch('currency.views.check_permissions', return_value=True)
    def test_retrieve_currency(self, mock_check_permissions):
        existing = Currency.objects.create(code='USD', name='United State Dollar', symbol='$')
        retrieve_url = reverse('currencies-detail', args=[existing.id])
        response = self.api_client.get(retrieve_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['code'], 'USD')
        mock_check_permissions.assert_called()
