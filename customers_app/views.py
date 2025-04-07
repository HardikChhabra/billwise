from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import RetrieveUpdateAPIView, ListAPIView
from auth_app.models import Customer
from stores_app.models import Bill
from .serializers import CustomerProfileSerializer, CustomerBillSerializer

class CustomerBillsView(ListAPIView):
    serializer_class = CustomerBillSerializer
    
    def get_queryset(self):
        return Bill.objects.filter(
            customer_id=self.request.customer_id
        ).order_by('-created_at')

class CustomerBillDetailView(APIView):
    def get(self, request, bill_id):
        bill = Bill.objects.filter(
            bill_id=bill_id, 
            customer_id=request.customer_id
        ).first()
        
        if not bill:
            return Response(
                {"error": "Bill not found"}, 
                status=status.HTTP_404_NOT_FOUND
            )
        
        from stores_app.serializers import BillSerializer
        return Response(BillSerializer(bill).data)
