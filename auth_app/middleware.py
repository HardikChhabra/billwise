import jwt
from django.conf import settings
from django.http import JsonResponse
from .models import Store, Customer

class JWTAuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Exclude auth endpoints from token validation
        if request.path.startswith('/api/auth/'):
            return self.get_response(request)

        # Check for Authorization header
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return JsonResponse({"error": "Authorization header missing or invalid"}, status=401)

        token = auth_header.split(' ')[1]
        try:
            payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
            email = payload.get('email')
            user_type = payload.get('user_type')

            # Add user info to request
            request.user_email = email
            request.user_type = user_type

            # For store-specific endpoints, validate the store
            if user_type == 'store' and request.path.startswith('/stores/'):
                try:
                    store = Store.objects.get(email=email)
                    request.store_id = store.store_id
                except Store.DoesNotExist:
                    return JsonResponse({"error": "Invalid store credentials"}, status=401)
            
            # For customer-specific endpoints, validate the customer
            elif user_type == 'customer' and request.path.startswith('/customers/'):
                try:
                    customer = Customer.objects.get(email=email)
                    request.customer_id = customer.customer_id
                except Customer.DoesNotExist:
                    return JsonResponse({"error": "Invalid customer credentials"}, status=401)

        except jwt.ExpiredSignatureError:
            return JsonResponse({"error": "Token expired"}, status=401)
        except jwt.InvalidTokenError:
            return JsonResponse({"error": "Invalid token"}, status=401)

        return self.get_response(request)