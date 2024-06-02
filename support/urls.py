from rest_framework.routers import DefaultRouter
from django.urls import include, path

from support.views import SupportViewSet


router = DefaultRouter()
router.register(r'', SupportViewSet, basename='support')

urlpatterns = [
    path('', include(router.urls)),
]