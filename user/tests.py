from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from unittest.mock import patch
from rest_framework import status

from roles.models import Role, Permission
from .models import Client
# from django.contrib.auth.models import User
from rest_framework.test import APIClient
from user.views import check_permissions, check_auth

User = get_user_model()


class ClientViewTestCase(TestCase):
    def setUp(self):
        self.url = reverse('clients-list')
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.api_client = APIClient()
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
        
        response = self.api_client.post(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        new_client = response.data
        self.assertEqual(new_client['username'], 'testclient')
        mock_check_permissions.assert_called()


    @patch('user.views.check_auth', return_value=False)
    def test_create_client_not_authenticated(self, check_auth):
        response = self.api_client.post(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(Client.objects.count(), 1)
        check_auth.assert_not_called()

    @patch('user.views.check_permissions', return_value=True)
    def test_update_client(self, mock_check_permissions):
        client = Client.objects.create(
            username='existclient',
            first_name='Exist',
            last_name='Client',
            email='email@email.com',
            password='password',
            phone_number='1234567890',
            date_of_birth='1990-01-01'
        )
        data = {
            'bio': 'This is Bio example',
            'gender': 'M',
            'phone_number': '0612123223'
        }
        self.api_client.force_authenticate(user=self.user)
        response = self.api_client.put(f'{self.url}{client.id}/', data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        updated_client = response.data
        self.assertEqual(updated_client['gender'], 'M')
        self.assertEqual(updated_client['username'], 'existclient')
        self.assertEqual(updated_client['phone_number'], '0612123223')
        mock_check_permissions.assert_called()

    def test_self_update_client(self):
        # Create role and permission for client
        permission = Permission.objects.create(name='can_update_client_self')
        role = Role.objects.create(name='Main')
        role.permissions.add(permission)
        self.user.roles.add(role)
        self.user.save()
        self.api_client.force_authenticate(user=self.user)

        url = f'{self.url}self_update/'

        response = self.api_client.put(url, data={'gender': 'M'}, format='json')
        self.assertEqual(response.wsgi_request.user, self.user)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.user.gender, 'M')

    def test_destroy_client(self):
        # TODO: Implement test logic
        pass


    def test_self_destroy_client(self):
        # TODO: Implement test logic
        pass


    def test_list_clients(self):
        # TODO: Implement test logic
        pass


    def test_retrieve_client(self):
        # TODO: Implement test logic
        pass


    def test_reset_password(self):
        # TODO: Implement test logic
        pass


    def test_self_reset_password(self):
        # TODO: Implement test logic
        pass


    def test_login(self):
        # TODO: Implement test logic
        pass


    def test_register(self):
        # TODO: Implement test logic
        pass