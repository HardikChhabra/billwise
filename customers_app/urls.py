from django.urls import path
from .views import (
    CustomerBillsView,
    CustomerBillDetailView
)

urlpatterns = [
    path('bills/', CustomerBillsView.as_view(), name='customer-bills'),
    path('bills/<int:bill_id>/', CustomerBillDetailView.as_view(), name='customer-bill-detail'),
]