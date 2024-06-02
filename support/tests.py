from unittest.mock import patch

from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from user.tests import User
from .models import Support


class PermissionViewSetTestCase(TestCase):
    def setUp(self):
        self.url = reverse('support-list')
        self.user = User.objects.create_user(username='tester', password='password')
        self.api_client = APIClient()
        self.email = 'tester@email.com'
        self.data = {
            'message': 'This is a test message',
            'full_name': 'Test User',
            'email': 'email@test.com'
        }

    def test_create_support_without_authentication(self):
        response = self.api_client.post(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        new_support = response.data
        self.assertEqual(new_support['message'], 'This is a test message')
        self.assertEqual(new_support['status'], 'Pending')

    def test_create_support_with_authentication(self):
        self.api_client.force_authenticate(user=self.user)
        self.data['email'] = self.email
        response = self.api_client.post(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        new_support = response.data
        self.assertEqual(new_support['message'], 'This is a test message')
        self.assertEqual(new_support['status'], 'Pending')
        self.assertEqual(new_support['email'], self.email)
        self.assertEqual(new_support['client'], self.user.id)

    @patch('support.views.check_permissions', return_value=True)
    def test_update_support(self, mock_check_permissions):
        self.api_client.force_authenticate(user=self.user)
        existing_support = Support.objects.create(message='Message test', full_name='Test User', client=self.user,
                                                  email=self.email)
        update_url = reverse('support-detail', args=[existing_support.id])
        update_data = {
            'message': 'This is a new message text',
        }
        response = self.api_client.put(update_url, update_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        updated_support = response.data
        self.assertEqual(updated_support['message'], 'This is a new message text')
        mock_check_permissions.assert_called()

    @patch('support.views.check_permissions', return_value=True)
    def test_update_support_status(self, mock_check_permissions):
        self.api_client.force_authenticate(user=self.user)
        existing_support = Support.objects.create(message='Message test', full_name='Test User', client=self.user,
                                                  email=self.email)
        update_url = reverse('support-detail', args=[existing_support.id])
        update_data = {
            'message': 'This is a new message text',
            'status': 'Resolved'
        }
        response = self.api_client.put(f'{update_url}update_status/', update_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        updated_support = response.data
        self.assertEqual(updated_support['message'], 'Message test')
        self.assertEqual(updated_support['status'], 'Resolved')
        mock_check_permissions.assert_called()

    @patch('support.views.check_permissions', return_value=True)
    def test_delete_support(self, mock_check_permissions):
        existing_support = Support.objects.create(message='Message test', full_name='Test User',
                                                  email=self.email)
        delete_url = reverse('support-detail', args=[existing_support.id])
        response = self.api_client.delete(delete_url)
        existing_support.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(existing_support.deleted_at is None)
        mock_check_permissions.assert_called()

    @patch('support.views.check_permissions', return_value=True)
    def test_list_support(self, mock_check_permissions):
        Support.objects.create(message='Message test 1', full_name='Test User',
                               email=self.email)
        Support.objects.create(message='Message test 2', full_name='Test User',
                               email=self.email)
        Support.objects.create(message='Message test 3', full_name='Test User2',
                               email=self.email)

        response = self.api_client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)
        mock_check_permissions.assert_called()

    @patch('support.views.check_permissions', return_value=True)
    def test_retrieve_support(self, mock_check_permissions):
        support1=Support.objects.create(message='Message test 1', full_name='Test User',
                               email=self.email)
        Support.objects.create(message='Message test 2', full_name='Test User2',
                               email=self.email)
        Support.objects.create(message='Message test 3', full_name='Test User3',
                               email=self.email)
        retrieve_url = reverse('support-detail', args=[support1.id])
        response = self.api_client.get(retrieve_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['full_name'], 'Test User')
        mock_check_permissions.assert_called()
