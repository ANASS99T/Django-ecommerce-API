from rest_framework.routers import DefaultRouter
from django.urls import include, path

from cartItem.views import CartItemViewSet


router = DefaultRouter()
router.register(r'', CartItemViewSet, basename='cartItem')

urlpatterns = [
    path('', include(router.urls)),
]