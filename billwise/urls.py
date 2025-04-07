from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('auth_app.urls')),
    path('customers/', include('customers_app.urls')),
    path('stores/', include('stores_app.urls')),
]