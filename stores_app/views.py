from django.db.models import Sum, F, Value, FloatField, Q, Count
from django.db.models.functions import Coalesce
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView
from django.shortcuts import get_object_or_404
from .models import Product, Bill, BillItem
from auth_app.models import Customer
from .serializers import (
    ProductSerializer,
    BillSerializer,
    CreateBillSerializer,
    BasicCustomerSerializer,
    ProductAnalyticsSerializer,
    BillItemSerializer
)
from django.db.models import Sum, F, ExpressionWrapper, DecimalField, Count, Value, FloatField
from django.db.models.functions import Coalesce
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Product
from .serializers import ProductAnalyticsSerializer
from decimal import Decimal

class ProductListCreateView(ListCreateAPIView):
    serializer_class = ProductSerializer

    def get_queryset(self):
        store_id = self.request.store_id
        category = self.request.query_params.get('category', None)
        queryset = Product.objects.filter(store_id=store_id)
        
        if category:
            queryset = queryset.filter(category=category)
            
        return queryset.order_by('category', 'name')
    
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        
        # Group products by category
        categories = {}
        for product in queryset:
            if product.category not in categories:
                categories[product.category] = []
            categories[product.category].append(ProductSerializer(product).data)
        
        return Response(categories)
    
    def perform_create(self, serializer):
        serializer.save(store_id=self.request.store_id)

class ProductRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    serializer_class = ProductSerializer
    
    def get_queryset(self):
        return Product.objects.filter(store_id=self.request.store_id)

class CreateBillView(APIView):
    def post(self, request):
        serializer = CreateBillSerializer(data=request.data)
        if serializer.is_valid():
            store_id = request.store_id
            customer_id = serializer.validated_data.get('customer_id')
            items_data = serializer.validated_data.get('items')
            
            # Validate customer if provided
            customer = None
            if customer_id:
                try:
                    customer = Customer.objects.get(customer_id=customer_id)
                except Customer.DoesNotExist:
                    return Response(
                        {"error": "Customer not found"}, 
                        status=status.HTTP_404_NOT_FOUND
                    )
            
            # Create bill
            bill = Bill.objects.create(
                store_id=store_id,
                customer=customer,
                total_amount=0  # Will update after calculating items
            )
            
            total_amount = 0
            bill_items = []
            
            # Process each item
            for item_data in items_data:
                product_id = item_data.get('product_id')
                quantity = item_data.get('quantity', 1)
                
                try:
                    product = Product.objects.get(product_id=product_id, store_id=store_id)
                    
                    # Check stock
                    if product.stock < quantity:
                        bill.delete()  # Rollback if insufficient stock
                        return Response(
                            {"error": f"Insufficient stock for product: {product.name}"}, 
                            status=status.HTTP_400_BAD_REQUEST
                        )
                    
                    # Create bill item
                    price_at_sale = product.selling_price
                    bill_item = BillItem.objects.create(
                        product=product,
                        quantity=quantity,
                        price_at_sale=price_at_sale
                    )
                    bill_items.append(bill_item)
                    
                    # Update product stock and units sold
                    product.stock -= quantity
                    product.units_sold += quantity
                    product.save()
                    
                    # Add to total
                    item_total = price_at_sale * quantity
                    total_amount += item_total
                    
                except Product.DoesNotExist:
                    # Rollback the bill and all created items if any product not found
                    bill.delete()
                    return Response(
                        {"error": f"Product with ID {product_id} not found"}, 
                        status=status.HTTP_404_NOT_FOUND
                    )
            
            # Update bill total and connect items
            bill.total_amount = total_amount
            bill.save()
            bill.items.set(bill_items)
            
            return Response(
                BillSerializer(bill).data, 
                status=status.HTTP_201_CREATED
            )
            
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class BillListView(ListAPIView):
    serializer_class = BillSerializer
    
    def get_queryset(self):
        store_id = self.request.store_id
        product_name = self.request.query_params.get('product_name', None)
        
        queryset = Bill.objects.filter(store_id=store_id)
        
        if product_name:
            # Filter bills that contain the specified product
            queryset = queryset.filter(
                items__product__name__icontains=product_name
            ).distinct()
            
        return queryset.order_by('-created_at')

class BillDetailView(APIView):
    def get(self, request, bill_id):
        bill = get_object_or_404(Bill, bill_id=bill_id, store_id=request.store_id)
        return Response(BillSerializer(bill).data)

