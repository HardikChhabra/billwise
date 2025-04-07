from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('auth_app.urls')),
    path('api/customers/', include('customers_app.urls')),
    path('api/stores/', include('stores_app.urls')),
]