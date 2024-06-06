from rest_framework import viewsets, status
from rest_framework.response import Response

from helpers.permission_helpers import unauthorized, check_permissions, check_auth
from document.models import Document
from document.serializer import DocumentSerializer
from product.models import Product


class DocumentViewSet(viewsets.ModelViewSet):
    queryset = Document.objects.filter(deleted_at__isnull=True)
    serializer_class = DocumentSerializer

    def create(self, request, *args, **kwargs):
        if not check_permissions(request, 'can_create_document'):
            return unauthorized()

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        if not check_permissions(request, 'can_update_document'):
            return unauthorized()
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        if not check_permissions(request, 'can_delete_document'):
            return unauthorized()
        try:
            document = self.get_object()
            if document.delete():
                return Response(status=status.HTTP_204_NO_CONTENT)
            else:
                return Response({'error': 'Error deleting the document'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request, *args, **kwargs):
        if not check_permissions(request, 'can_view_document_list'):
            return unauthorized()
        return super().list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        if not check_permissions(request, 'can_view_document'):
            return unauthorized()
        return super().retrieve(request, *args, **kwargs)
