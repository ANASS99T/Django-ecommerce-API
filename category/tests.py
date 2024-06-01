from unittest.mock import patch

from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from .models import Category


class CategoryViewSetTestCase(TestCase):
    def setUp(self):
        self.url = reverse('categories-list')
        self.api_client = APIClient()
        self.data = {
            'name': 'CategoryTest',
            'description': 'Category description',
        }

    @patch('category.views.check_permissions', return_value=True)
    def test_create_category(self, mock_check_permissions):
        response = self.api_client.post(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        new_category = response.data
        self.assertEqual(new_category['name'], 'CategoryTest')
        mock_check_permissions.assert_called()

    @patch('category.views.check_permissions', return_value=True)
    def test_create_sub_category(self, mock_check_permissions):
        parent_category = Category.objects.create(name='Parent category')
        self.data['parent'] = parent_category.id
        response = self.api_client.post(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        new_category = response.data
        self.assertEqual(new_category['name'], 'CategoryTest')
        mock_check_permissions.assert_called()

    @patch('category.views.check_permissions', return_value=True)
    def test_update_category(self, mock_check_permissions):
        existing_category = Category.objects.create(name='New category', description='New category description')
        update_url = reverse('categories-detail', args=[existing_category.id])
        update_data = {
            'name': 'TestCategoryUpdated',
        }
        response = self.api_client.put(update_url, update_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        updated_category = response.data
        self.assertEqual(updated_category['name'], 'TestCategoryUpdated')
        mock_check_permissions.assert_called()

    @patch('category.views.check_permissions', return_value=True)
    def test_delete_category(self, mock_check_permissions):
        existing_category = Category.objects.create(name='New category', description='New category description')
        delete_url = reverse('categories-detail', args=[existing_category.id])
        response = self.api_client.delete(delete_url)
        existing_category.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(existing_category.deleted_at is None)
        mock_check_permissions.assert_called()

    @patch('category.views.check_permissions', return_value=True)
    def test_list_category(self, mock_check_permissions):
        Category.objects.create(name='Demo category 1')
        Category.objects.create(name='Demo category 2')
        Category.objects.create(name='Demo category 3', parent=Category.objects.first())
        response = self.api_client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)
        mock_check_permissions.assert_called()

    @patch('category.views.check_permissions', return_value=True)
    def test_retrieve_category(self, mock_check_permissions):
        existing_category = Category.objects.create(name='New category', description='New category description')
        retrieve_url = reverse('categories-detail', args=[existing_category.id])
        response = self.api_client.get(retrieve_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'New category')
        mock_check_permissions.assert_called()