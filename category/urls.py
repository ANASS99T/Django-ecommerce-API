from rest_framework.routers import DefaultRouter
from django.urls import include, path

from category.views import CategoryViewSet


router = DefaultRouter()
router.register(r'', CategoryViewSet, basename='categories')

urlpatterns = [
    path('', include(router.urls)),
]