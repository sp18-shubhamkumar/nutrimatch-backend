from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from ..permissions import IsRestaurantAdminOrEmployee
from ..serializers import FoodItemSerializer
from ..models import Restaurant, Employee, FoodItem
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status

class FoodItemView(APIView):
    permission_classes = [IsAuthenticated, IsRestaurantAdminOrEmployee]
    parser_classes = [MultiPartParser, FormParser]

    def get_restaurant(self, rid, user):
        try:
            restaurant = Restaurant.objects.get(id=rid)
            if restaurant.owner == user or Employee.objects.filter(user=user, restaurant=restaurant).exists():
                return restaurant
        except Restaurant.DoesNotExist:
            return None

    @swagger_auto_schema(request_body=FoodItemSerializer)
    def post(self, request, rid):
        restaurant = self.get_restaurant(rid, request.user)
        if not restaurant:
            return Response({'error': 'Unauthorized or restaurant not found'}, status=status.HTTP_403_FORBIDDEN)

        serializer = FoodItemSerializer(data=request.data, context={
                                        'restaurant': restaurant, 'request': request})

        if serializer.is_valid():
            food = serializer.save(restaurant=restaurant)
            out = FoodItemSerializer(
                food, context={'restaurant': restaurant, 'request': request})
            response_data = {
                'message': 'Food Item added Successfully', 'data': out.data}
            return Response(response_data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, rid, fid=None):
        restaurant = self.get_restaurant(rid, request.user)
        if not restaurant:
            return Response({'error': 'Unauthorized or restaurant not found'}, status=status.HTTP_403_FORBIDDEN)

        if fid:
            try:
                food = FoodItem.objects.get(id=fid, restaurant=restaurant)
                serializer = FoodItemSerializer(
                    food, context={'restaurant': restaurant, 'request': request})
                return Response(serializer.data)
            except FoodItem.DoesNotExist:
                return Response({'error': 'Food Item not found'}, status=status.HTTP_404_NOT_FOUND)

        foods = FoodItem.objects.filter(restaurant=restaurant)
        serializer = FoodItemSerializer(foods, many=True, context={
                                        'request': request})
        return Response(serializer.data)

    @swagger_auto_schema(request_body=FoodItemSerializer)
    def patch(self, request, rid, fid):
        restaurant = self.get_restaurant(rid, request.user)
        if not restaurant:
            return Response({'error': 'Unauthorized or restaurant not found'}, status=status.HTTP_403_FORBIDDEN)

        try:
            food = FoodItem.objects.get(id=fid, restaurant=restaurant)
        except FoodItem.DoesNotExist:
            return Response({'error': 'Food Item not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = FoodItemSerializer(
            food, data=request.data, partial=True, context={'restaurant': restaurant, 'request': request})

        if serializer.is_valid():
            food = serializer.save()
            out = FoodItemSerializer(food, context={'request': request})
            response_data = {
                'message': 'Food Item Updated Successfully', 'data': out.data}
            return Response(response_data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, rid, fid):
        restaurant = self.get_restaurant(rid, request.user)
        if not restaurant:
            return Response({'error': 'Unauthorized or restaurant not found'}, status=status.HTTP_403_FORBIDDEN)

        try:
            food = FoodItem.objects.get(id=fid, restaurant=restaurant)
            food.delete()
            return Response({'message': 'Food Item is Deleted'}, status=status.HTTP_204_NO_CONTENT)
        except FoodItem.DoesNotExist:
            return Response({'error': 'Food Item not Found'}, status=status.HTTP_404_NOT_FOUND)
