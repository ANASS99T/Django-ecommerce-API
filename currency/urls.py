from rest_framework.routers import DefaultRouter
from django.urls import include, path

from currency.views import CurrencyViewSet


router = DefaultRouter()
router.register(r'', CurrencyViewSet, basename='currencies')

urlpatterns = [
    path('', include(router.urls)),
]