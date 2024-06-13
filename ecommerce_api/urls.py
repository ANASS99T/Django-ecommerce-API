from django.contrib import admin
from django.urls import include, path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="API Docs",
        default_version='v1',
        description="API documentation",
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/clients/', include('user.urls')),
    path('api/roles/', include('roles.urls')),
    path('api/permissions/', include('permission.urls')),
    path('api/categories/', include('category.urls')),
    path('api/support/', include('support.urls')),
    path('api/characteristics/', include('characteristic.urls')),
    path('api/currencies/', include('currency.urls')),
    path('api/documents/', include('document.urls')),
    path('api/products/', include('product.urls')),
    path('api/cart/', include('cart.urls')),
    path('api/cartItem/', include('cartItem.urls')),
    path('api/global_vars/', include('global_vars.urls')),
    path('api/order/', include('order.urls')),

    path('api/docs/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]