class ProductAnalyticsView(APIView):
    def get(self, request):
        store_id = request.store_id
        category = request.query_params.get('category', None)
        
        # Base queryset
        queryset = Product.objects.filter(store_id=store_id)
        
        # Filter by category if provided
        if category:
            queryset = queryset.filter(category=category)
        
        # Calculate metrics with proper annotations
        products = queryset.annotate(
            selling_price=ExpressionWrapper(
                F('cost') * (1 + F('profit_percent') / 100),
                output_field=DecimalField(max_digits=10, decimal_places=2)
            ),
            profit_per_unit=ExpressionWrapper(
                F('cost') * F('profit_percent') / 100,
                output_field=DecimalField(max_digits=10, decimal_places=2)
            ),
            total_revenue=ExpressionWrapper(
                F('selling_price') * F('units_sold'),
                output_field=DecimalField(max_digits=12, decimal_places=2)
            ),
            total_profit=ExpressionWrapper(
                F('profit_per_unit') * F('units_sold'),
                output_field=DecimalField(max_digits=12, decimal_places=2)
            )
        ).order_by('category', 'name')
        
        # For most and least selling products
        most_selling = products.order_by('-units_sold').first()
        least_selling = products.filter(units_sold__gt=0).order_by('units_sold').first()
        
        # Calculate category-wise metrics
        category_metrics = {}
        for product in products:
            cat = product.category
            if cat not in category_metrics:
                category_metrics[cat] = {
                    'total_revenue': Decimal('0.00'),
                    'total_profit': Decimal('0.00'),
                    'units_sold': 0,
                    'product_count': 0
                }
            
            category_metrics[cat]['total_revenue'] += product.total_revenue or Decimal('0.00')
            category_metrics[cat]['total_profit'] += product.total_profit or Decimal('0.00')
            category_metrics[cat]['units_sold'] += product.units_sold
            category_metrics[cat]['product_count'] += 1
        
        # Category-specific analytics if requested
        category_data = None
        if category and category in category_metrics:
            category_data = {
                'category': category,
                'total_products': category_metrics[category]['product_count'],
                'total_units_sold': category_metrics[category]['units_sold'],
                'total_revenue': float(category_metrics[category]['total_revenue']),
                'total_profit': float(category_metrics[category]['total_profit']),
                'average_profit_per_product': float(category_metrics[category]['total_profit'] / category_metrics[category]['product_count']) if category_metrics[category]['product_count'] > 0 else 0
            }
        
        # Format response
        response_data = {
            'most_selling_product': ProductAnalyticsSerializer(most_selling).data if most_selling else None,
            'least_selling_product': ProductAnalyticsSerializer(least_selling).data if least_selling else None,
            'categories_summary': {
                cat: {
                    'total_revenue': float(metrics['total_revenue']),
                    'total_profit': float(metrics['total_profit']),
                    'units_sold': metrics['units_sold'],
                    'product_count': metrics['product_count']
                } 
                for cat, metrics in category_metrics.items()
            }
        }
        
        if category_data:
            response_data['category_analytics'] = category_data
            
            # Add top 5 most profitable products in this category
            top_profitable = products.order_by('-total_profit')[:5]
            response_data['category_analytics']['top_profitable_products'] = ProductAnalyticsSerializer(top_profitable, many=True).data
        
        return Response(response_data)
    
class CategoryAnalyticsView(APIView):
    def get(self, request, category):
        store_id = request.store_id
        
        # Get all products in this category
        products = Product.objects.filter(
            store_id=store_id,
            category=category
        ).annotate(
            selling_price=ExpressionWrapper(
                F('cost') * (1 + F('profit_percent') / 100),
                output_field=DecimalField(max_digits=10, decimal_places=2)
            ),
            profit_per_unit=ExpressionWrapper(
                F('cost') * F('profit_percent') / 100,
                output_field=DecimalField(max_digits=10, decimal_places=2)
            ),
            total_revenue=ExpressionWrapper(
                F('selling_price') * F('units_sold'),
                output_field=DecimalField(max_digits=12, decimal_places=2)
            ),
            total_profit=ExpressionWrapper(
                F('profit_per_unit') * F('units_sold'),
                output_field=DecimalField(max_digits=12, decimal_places=2)
            )
        )
        
        if not products.exists():
            return Response(
                {"error": f"No products found in category: {category}"},
                status=status.HTTP_404_NOT_FOUND
            )
            
        # Calculate aggregate metrics
        total_revenue = sum(p.total_revenue or Decimal('0.00') for p in products)
        total_profit = sum(p.total_profit or Decimal('0.00') for p in products)
        total_units = sum(p.units_sold for p in products)
        
        # Get top selling and most profitable products
        top_selling = products.order_by('-units_sold')[:5]
        top_profitable = products.order_by('-total_profit')[:5]
        
        return Response({
            'category': category,
            'product_count': products.count(),
            'total_revenue': float(total_revenue),
            'total_profit': float(total_profit),
            'total_units_sold': total_units,
            'top_selling_products': ProductAnalyticsSerializer(top_selling, many=True).data,
            'top_profitable_products': ProductAnalyticsSerializer(top_profitable, many=True).data,
        })

class TopProductsView(APIView):
    def get(self, request):
        store_id = request.store_id
        metric = request.query_params.get('metric', 'profit')  # Default to profit
        limit = int(request.query_params.get('limit', 10))
        
        # Annotate products with calculated fields
        products = Product.objects.filter(store_id=store_id).annotate(
            selling_price=ExpressionWrapper(
                F('cost') * (1 + F('profit_percent') / 100),
                output_field=DecimalField(max_digits=10, decimal_places=2)
            ),
            profit_per_unit=ExpressionWrapper(
                F('cost') * F('profit_percent') / 100,
                output_field=DecimalField(max_digits=10, decimal_places=2)
            ),
            total_revenue=ExpressionWrapper(
                F('selling_price') * F('units_sold'),
                output_field=DecimalField(max_digits=12, decimal_places=2)
            ),
            total_profit=ExpressionWrapper(
                F('profit_per_unit') * F('units_sold'),
                output_field=DecimalField(max_digits=12, decimal_places=2)
            )
        )
        
        # Order by the appropriate metric
        if metric == 'profit':
            products = products.order_by('-total_profit')
        elif metric == 'revenue':
            products = products.order_by('-total_revenue')
        elif metric == 'units':
            products = products.order_by('-units_sold')
        else:
            return Response(
                {"error": "Invalid metric. Choose from: profit, revenue, units"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Limit results
        products = products[:limit]
        
        return Response({
            'metric': metric,
            'products': ProductAnalyticsSerializer(products, many=True).data
        })