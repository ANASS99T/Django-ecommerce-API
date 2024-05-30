from unittest.mock import patch
from permission.models import Permission
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from roles.models import Role


class RoleViewSetTestCase(TestCase):
    def setUp(self):
        self.url = reverse('roles-list')
        self.api_client = APIClient()
        self.data = {
            'name': 'TestRole',
            'description': 'This is a test role',
        }
        self.permission1 = Permission.objects.create(name='can_create_client')
        self.permission2 = Permission.objects.create(name='can_view_client')

    @patch('roles.views.check_permissions', return_value=True)
    def test_create_role_without_permission(self, mock_check_permissions):
        response = self.api_client.post(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        mock_check_permissions.assert_called()
        self.assertIn('permissions', response.data)

    @patch('roles.views.check_permissions', return_value=True)
    def test_create_role_with_permissions(self, mock_check_permissions):
        self.data['permissions'] = [self.permission1.id, self.permission2.id]
        response = self.api_client.post(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        new_role = response.data
        self.assertEqual(new_role['name'], 'TestRole')
        self.assertEqual(new_role['description'], 'This is a test role')
        self.assertEqual(len(new_role['permissions']), 2)
        mock_check_permissions.assert_called()

    @patch('roles.views.check_permissions', return_value=True)
    def test_update_role(self, mock_check_permissions):
        existing_role = Role.objects.create(name='New Role', description='This is a test role')
        existing_role.permissions.add(self.permission1)
        existing_role.permissions.add(self.permission2)
        update_url = reverse('roles-detail', args=[existing_role.id])
        update_data = {
            'name': 'TestRoleUpdated',
            'description': 'This is a test role updated',
            'permissions': [self.permission1.id]
        }
        response = self.api_client.put(update_url, update_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        updated_role = response.data
        self.assertEqual(updated_role['name'], 'TestRoleUpdated')
        self.assertEqual(updated_role['description'], 'This is a test role updated')
        self.assertEqual(len(updated_role['permissions']), 1)
        self.assertEqual(existing_role.deleted_at, None)
        mock_check_permissions.assert_called()

    @patch('roles.views.check_permissions', return_value=True)
    def test_delete_role(self, mock_check_permissions):
        existing_role = Role.objects.create(name='New Role', description='This is a test role')
        existing_role.permissions.add(self.permission1)
        existing_role.permissions.add(self.permission2)
        delete_url = reverse('roles-detail', args=[existing_role.id])
        response = self.api_client.delete(delete_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        existing_role.refresh_from_db()
        self.assertNotEqual(existing_role.deleted_at, None)
        mock_check_permissions.assert_called()

    @patch('roles.views.check_permissions', return_value=True)
    def test_list_roles(self, mock_check_permissions):
        Role.objects.create(name='Demo Role 1', description='This is a demo role')
        Role.objects.create(name='Test Role 2', description='This is a test role')
        response = self.api_client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        mock_check_permissions.assert_called()

    @patch('roles.views.check_permissions', return_value=True)
    def test_retrieve_role(self, mock_check_permissions):
        existing_role = Role.objects.create(name='New Role', description='This is a test role')
        existing_role.permissions.add(self.permission1)
        existing_role.permissions.add(self.permission2)
        retrieve_url = reverse('roles-detail', args=[existing_role.id])
        response = self.api_client.get(retrieve_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        role = response.data
        self.assertEqual(role['name'], 'New Role')
        self.assertEqual(role['description'], 'This is a test role')
        self.assertEqual(len(role['permissions']), 2)
        mock_check_permissions.assert_called()

    @patch('roles.views.check_permissions', return_value=True)
    def test_disable_role(self, mock_check_permissions):
        existing_role = Role.objects.create(name='New Role', description='This is a test role')
        existing_role.permissions.add(self.permission1)
        existing_role.permissions.add(self.permission2)
        disable_url = reverse('roles-detail', args=[existing_role.id])
        data = {
            'active': False
        }
        response = self.api_client.put(disable_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        existing_role.refresh_from_db()
        self.assertEqual(existing_role.active, False)
        mock_check_permissions.assert_called()