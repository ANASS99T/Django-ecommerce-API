from rest_framework.routers import DefaultRouter
from django.urls import include, path

from global_vars.views import GlobalVarsViewSet


router = DefaultRouter()
router.register(r'', GlobalVarsViewSet, basename='global_vars')

urlpatterns = [
    path('', include(router.urls)),
]