from rest_framework.routers import DefaultRouter
from django.urls import include, path

from roles.views import RoleViewSet


router = DefaultRouter()
router.register(r'', RoleViewSet, basename='roles')

urlpatterns = [
    path('', include(router.urls)),
]