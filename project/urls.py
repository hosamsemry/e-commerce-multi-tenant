
from django.contrib import admin
from django.urls import path, include, re_path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('apps.tenancy.urls')),
    path("api/accounts/", include("apps.accounts.urls")),
    re_path(r'^auth/', include('djoser.urls')),
    path("api/", include("apps.products.urls")),
    path("api/", include("apps.orders.urls")),
]
