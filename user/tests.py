from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from unittest.mock import patch
from rest_framework import status

from global_vars.models import Global_Vars
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
        permission = Permission.objects.create(name='can_delete_client')
        role = Role.objects.create(name='Main')
        role.permissions.add(permission)
        self.user.roles.add(role)
        self.user.save()
        self.api_client.force_authenticate(user=self.user)
        client = Client.objects.create(
            username='newclient',
            first_name='Exist',
            last_name='Client',
            email='email@email.com',
            password='password',
            phone_number='1234567890',
            date_of_birth='1990-01-01'
        )
        response = self.api_client.delete(f'{self.url}{client.id}/')
        client = Client.objects.get(username='newclient')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertNotEqual(client.deleted_at, None)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_self_destroy_client(self):
        permission = Permission.objects.create(name='can_delete_client_self')
        role = Role.objects.create(name='Main')
        role.permissions.add(permission)
        self.user.roles.add(role)
        self.user.save()
        self.api_client.force_authenticate(user=self.user)

        url = f'{self.url}self_destroy/'
        response = self.api_client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertNotEqual(self.user.deleted_at, None)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_list_clients(self):
        permission = Permission.objects.create(name='can_view_client_all')
        role = Role.objects.create(name='Main')
        role.permissions.add(permission)
        self.user.roles.add(role)
        self.user.save()
        self.api_client.force_authenticate(user=self.user)
        Client.objects.create(
            username='newclient1',
            first_name='Exist',
            last_name='Client',
            email='email1@email.com',
            password='password',
            phone_number='1234567890',
            date_of_birth='1990-01-01'
        )
        Client.objects.create(
            username='newclient2',
            first_name='Exist',
            last_name='Client',
            email='email2@email.com',
            password='password',
            phone_number='1234567890',
            date_of_birth='1990-01-01'
        )

        response = self.api_client.get(self.url)
        self.assertGreater(Client.objects.count(), 2)
        self.assertEqual(response.data[2]['username'], 'newclient2')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_client(self):
        permission = Permission.objects.create(name='can_view_client')
        role = Role.objects.create(name='Main')
        role.permissions.add(permission)
        self.user.roles.add(role)
        self.user.save()
        self.api_client.force_authenticate(user=self.user)
        client = Client.objects.create(
            username='newclient1',
            first_name='Exist',
            last_name='Client',
            email='email1@email.com',
            password='password',
            phone_number='1234567890',
            date_of_birth='1990-01-01'
        )

        response = self.api_client.get(f'{self.url}{client.id}/')
        self.assertGreater(Client.objects.count(), 1)
        self.assertEqual(response.data['username'], 'newclient1')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_reset_password(self):
        permission = Permission.objects.create(name='can_reset_password')
        role = Role.objects.create(name='Main')
        role.permissions.add(permission)
        self.user.roles.add(role)
        self.user.save()
        self.api_client.force_authenticate(user=self.user)

        Global_Vars.objects.create(key='default_password', value='newpassword')
        client = Client.objects.create(
            username='newClient',
            first_name='Exist',
            last_name='Client',
            email='email1@email.com',
            password='password',
            phone_number='1234567890',
            date_of_birth='1990-01-01'
        )
        url = f'{self.url}{client.id}/reset_password/'
        response = self.api_client.post(url)
        client.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('message', response.data)

    def test_self_reset_password(self):
        permission = Permission.objects.create(name='can_reset_password_self')
        role = Role.objects.create(name='Test')
        role.permissions.add(permission)
        self.user.roles.add(role)
        self.user.save()
        self.api_client.force_authenticate(user=self.user)

        Global_Vars.objects.create(key='default_password', value='newpassword')

        url = f'{self.url}self_reset_password/'
        response = self.api_client.post(url)
        self.user.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('message', response.data)

    def test_login_email(self):
        client = Client.objects.create(
            username='newClient',
            first_name='First Name',
            last_name='Last name',
            email='email1@email.com',
            password='password',
            phone_number='1234567890',
            date_of_birth='1990-01-01')

        url = f'{self.url}login/'
        response = self.api_client.post(url, data={'email': client.email, 'password': client.password}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)

    def test_login_phone(self):
        client = Client.objects.create(
            username='newClient',
            first_name='First Name',
            last_name='Last name',
            email='email1@email.com',
            password='password',
            phone_number='1234567890',
            date_of_birth='1990-01-01')

        url = f'{self.url}login/'
        response = self.api_client.post(url, data={'phone_number': client.phone_number, 'password': client.password}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)

    def test_register(self):
        data = {
            'username': 'newClient',
            'email': 'testclient@test.com',
            'phone_number': '1234567890',
            'password': 'P@ssword123',
            'confirm_password': 'P@ssword123'
        }

        url = f'{self.url}register/'
        response = self.api_client.post(url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['username'], data['username'])
