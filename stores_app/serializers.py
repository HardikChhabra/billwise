from rest_framework import serializers
from .models import Product, Bill, BillItem
from auth_app.models import Customer

class ProductSerializer(serializers.ModelSerializer):
    selling_price = serializers.ReadOnlyField()
    
    class Meta:
        model = Product
        fields = [
            'product_id', 'name', 'cost', 'profit_percent', 
            'stock', 'category', 'units_sold', 'selling_price'
        ]
        read_only_fields = ['product_id', 'units_sold']

class BillItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)
    total_price = serializers.ReadOnlyField()
    
    class Meta:
        model = BillItem
        fields = ['bill_item_id', 'product', 'product_name', 'quantity', 'price_at_sale', 'total_price']
        read_only_fields = ['bill_item_id', 'price_at_sale']

class BillSerializer(serializers.ModelSerializer):
    items = BillItemSerializer(many=True, read_only=True)
    customer_name = serializers.CharField(source='customer.name', read_only=True)
    
    class Meta:
        model = Bill
        fields = ['bill_id', 'store', 'customer', 'customer_name', 'total_amount', 'created_at', 'items']
        read_only_fields = ['bill_id', 'store', 'total_amount', 'created_at']

class CreateBillSerializer(serializers.Serializer):
    customer_id = serializers.IntegerField(required=False, allow_null=True)
    items = serializers.ListField(
        child=serializers.DictField(
            child=serializers.IntegerField(),
            allow_empty=False
        ),
        allow_empty=False
    )

class BasicCustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['customer_id', 'name', 'phone']

class ProductAnalyticsSerializer(serializers.ModelSerializer):
    selling_price = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    profit_per_unit = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    total_revenue = serializers.DecimalField(max_digits=12, decimal_places=2, read_only=True)
    total_profit = serializers.DecimalField(max_digits=12, decimal_places=2, read_only=True)
    
    class Meta:
        model = Product
        fields = [
            'product_id', 'name', 'category', 'units_sold', 
            'selling_price', 'profit_per_unit', 'total_revenue', 'total_profit'
        ]