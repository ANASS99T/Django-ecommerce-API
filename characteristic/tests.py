from unittest.mock import patch

from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from category.models import Category
from product.models import Product
from .models import Characteristic
from django.utils import timezone


class CharacteristicViewSetTestCase(TestCase):
    def setUp(self):
        self.url = reverse('characteristics-list')
        self.api_client = APIClient()
        self.category = Category.objects.create(name='Test Category')
        self.product = Product.objects.create(name='Test Product', description='Description test',
                                              category=self.category, price=100)
        self.data = {
            'key': 'Material',
            'value': 'Metal',
            'product': self.product.id,
            'status': True
        }

    @patch('characteristic.views.check_permissions', return_value=True)
    def test_create_characteristic(self, mock_check_permissions):
        response = self.api_client.post(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        new_characteristic = response.data
        self.assertEqual(new_characteristic['key'], 'Material')
        mock_check_permissions.assert_called()

    @patch('characteristic.views.check_permissions', return_value=True)
    def test_update_characteristic(self, mock_check_permissions):
        existing = Characteristic.objects.create(key='model', value='2022', product=self.product)
        update_url = reverse('characteristics-detail', args=[existing.id])
        update_data = {
            'value': '2024',
        }
        response = self.api_client.put(update_url, update_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        updated_permission = response.data
        self.assertEqual(updated_permission['value'], '2024')
        mock_check_permissions.assert_called()

    @patch('characteristic.views.check_permissions', return_value=True)
    def test_delete_characteristic(self, mock_check_permissions):
        existing = Characteristic.objects.create(key='model', value='2022', product=self.product)
        delete_url = reverse('characteristics-detail', args=[existing.id])
        response = self.api_client.delete(delete_url)
        existing.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(existing.deleted_at is None)
        self.assertFalse(existing.status is True)
        mock_check_permissions.assert_called()

    @patch('characteristic.views.check_permissions', return_value=True)
    def test_list_characteristic(self, mock_check_permissions):
        char1 = Characteristic.objects.create(key='model', value='2022', product=self.product)
        Characteristic.objects.create(key='Power level', value='100%', product=self.product, parent=char1)
        Characteristic.objects.create(key='Brand', value='Apple', product=self.product, deleted_at=timezone.now())
        response = self.api_client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        mock_check_permissions.assert_called()

    @patch('characteristic.views.check_permissions', return_value=True)
    def test_retrieve_characteristic(self, mock_check_permissions):
        existing = Characteristic.objects.create(key='model', value='2023', product=self.product)
        retrieve_url = reverse('characteristics-detail', args=[existing.id])
        response = self.api_client.get(retrieve_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['value'], '2023')
        mock_check_permissions.assert_called()
