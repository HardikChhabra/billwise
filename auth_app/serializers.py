from rest_framework import serializers
from .models import Store, Customer

class StoreLoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True, write_only=True)

class StoreRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    
    class Meta:
        model = Store
        fields = ['email', 'password', 'name', 'location']
        extra_kwargs = {
            'email': {'required': True},
            'name': {'required': True},
            'location': {'required': True},
        }

class CustomerLoginSerializer(serializers.Serializer):
    phone = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)

class CustomerRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    
    class Meta:
        model = Customer
        fields = ['email', 'password', 'phone', 'name', 'address']
        extra_kwargs = {
            'phone': {'required': True},
            'name': {'required': True},
            'address': {'required': True},
        }