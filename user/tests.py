from django.test import Client as Cl, TestCase
from django.urls import reverse
from unittest.mock import patch
from rest_framework import status
from .models import Client


class ClientViewTestCase(TestCase):
    def setUp(self):
        self.client = Cl()
        self.url = reverse('clients-list')
        self.data = {
            'username': 'test_username',
            'first_name':'Test',
            'last_name':'Client',
            'email': 'test@test.com',
            'phone_number': '00212644335533',
            'date_of_birth': '1990-01-01',
        }

    @patch('user.views.check_auth', return_value=True)
    @patch('user.views.check_permissions', return_value=True)
    def test_create_client_authenticated_with_permission(self, mock_check_auth, mock_check_permissions):
        response = self.client.post(self.url, self.data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Client.objects.count(), 1)
        self.assertEqual(Client.objects.get().username, 'test_username')

        mock_check_auth.assert_called_once()
        mock_check_permissions.assert_called_once_with(any(), 'can_create_client')

        
    @patch('user.views.check_auth', return_value=False)
    @patch('user.views.check_permissions', return_value=True)
    def test_create_client_not_authenticated_with_permission(self, mock_check_auth, mock_check_permissions):
        response = self.client.post(self.url, self.data)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(Client.objects.count(), 0)

        mock_check_auth.assert_called_once()
        mock_check_permissions.assert_not_called()

    @patch('user.views.check_auth', return_value=True)
    @patch('user.views.check_permissions', return_value=False)
    def test_create_client_authenticated_without_permission(self, mock_check_auth, mock_check_permissions):
        response = self.client.post(self.url, self.data)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(Client.objects.count(), 0)

        mock_check_auth.assert_called_once()
        mock_check_permissions.assert_called_once_with(any(), 'can_create_client')