from rest_framework.views import APIView
from ..models import Restaurant
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from ..serializers import RestauratCreateSerializer
from ..permissions import IsRestaurantAdmin
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema


class RestaurantsOperationView(APIView):
    permission_classes = [IsAuthenticated, IsRestaurantAdmin]

    @swagger_auto_schema(request_body=RestauratCreateSerializer)
    def post(Self, request):
        serializer = RestauratCreateSerializer(
            data=request.data, context={'request': request})
        if serializer.is_valid():
            restaurant = serializer.save()
            return Response({"message": f"Restaurant {restaurant.name} is created successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, rid=None):
        if rid:
            try:
                restaurant = Restaurant.objects.get(id=rid, owner=request.user)
            except Restaurant.DoesNotExist:
                return Response({'detail': 'Restaurant not found or unauthorized.'}, status=status.HTTP_404_NOT_FOUND)
            serializer = RestauratCreateSerializer(restaurant)
            return Response(serializer.data)

        else:
            restaurants = Restaurant.objects.filter(owner=request.user)
            serializer = RestauratCreateSerializer(restaurants, many=True)
            return Response(serializer.data)

    @swagger_auto_schema(request_body=RestauratCreateSerializer)
    def put(self, request, rid):
        try:
            restaurant = Restaurant.objects.get(id=rid, owner=request.user)
        except Restaurant.DoesNotExist:
            return Response({'detail': 'Restaurant not found or unauthorized.'}, status=status.HTTP_404_NOT_FOUND)
        serializer = RestauratCreateSerializer(
            restaurant, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Restaurant updated successfully.', 'data': serializer.data})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, rid):
        try:
            restaurant = Restaurant.objects.get(id=rid, owner=request.user)
        except Restaurant.DoesNotExist:
            return Response({'detail': 'Restaurant not found or authorized'}, status=status.HTTP_404_NOT_FOUND)
        restaurant.delete()
        return Response({'message': 'Restaurant deleted Successfuly'}, status=status.HTTP_204_NO_CONTENT)
