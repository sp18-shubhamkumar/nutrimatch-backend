from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from ..permissions import IsRestaurantAdminOrEmployee
from ..serializers import FoodItemSerializer
from ..models import Restaurant, Employee, FoodItem
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema


class FoodItemView(APIView):
    permission_classes = [IsAuthenticated, IsRestaurantAdminOrEmployee]\


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
            return Response({'error': 'Unauthorized or restaurant not found'}, status=403)

        serializer = FoodItemSerializer(data=request.data, context={
                                        'restaurant': restaurant})

        if serializer.is_valid():
            serializer.save(restaurant=restaurant)
            return Response({'message': 'Food Item added Successfully', 'data': serializer.data}, status=201)
        return Response(serializer.errors, status=400)

    def get(self, request, rid, fid=None):
        restaurant = self.get_restaurant(rid, request.user)
        if not restaurant:
            return Response({'error': 'Unauthorized or restaurant not found'}, status=403)

        if fid:
            try:
                food = FoodItem.objects.get(id=fid, restaurant=restaurant)
                serializer = FoodItemSerializer(
                    food, context={'restaurant': restaurant})
                return Response(serializer.data)
            except FoodItem.DoesNotExist:
                return Response({'error': 'Food Item not found'}, status=404)

        foods = FoodItem.objects.filter(restaurant=restaurant)
        serializer = FoodItemSerializer(foods, many=True, context={
                                        'restaurant': restaurant})
        return Response(serializer.data)

    @swagger_auto_schema(request_body=FoodItemSerializer)
    def patch(self, request, rid, fid):
        restaurant = self.get_restaurant(rid, request.user)
        if not restaurant:
            return Response({'error': 'Unauthorized or restaurant not found'}, status=403)

        try:
            food = FoodItem.objects.get(id=fid, restaurant=restaurant)
        except FoodItem.DoesNotExist:
            return Response({'error': 'Food Item not found'}, status=404)
        serializer = FoodItemSerializer(
            food, data=request.data, partial=True, context={'restaurant': restaurant})
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Food item updated', 'data': serializer.data})
        return Response(serializer.errors, status=400)

    def delete(self, request, rid, fid):
        restaurant = self.get_restaurant(rid, request.user)
        if not restaurant:
            return Response({'error': 'Unauthorized or restaurant not found'}, status=403)

        try:
            food = FoodItem.objects.get(id=fid, restaurant=restaurant)
            food.delete()
            return Response({'message': 'Food Item is Deleted'}, status=204)
        except FoodItem.DoesNotExist:
            return Response({'error': 'Food Item not Found'}, status=404)
