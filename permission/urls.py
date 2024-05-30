from rest_framework.routers import DefaultRouter
from django.urls import include, path

from permission.views import PermissionViewSet


router = DefaultRouter()
router.register(r'', PermissionViewSet, basename='permissions')

urlpatterns = [
    path('', include(router.urls)),
]