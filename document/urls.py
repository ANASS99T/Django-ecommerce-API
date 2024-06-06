from rest_framework.routers import DefaultRouter
from django.urls import include, path

from document.views import DocumentViewSet


router = DefaultRouter()
router.register(r'', DocumentViewSet, basename='documents')

urlpatterns = [
    path('', include(router.urls)),
]