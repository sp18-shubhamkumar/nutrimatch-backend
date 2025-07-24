from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from ..models import Restaurant, Employee, NewDiseaseIngredientRequest
from ..serializers import NewRequestSerializer


class NewRequestView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = request.data.copy()
        restaurant = None

        if request.user.user_type in ['restaurant_admin', 'employee']:
            if request.user.user_type == 'restaurant_admin':
                restaurant = Restaurant.objects.filter(owner=request.user).first()
            else:
                emp = Employee.objects.filter(user=request.user).first()
                restaurant = emp.restaurant if emp else None

            if restaurant:
                data['restaurant'] = restaurant.id

        seri

    
