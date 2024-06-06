from rest_framework.routers import DefaultRouter
from django.urls import include, path

from characteristic.views import CharacteristicViewSet


router = DefaultRouter()
router.register(r'', CharacteristicViewSet, basename='characteristics')

urlpatterns = [
    path('', include(router.urls)),
]