from django.urls import path
from .views import (
    ProductListCreateView,
    ProductRetrieveUpdateDestroyView,
    CreateBillView,
    BillListView,
    BillDetailView,
    ProductAnalyticsView,
    CategoryAnalyticsView,
    TopProductsView
)

urlpatterns = [
    path('products/', ProductListCreateView.as_view(), name='product-list-create'),
    path('products/<int:pk>/', ProductRetrieveUpdateDestroyView.as_view(), name='product-detail'),
    path('bills/create/', CreateBillView.as_view(), name='create-bill'),
    path('bills/', BillListView.as_view(), name='bill-list'),
    path('bills/<int:bill_id>/', BillDetailView.as_view(), name='bill-detail'),
    path('analytics/products/', ProductAnalyticsView.as_view(), name='product-analytics'),
    path('analytics/category/<str:category>/', CategoryAnalyticsView.as_view(), name='category-analytics'),
    path('analytics/top-products/', TopProductsView.as_view(), name='top-products'),
]