import os
import tempfile
from tempfile import TemporaryDirectory
from unittest.mock import patch

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from category.models import Category
from characteristic.models import Characteristic
from currency.models import Currency
from document.models import Document
from ecommerce_api import settings
from .models import Product
from django.utils import timezone


class ProductViewSetTestCase(TestCase):
    def setUp(self):
        self.url = reverse('products-list')
        self.api_client = APIClient()
        self.category = Category.objects.create(name='Test Category')
        self.currency = Currency.objects.create(code='USD', name='USD', symbol='$')
        self.data = {
            'name': 'Test Product',
            'description': 'Description test',
            'category': self.category.id,
            'price': 100
        }

    @patch('product.views.check_permissions', return_value=True)
    def test_create_product(self, mock_check_permissions):
        response = self.api_client.post(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        new_product = response.data
        self.assertEqual(new_product['name'], 'Test Product')
        mock_check_permissions.assert_called()

    @patch('product.views.check_permissions', return_value=True)
    def test_update_product(self, mock_check_permissions):
        existing = Product.objects.create(name=self.data['name'], description=self.data['description'],
                                          category=self.category, price=self.data['price'])
        update_url = reverse('products-detail', args=[existing.id])
        update_data = {
            'name': 'Updated product name',
        }
        response = self.api_client.put(update_url, update_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        updated_data = response.data
        self.assertEqual(updated_data['name'], 'Updated product name')
        mock_check_permissions.assert_called()

    @patch('product.views.check_permissions', return_value=True)
    def test_delete_product(self, mock_check_permissions):
        existing = Product.objects.create(name=self.data['name'], description=self.data['description'],
                                          category=self.category, price=self.data['price'])
        delete_url = reverse('products-detail', args=[existing.id])
        response = self.api_client.delete(delete_url)
        existing.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(existing.deleted_at is None)
        self.assertFalse(existing.status is True)
        mock_check_permissions.assert_called()

    @patch('product.views.check_permissions', return_value=True)
    def test_list_product(self, mock_check_permissions):
        Product.objects.create(name=self.data['name'], description=self.data['description'],
                               category=self.category, price=self.data['price'])
        Product.objects.create(name='prod2', description='desc2',
                               category=self.category, price=500.43)
        Product.objects.create(name='prod3', description='desc3',
                               category=self.category, price=999.99, deleted_at=timezone.now())
        response = self.api_client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        mock_check_permissions.assert_called()

    @patch('product.views.check_permissions', return_value=True)
    def test_retrieve_product(self, mock_check_permissions):
        with tempfile.TemporaryDirectory() as tmp_media:
            temp_media_root = os.path.join(tmp_media, settings.MEDIA_ROOT)
            with self.settings(MEDIA_ROOT=temp_media_root):
                product = Product.objects.create(name=self.data['name'], description=self.data['description'],
                                                 category=self.category, price=self.data['price'], currency=self.currency)

                dummy_file1 = SimpleUploadedFile('test.jpg', b'file_content', content_type='image/jpeg')
                Document.objects.create(name=dummy_file1.name, path=dummy_file1, size=dummy_file1.size,
                                        document_type='Image', product=product, status=True, is_main=True)

                dummy_file2 = SimpleUploadedFile('test2.jpg', b'file_content', content_type='image/jpeg')
                Document.objects.create(name=dummy_file2.name, path=dummy_file2, size=dummy_file2.size,
                                        document_type='Image', product=product, status=True, is_main=False)

                Characteristic.objects.create(key='model', value='2022', product=product)

                retrieve_url = reverse('products-detail', args=[product.id])
                response = self.api_client.get(retrieve_url)
                self.assertEqual(response.status_code, status.HTTP_200_OK)
                self.assertEqual(response.data['product']['name'], self.data['name'])
                self.assertEqual(response.data['product']['status'], False)
                mock_check_permissions.assert_called()

    @patch('product.views.check_permissions', return_value=True)
    def test_validate_product(self, mock_check_permissions):
        with tempfile.TemporaryDirectory() as tmp_media:
            temp_media_root = os.path.join(tmp_media, settings.MEDIA_ROOT)
            with self.settings(MEDIA_ROOT=temp_media_root):
                product = Product.objects.create(name=self.data['name'], description=self.data['description'],
                                                 category=self.category, price=self.data['price'], currency=self.currency)

                dummy_file1 = SimpleUploadedFile('test.jpg', b'file_content', content_type='image/jpeg')
                Document.objects.create(name=dummy_file1.name, path=dummy_file1, size=dummy_file1.size,
                                        document_type='Image', product=product, status=True, is_main=True)

                dummy_file2 = SimpleUploadedFile('test2.jpg', b'file_content', content_type='image/jpeg')
                Document.objects.create(name=dummy_file2.name, path=dummy_file2, size=dummy_file2.size,
                                        document_type='Image', product=product, status=True, is_main=False)

                Characteristic.objects.create(key='model', value='2022', product=product)
                validate_url = reverse('products-validate', args=[product.id])

                response = self.api_client.post(validate_url)
                product.refresh_from_db()
                self.assertEqual(response.status_code, status.HTTP_200_OK)
                self.assertEqual(product.status, True)
                mock_check_permissions.assert_called()

    @patch('product.views.check_permissions', return_value=True)
    def test_validate_product_fail_currency(self, mock_check_permissions):
        product = Product.objects.create(name=self.data['name'], description=self.data['description'],
                                         category=self.category, price=self.data['price'])

        validate_url = reverse('products-validate', args=[product.id])

        response = self.api_client.post(validate_url)
        product.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['message'], 'Product has no currency')
        self.assertEqual(product.status, False)
        mock_check_permissions.assert_called()

    @patch('product.views.check_permissions', return_value=True)
    def test_validate_product_fail_documents(self, mock_check_permissions):
        product = Product.objects.create(name=self.data['name'], description=self.data['description'],
                                         category=self.category, price=self.data['price'], currency=self.currency)

        validate_url = reverse('products-validate', args=[product.id])

        response = self.api_client.post(validate_url)
        product.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['message'], 'Product has no document')
        self.assertEqual(product.status, False)
        mock_check_permissions.assert_called()

    @patch('product.views.check_permissions', return_value=True)
    def test_validate_product_fail_image(self, mock_check_permissions):
        with tempfile.TemporaryDirectory() as tmp_media:
            temp_media_root = os.path.join(tmp_media, settings.MEDIA_ROOT)
            with self.settings(MEDIA_ROOT=temp_media_root):
                product = Product.objects.create(name=self.data['name'], description=self.data['description'],
                                                 category=self.category, price=self.data['price'], currency=self.currency)

                dummy_file1 = SimpleUploadedFile('test.mp4', b'file_content', content_type='video/mp4')
                Document.objects.create(name=dummy_file1.name, path=dummy_file1, size=dummy_file1.size,
                                        document_type='Video', product=product, status=True, is_main=True)

                validate_url = reverse('products-validate', args=[product.id])

                response = self.api_client.post(validate_url)
                product.refresh_from_db()
                self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
                self.assertEqual(response.data['message'], 'Product has no image')
                self.assertEqual(product.status, False)
                mock_check_permissions.assert_called()

    @patch('product.views.check_permissions', return_value=True)
    def test_validate_product_fail_image_main(self, mock_check_permissions):
        with tempfile.TemporaryDirectory() as tmp_media:
            temp_media_root = os.path.join(tmp_media, settings.MEDIA_ROOT)
            with self.settings(MEDIA_ROOT=temp_media_root):
                product = Product.objects.create(name=self.data['name'], description=self.data['description'],
                                                 category=self.category, price=self.data['price'], currency=self.currency)

                dummy_file1 = SimpleUploadedFile('test.jpg', b'file_content', content_type='image/jpeg')
                Document.objects.create(name=dummy_file1.name, path=dummy_file1, size=dummy_file1.size,
                                        document_type='Image', product=product, status=True, is_main=False)

                validate_url = reverse('products-validate', args=[product.id])

                response = self.api_client.post(validate_url)
                product.refresh_from_db()
                self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
                self.assertEqual(response.data['message'], 'Product has no main image')
                self.assertEqual(product.status, False)
                mock_check_permissions.assert_called()

        @patch('product.views.check_permissions', return_value=True)
        def test_validate_product_fail_image_main(self, mock_check_permissions):
            with tempfile.TemporaryDirectory() as tmp_media:
                temp_media_root = os.path.join(tmp_media, settings.MEDIA_ROOT)
                with self.settings(MEDIA_ROOT=temp_media_root):
                    product = Product.objects.create(name=self.data['name'], description=self.data['description'],
                                                     category=self.category, price=self.data['price'], currency=self.currency)

                    dummy_file1 = SimpleUploadedFile('test.jpg', b'file_content', content_type='image/jpeg')
                    Document.objects.create(name=dummy_file1.name, path=dummy_file1, size=dummy_file1.size,
                                            document_type='Image', product=product, status=True, is_main=False)

                    validate_url = reverse('products-validate', args=[product.id])

                    response = self.api_client.post(validate_url)
                    product.refresh_from_db()
                    self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
                    self.assertEqual(response.data['message'], 'Product has no main image')
                    self.assertEqual(product.status, False)
                    mock_check_permissions.assert_called()

    @patch('product.views.check_permissions', return_value=True)
    def test_validate_product_fail_characteristics(self, mock_check_permissions):
        with tempfile.TemporaryDirectory() as tmp_media:
            temp_media_root = os.path.join(tmp_media, settings.MEDIA_ROOT)
            with self.settings(MEDIA_ROOT=temp_media_root):
                product = Product.objects.create(name=self.data['name'], description=self.data['description'],
                                                 category=self.category, price=self.data['price'], currency=self.currency)

                dummy_file1 = SimpleUploadedFile('test.jpg', b'file_content', content_type='image/jpeg')
                Document.objects.create(name=dummy_file1.name, path=dummy_file1, size=dummy_file1.size,
                                        document_type='Image', product=product, status=True, is_main=True)

                validate_url = reverse('products-validate', args=[product.id])

                response = self.api_client.post(validate_url)
                product.refresh_from_db()
                self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
                self.assertEqual(response.data['message'], 'Product has no characteristics')
                self.assertEqual(product.status, False)
                mock_check_permissions.assert_called()

