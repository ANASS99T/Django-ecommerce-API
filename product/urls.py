from rest_framework.routers import DefaultRouter
from django.urls import include, path

from product.views import ProductViewSet


router = DefaultRouter()
router.register(r'', ProductViewSet, basename='products')

urlpatterns = [
    path('', include(router.urls)),
]