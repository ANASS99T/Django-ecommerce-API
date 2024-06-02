from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/clients/', include('user.urls')),
    path('api/roles/', include('roles.urls')),
    path('api/permissions/', include('permission.urls')),
    path('api/categories/', include('category.urls')),
    path('api/support/', include('support.urls')),

]
