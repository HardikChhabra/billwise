from django.urls import path
from .views import (
    StoreLoginView,
    StoreRegisterView,
    CustomerLoginView,
    CustomerRegisterView
)

urlpatterns = [
    path('stores/login/', StoreLoginView.as_view(), name='store-login'),
    path('stores/register/', StoreRegisterView.as_view(), name='store-register'),
    path('customer/login/', CustomerLoginView.as_view(), name='customer-login'),
    path('customer/register/', CustomerRegisterView.as_view(), name='customer-register'),
]