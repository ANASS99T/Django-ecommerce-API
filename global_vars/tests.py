from unittest.mock import patch

from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from .models import Global_Vars
from django.utils import timezone


class GlobalVarsViewSetTestCase(TestCase):
    def setUp(self):
        self.url = reverse('global_vars-list')
        self.api_client = APIClient()
        self.data = {
            'key': 'default_password',
            'value': '123456789'
        }

    @patch('global_vars.views.check_permissions', return_value=True)
    def test_create_currency(self, mock_check_permissions):
        response = self.api_client.post(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        new_currency = response.data
        self.assertEqual(new_currency['key'], 'default_password')
        mock_check_permissions.assert_called()

    @patch('global_vars.views.check_permissions', return_value=True)
    def test_update_currency(self, mock_check_permissions):
        existing = Global_Vars.objects.create(key='default_password', value='123456789')
        update_url = reverse('global_vars-detail', args=[existing.id])
        update_data = {
            'value': '987654321'
        }
        response = self.api_client.put(update_url, update_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        updated_data = response.data
        self.assertEqual(updated_data['value'], '987654321')
        mock_check_permissions.assert_called()

    @patch('global_vars.views.check_permissions', return_value=True)
    def test_delete_currency(self, mock_check_permissions):
        existing = Global_Vars.objects.create(key='default_password', value='123456789')
        delete_url = reverse('global_vars-detail', args=[existing.id])
        response = self.api_client.delete(delete_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        mock_check_permissions.assert_called()

    @patch('global_vars.views.check_permissions', return_value=True)
    def test_list_currency(self, mock_check_permissions):
        Global_Vars.objects.create(key='default_password', value='123456789')
        Global_Vars.objects.create(key='env', value='Prod')
        Global_Vars.objects.create(key='project_name', value='E-Commerce')
        response = self.api_client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)
        mock_check_permissions.assert_called()

    @patch('global_vars.views.check_permissions', return_value=True)
    def test_retrieve_currency(self, mock_check_permissions):
        existing = Global_Vars.objects.create(key='default_password', value='123456789')
        Global_Vars.objects.create(key='env', value='Prod')
        Global_Vars.objects.create(key='project_name', value='E-Commerce')
        retrieve_url = reverse('global_vars-detail', args=[existing.id])
        response = self.api_client.get(retrieve_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['key'], 'default_password')
        mock_check_permissions.assert_called()
