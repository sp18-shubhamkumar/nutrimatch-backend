from rest_framework.views import APIView
from rest_framework.response import Response
from ..models import Customer
from ..permissions import IsCustomer
from ..serializers import CustomerSerializer
from drf_yasg.utils import swagger_auto_schema


class CustomerProfileView(APIView):
    permission_classes = [IsCustomer]

    def get(self, request):
        try:
            customer = request.user.customer_profile
        except Customer.DoesNotExist:
            return Response({"error": "Customer profile not found."}, status=404)

        serializer = CustomerSerializer(customer)
        return Response(serializer.data, status=200)

    @swagger_auto_schema(request_body=CustomerSerializer)
    def put(self, request):
        try:
            customer = request.user.customer_profile
        except Customer.DoesNotExist:
            return Response({"error": "Customer profile not found."}, status=404)

        serializer = CustomerSerializer(customer, request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)
        return Response(serializer.errors, status=400)

    def delete(self, request):
        try:
            customer = request.user.customer_profile
        except Customer.DoesNotExist:
            return Response({"error": "Customer profile not found."}, status=404)

        user = request.user
        customer.delete()
        user.delete()

        return Response({"message": "Customer profile deleted successfully."}, status=204)
