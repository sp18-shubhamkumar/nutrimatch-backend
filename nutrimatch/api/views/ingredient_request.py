from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from ..models import Restaurant, Employee, IngredientRequest
from ..serializers import IngredientRequestSerializer
from drf_yasg.utils import swagger_auto_schema 

class IngredientRequestView(APIView):
    permission_classes = [IsAuthenticated]

    def get_user_restaurant(self, user):
        if user.user_type == 'restaurant_admin':
            return Restaurant.objects.filter(owner=user).first()
        if user.user_type == 'employee':
            emp = Employee.objects.filter(user=user).first()
            return emp.restaurant if emp else None
        return None
    
    def get(self, request):
        if request.user.is_superuser:
            requests = IngredientRequest.objects.all()
        elif request.user.user_type in ['restaurant_admin', 'employee']:
            restaurant = self.get_user_restaurant(request.user)
            requests = IngredientRequest.objects.filter(restaurant=restaurant)
        else:
            requests = IngredientRequest.objects.filter(user=request.user)
        serializer = IngredientRequestSerializer(requests, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(request_body=IngredientRequestSerializer)
    def post(self, request):
        restaurant = None
        if request.user.user_type in ['restaurant_admin', 'employee']:
            restaurant = self.get_user_restaurant(request.user)
        serializer = IngredientRequestSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user, restaurant=restaurant)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    
