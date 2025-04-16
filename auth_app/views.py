import jwt
from datetime import datetime
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Store, Customer
from .serializers import (
    StoreLoginSerializer, 
    StoreRegisterSerializer,
    CustomerLoginSerializer,
    CustomerRegisterSerializer
)

class StoreLoginView(APIView):
    def post(self, request):
        serializer = StoreLoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']
            
            try:
                store = Store.objects.get(email=email)
                if store.check_password(password):
                    # Generate JWT token
                    payload = {
                        'email': email,
                        'user_type': 'store',
                        'exp': datetime.utcnow() + settings.JWT_EXPIRATION_DELTA
                    }
                    token = jwt.encode(payload, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
                    
                    return Response({
                        'token': token,
                        'store_id': store.store_id,
                        'name': store.name
                    }, status=status.HTTP_200_OK)
                else:
                    return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
            except Store.DoesNotExist:
                return Response({'error': 'Store not found'}, status=status.HTTP_404_NOT_FOUND)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class StoreRegisterView(APIView):
    def post(self, request):
        serializer = StoreRegisterSerializer(data=request.data)
        if serializer.is_valid():
            store = serializer.save()
            
            # Generate JWT token
            payload = {
                'email': store.email,
                'user_type': 'store',
                'exp': datetime.utcnow() + settings.JWT_EXPIRATION_DELTA
            }
            token = jwt.encode(payload, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
            
            return Response({
                'token': token,
                'store_id': store.store_id,
                'name': store.name
            }, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CustomerLoginView(APIView):
    def post(self, request):
        serializer = CustomerLoginSerializer(data=request.data)
        if serializer.is_valid():
            phone = serializer.validated_data['phone']
            password = serializer.validated_data['password']
            
            try:
                customer = Customer.objects.get(phone=phone)
                if customer.check_password(password):
                    # Generate JWT token
                    payload = {
                        'email': customer.email,
                        'user_type': 'customer',
                        'exp': datetime.utcnow() + settings.JWT_EXPIRATION_DELTA
                    }
                    token = jwt.encode(payload, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
                    
                    return Response({
                        'token': token,
                        'customer_id': customer.customer_id,
                        'name': customer.name
                    }, status=status.HTTP_200_OK)
                else:
                    return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
            except Customer.DoesNotExist:
                return Response({'error': 'Customer not found'}, status=status.HTTP_404_NOT_FOUND)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CustomerRegisterView(APIView):
    def post(self, request):
        serializer = CustomerRegisterSerializer(data=request.data)
        if serializer.is_valid():
            customer = serializer.save()
            
            # Generate JWT token
            payload = {
                'email': customer.email,
                'user_type': 'customer',
                'exp': datetime.utcnow() + settings.JWT_EXPIRATION_DELTA
            }
            token = jwt.encode(payload, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
            
            return Response({
                'token': token,
                'customer_id': customer.customer_id,
                'name': customer.name
            }, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)