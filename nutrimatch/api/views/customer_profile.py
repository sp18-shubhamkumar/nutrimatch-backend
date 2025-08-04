from rest_framework.views import APIView
from rest_framework.response import Response
from ..models import Customer
from ..permissions import IsCustomer
from ..serializers import CustomerSerializer
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status


class CustomerProfileView(APIView):
    permission_classes = [IsCustomer]

    def get(self, request):
        try:
            customer = request.user.customer_profile
        except Customer.DoesNotExist:
            return Response({"error": "Customer profile not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = CustomerSerializer(customer)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(request_body=CustomerSerializer)
    def put(self, request):
        try:
            customer = request.user.customer_profile
        except Customer.DoesNotExist:
            return Response({"error": "Customer profile not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = CustomerSerializer(customer, request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        try:
            customer = request.user.customer_profile
        except Customer.DoesNotExist:
            return Response({"error": "Customer profile not found."}, status=status.HTTP_404_NOT_FOUND)

        user = request.user
        customer.delete()
        user.delete()

        return Response({"message": "Customer profile deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
