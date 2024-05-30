from unittest.mock import patch

from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from roles.models import Role
from .models import Permission


class PermissionViewSetTestCase(TestCase):
    def setUp(self):
        self.url = reverse('permissions-list')
        self.api_client = APIClient()
        self.data = {
            'name': 'TestPermission',
        }

    @patch('permission.views.check_permissions', return_value=True)
    def test_create_permission(self, mock_check_permissions):
        response = self.api_client.post(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        new_permission = response.data
        self.assertEqual(new_permission['name'], 'TestPermission')
        mock_check_permissions.assert_called()

    @patch('permission.views.check_permissions', return_value=True)
    def test_update_permission(self, mock_check_permissions):
        existing_permission = Permission.objects.create(name='New Permission')
        update_url = reverse('permissions-detail', args=[existing_permission.id])
        update_data = {
            'name': 'TestPermissionUpdated',
        }
        response = self.api_client.put(update_url, update_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        updated_permission = response.data
        self.assertEqual(updated_permission['name'], 'TestPermissionUpdated')
        mock_check_permissions.assert_called()

    @patch('permission.views.check_permissions', return_value=True)
    def test_delete_permission(self, mock_check_permissions):
        existing_permission = Permission.objects.create(name='New Permission')
        delete_url = reverse('permissions-detail', args=[existing_permission.id])
        response = self.api_client.delete(delete_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Permission.objects.filter(name='New Permission').exists())
        mock_check_permissions.assert_called()

    @patch('permission.views.check_permissions', return_value=True)
    def test_list_permission(self, mock_check_permissions):
        Permission.objects.create(name='Demo Permission 1')
        Permission.objects.create(name='Demo Permission 2')

        response = self.api_client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        mock_check_permissions.assert_called()

    @patch('permission.views.check_permissions', return_value=True)
    def test_retrieve_permission(self, mock_check_permissions):
        existing_permission = Permission.objects.create(name='New Permission')
        retrieve_url = reverse('permissions-detail', args=[existing_permission.id])
        response = self.api_client.get(retrieve_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'New Permission')
        mock_check_permissions.assert_called()