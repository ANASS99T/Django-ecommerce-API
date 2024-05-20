from django.test import TestCase
from django.urls import reverse
from unittest.mock import patch
from rest_framework import status
from .models import Client
from django.contrib.auth.models import User
from rest_framework.test import APIClient

class ClientViewTestCase(TestCase):
    def setUp(self):
        self.url = reverse('clients-list')
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.api_client = APIClient()
        self.api_client.force_authenticate(user=self.user)
        self.data = {
            'username': 'testclient',
            'first_name': 'Test',
            'last_name': 'Client',
            'email': 'testclient@test.com',
            'phone_number': '1234567890',
            'date_of_birth': '1990-01-01',
        }


    @patch('user.views.check_permissions', return_value=True)
    def test_create_client_authenticated_with_permission(self, mock_check_permissions):
        
        response = self.client.post(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Client.objects.count(), 1)
        self.assertEqual(Client.objects.get().first_name, 'Test')

        mock_check_permissions.assert_called()


    @patch('user.views.check_auth', return_value=False)
    def test_create_client_not_authenticated_with_permission(self, check_auth):
        response = self.client.post(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(Client.objects.count(), 0)
        check_auth.assert_not_called()

    @patch('user.views.check_permissions', return_value=False)
    def test_create_client_authenticated_without_permission(self, mock_check_permissions):
        response = self.client.post(self.url, self.data, format='json')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(Client.objects.count(), 0)

        mock_check_permissions.assert_called_once()



   