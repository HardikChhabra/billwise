from django.contrib import admin
from django.urls import path, include
from .views import readme_view
from django.views.generic.base import RedirectView

urlpatterns = [
    path('', readme_view, name="readme"),
    path('admin/', admin.site.urls),
    path('auth/', include('auth_app.urls')),
    path('customers/', include('customers_app.urls')),
    path('stores/', include('stores_app.urls')),
]