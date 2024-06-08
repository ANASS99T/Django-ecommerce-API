from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from category.serializer import CategorySerializer
from characteristic.serializer import CharacteristicSerializer
from currency.serializer import CurrencySerializer
from document.serializer import DocumentSerializer
from helpers.permission_helpers import unauthorized, check_permissions, check_auth
from product.models import Product
from product.serializer import ProductSerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.filter(deleted_at__isnull=True)
    serializer_class = ProductSerializer

    def create(self, request, *args, **kwargs):
        if not check_permissions(request, 'can_create_product'):
            return unauthorized()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(status=False)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        if not check_permissions(request, 'can_update_product'):
            return unauthorized()
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(
            serializer.data)

    def destroy(self, request, *args, **kwargs):
        if not check_permissions(request, 'can_delete_product'):
            return unauthorized()
        role = self.get_object()
        role.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def list(self, request, *args, **kwargs):
        if not check_permissions(request, 'can_view_product_list'):
            return unauthorized()
        return super().list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        if not check_permissions(request, 'can_view_product'):
            return unauthorized()
        product = self.get_object()
        categpry = product.category
        currency = product.currency
        documents = product.documents.filter(deleted_at__isnull=True)
        characteristics = product.characteristics.filter(deleted_at__isnull=True)

        product_serializer = ProductSerializer(product)
        categpry_serializer = CategorySerializer(categpry)
        currency_serializer = CurrencySerializer(currency)
        documents_serializer = DocumentSerializer(documents, many=True)
        characteristics_serializer = CharacteristicSerializer(characteristics, many=True)

        return Response(
            data={'product': product_serializer.data,
                  'category': categpry_serializer.data,
                  'currency': currency_serializer.data,
                  'documents': documents_serializer.data,
                  'characteristics': characteristics_serializer.data},
            status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    def validate(self, request, *args, **kwargs):
        if not check_permissions(request, 'can_validate_product'):
            return unauthorized()
        is_main = False
        image_exist = False

        product = self.get_object()
        category = product.category
        if not category:
            return Response(data={'message': 'Product has no category'}, status=status.HTTP_400_BAD_REQUEST)

        if not product.currency:
            return Response(data={'message': 'Product has no currency'}, status=status.HTTP_400_BAD_REQUEST)

        documents = product.documents.all()
        if not documents:
            return Response(data={'message': 'Product has no document'}, status=status.HTTP_400_BAD_REQUEST)
        for document in documents:
            if document.document_type == 'Image':
                image_exist = True
                if document.is_main:
                    is_main = True
                    break
        if not image_exist:
            return Response(data={'message': 'Product has no image'}, status=status.HTTP_400_BAD_REQUEST)
        if not is_main:
            return Response(data={'message': 'Product has no main image'}, status=status.HTTP_400_BAD_REQUEST)

        characteristics = product.characteristics.all()
        if not characteristics:
            return Response(data={'message': 'Product has no characteristics'}, status=status.HTTP_400_BAD_REQUEST)

        product.status = True
        product.save()
        return Response(data={'message': 'Product validated'}, status=status.HTTP_200_OK)
