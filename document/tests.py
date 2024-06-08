import os
import shutil
import tempfile
from tempfile import TemporaryDirectory
from unittest.mock import patch, MagicMock
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from category.models import Category
from ecommerce_api import settings
from product.models import Product
from .models import Document
from django.utils import timezone


class DocumentViewSetTestCase(TestCase):
    def setUp(self):
        self.url = reverse('documents-list')
        self.api_client = APIClient()
        self.category = Category.objects.create(name='Test Category')
        self.product = Product.objects.create(name='Test Product', description='Description test',
                                              category=self.category, price=100)

    def cleanUp(self, folder_to_delete):
        shutil.rmtree(folder_to_delete)

    @patch('document.views.check_permissions', return_value=True)
    def test_create_document_image(self, mock_check_permissions):
        with tempfile.TemporaryDirectory() as tmp_media:
            temp_media_root = os.path.join(tmp_media, settings.MEDIA_ROOT)
            with self.settings(MEDIA_ROOT=temp_media_root):
                dummy_file = SimpleUploadedFile('test.jpg', b'file_content', content_type='image/jpeg')
                data = {
                    'name': dummy_file.name,
                    'path': dummy_file,
                    'size': dummy_file.size,
                    'document_type': 'Image',
                    'dimension': '100x100',
                    'is_main': True,
                    'product': self.product.id,
                    'status': True
                }

                response = self.api_client.post(self.url, data, format='multipart')
                document = response.data
                self.assertEqual(response.status_code, status.HTTP_201_CREATED)
                self.assertEqual(document['name'], dummy_file.name)
                self.assertEqual(document['document_type'], 'Image')
                self.assertEqual(document['size'], dummy_file.size)
                self.assertEqual(document['dimension'], '100x100')
                self.assertEqual(document['status'], True)
                self.assertEqual(document['is_main'], True)

                mock_check_permissions.assert_called()

    @patch('document.views.check_permissions', return_value=True)
    def test_create_document_video(self, mock_check_permissions):
        with tempfile.TemporaryDirectory() as tmp_media:
            temp_media_root = os.path.join(tmp_media, settings.MEDIA_ROOT)
            with self.settings(MEDIA_ROOT=temp_media_root):
                dummy_file = SimpleUploadedFile('test.mp4', b'file_content', content_type='video/mp4')
                data = {
                    'name': dummy_file.name,
                    'path': dummy_file,
                    'size': dummy_file.size,
                    'document_type': 'Video',
                    'is_main': True,
                    'product': self.product.id,
                    'status': True
                }

                response = self.api_client.post(self.url, data, format='multipart')
                document = response.data
                self.assertEqual(response.status_code, status.HTTP_201_CREATED)
                self.assertEqual(document['name'], dummy_file.name)
                self.assertEqual(document['document_type'], 'Video')
                self.assertEqual(document['size'], dummy_file.size)
                self.assertEqual(document['status'], True)
                self.assertEqual(document['is_main'], True)
                mock_check_permissions.assert_called()

    @patch('document.views.check_permissions', return_value=True)
    def test_create_document_pdf(self, mock_check_permissions):
        with tempfile.TemporaryDirectory() as tmp_media:
            temp_media_root = os.path.join(tmp_media, settings.MEDIA_ROOT)
            with self.settings(MEDIA_ROOT=temp_media_root):
                dummy_file = SimpleUploadedFile('test.pdf', b'file_content', content_type='application/pdf')
                data = {
                    'name': dummy_file.name,
                    'path': dummy_file,
                    'size': dummy_file.size,
                    'document_type': 'PDF',
                    'is_main': True,
                    'product': self.product.id,
                    'status': True
                }

                response = self.api_client.post(self.url, data, format='multipart')
                document = response.data
                self.assertEqual(document['name'], dummy_file.name)
                self.assertEqual(document['document_type'], 'PDF')
                self.assertEqual(document['size'], dummy_file.size)
                self.assertEqual(document['status'], True)
                self.assertEqual(document['is_main'], True)

                self.assertEqual(response.status_code, status.HTTP_201_CREATED)
                mock_check_permissions.assert_called()

    @patch('document.views.check_permissions', return_value=True)
    def test_update_document(self, mock_check_permissions):
        with tempfile.TemporaryDirectory() as tmp_media:
            temp_media_root = os.path.join(tmp_media, settings.MEDIA_ROOT)
            with self.settings(MEDIA_ROOT=temp_media_root):
                dummy_file = SimpleUploadedFile('test.jpg', b'file_content', content_type='image/jpeg')
                document = Document.objects.create(name=dummy_file.name, path=dummy_file, size=dummy_file.size,
                                                   document_type='Image', product=self.product, status=True, is_main=True)
                update_url = reverse('documents-detail', args=[document.id])
                dummy_file = SimpleUploadedFile('test1.jpg', b'file_content', content_type='image/jpeg')
                data = {
                    'name': dummy_file.name,
                    'path': dummy_file,
                    'size': dummy_file.size,
                    'document_type': 'Image',
                    'is_main': True,
                    'product': self.product.id,
                    'status': True
                }

                response = self.api_client.put(update_url, data, format='multipart')
                document = response.data
                self.assertEqual(response.status_code, status.HTTP_200_OK)
                self.assertEqual(document['name'], dummy_file.name)
                self.assertEqual(document['document_type'], 'Image')
                self.assertEqual(document['size'], dummy_file.size)
                self.assertEqual(document['status'], True)
                self.assertEqual(document['is_main'], True)
                mock_check_permissions.assert_called()

    @patch('document.views.check_permissions', return_value=True)
    def test_delete_document(self, mock_check_permissions):
        with tempfile.TemporaryDirectory() as tmp_media:
            temp_media_root = os.path.join(tmp_media, settings.MEDIA_ROOT)
            temp_deleted_media_root = os.path.join(settings.MEDIA_ROOT, 'temp_deleted')
            with self.settings(MEDIA_ROOT=temp_media_root, DELETED_MEDIA_ROOT=temp_deleted_media_root):
                dummy_file = SimpleUploadedFile('test.jpg', b'file_content', content_type='image/jpeg')
                document = Document.objects.create(name=dummy_file.name, path=dummy_file, size=dummy_file.size,
                                                   document_type='Image', product=self.product, status=True,
                                                   is_main=True)
                delete_url = reverse('documents-detail', args=[document.id])
                response = self.api_client.delete(delete_url)
                document.refresh_from_db()
                self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
                self.assertFalse(document.deleted_at is None)
                self.assertFalse(document.status is True)
                mock_check_permissions.assert_called()
                self.cleanUp(temp_deleted_media_root)

    @patch('document.views.check_permissions', return_value=True)
    def test_list_document(self, mock_check_permissions):
        with tempfile.TemporaryDirectory() as tmp_media:
            temp_media_root = os.path.join(tmp_media, settings.MEDIA_ROOT)
            with self.settings(MEDIA_ROOT=temp_media_root):
                dummy_file = SimpleUploadedFile('test.jpg', b'file_content', content_type='image/jpeg')
                dummy_video = SimpleUploadedFile('test.mp4', b'file_content', content_type='video/mp4')
                dummy_pdf = SimpleUploadedFile('test.pdf', b'file_content', content_type='application/pdf')
                Document.objects.create(name=dummy_file.name, path=dummy_file, size=dummy_file.size,
                                        document_type='Image', product=self.product, status=True, is_main=True)
                Document.objects.create(name=dummy_file.name, path=dummy_file, size=dummy_file.size,
                                        document_type='Image', product=self.product, status=True, is_main=True)
                Document.objects.create(name=dummy_file.name, path=dummy_file, size=dummy_file.size,
                                        document_type='Image', product=self.product, status=True, is_main=True,
                                        deleted_at=timezone.now())
                Document.objects.create(name=dummy_file.name, path=dummy_file, size=dummy_file.size,
                                        document_type='Image', product=self.product, status=True, is_main=True,
                                        deleted_at=timezone.now())
                Document.objects.create(name=dummy_video.name, path=dummy_video, size=dummy_video.size,
                                        document_type='Video', product=self.product, status=True, is_main=True)
                Document.objects.create(name=dummy_pdf.name, path=dummy_pdf, size=dummy_pdf.size,
                                        document_type='PDF', product=self.product, status=True, is_main=True)

                response = self.api_client.get(self.url)
                self.assertEqual(response.status_code, status.HTTP_200_OK)
                self.assertEqual(len(response.data), 4)
                mock_check_permissions.assert_called()

    @patch('document.views.check_permissions', return_value=True)
    def test_retrieve_document(self, mock_check_permissions):
        with tempfile.TemporaryDirectory() as tmp_media:
            temp_media_root = os.path.join(tmp_media, settings.MEDIA_ROOT)
            with self.settings(MEDIA_ROOT=temp_media_root):
                dummy_file = SimpleUploadedFile('test.jpg', b'file_content', content_type='image/jpeg')
                dummy_video = SimpleUploadedFile('test.mp4', b'file_content', content_type='video/mp4')
                document = Document.objects.create(name=dummy_file.name, path=dummy_file, size=dummy_file.size,
                                                   document_type='Image', product=self.product, status=True,
                                                   is_main=True)
                Document.objects.create(name=dummy_video.name, path=dummy_video, size=dummy_video.size,
                                        document_type='Video', product=self.product, status=True, is_main=True)
                retrieve_url = reverse('documents-detail', args=[document.id])
                response = self.api_client.get(retrieve_url)
                self.assertEqual(response.status_code, status.HTTP_200_OK)
                self.assertEqual(response.data['name'], dummy_file.name)
                self.assertEqual(response.data['document_type'], 'Image')
                mock_check_permissions.assert_called()