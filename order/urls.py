from rest_framework.routers import DefaultRouter
from django.urls import include, path

from order.views import OrderViewSet


router = DefaultRouter()
router.register(r'', OrderViewSet, basename='order')

urlpatterns = [
    path('', include(router.urls)),
]