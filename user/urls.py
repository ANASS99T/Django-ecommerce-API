from rest_framework.routers import DefaultRouter
from django.urls import include, path

from user.views import ClientViewSet


router = DefaultRouter()
router.register(r'', ClientViewSet, basename='clients')

urlpatterns = [
    path('', include(router.urls)),
]