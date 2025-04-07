from rest_framework import serializers
from auth_app.models import Customer
from stores_app.models import Bill
from stores_app.serializers import BillSerializer

class CustomerProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['customer_id', 'email', 'phone', 'name', 'address']
        read_only_fields = ['customer_id']

class CustomerBillSerializer(serializers.ModelSerializer):
    store_name = serializers.CharField(source='store.name', read_only=True)
    
    class Meta:
        model = Bill
        fields = ['bill_id', 'store_name', 'total_amount', 'created_at']