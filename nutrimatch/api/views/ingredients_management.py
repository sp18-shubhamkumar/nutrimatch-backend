from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..models import Ingredients
from ..serializers import IngredientSerializer
from ..permissions import IsAdminOrReadOnly
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

class IngredientsView(APIView):
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]

    def get_object(self,iid):
        try:
            return Ingredients.objects.get(id=iid)
        except Ingredients.DoesNotExist:
            return None

    @swagger_auto_schema(manual_parameters=[openapi.Parameter(
        'search', openapi.IN_QUERY, 
        description="Search ingredient by name(case-insensitive)", 
        type=openapi.TYPE_STRING)
        ]
        )
    
    def get(self, request, iid=None):
        if iid:
            ingredient = self.get_object(iid)
            if not ingredient:
                return Response({'error':'Ingredient not found'}, status=404)
            serializer = IngredientSerializer(ingredient)
            return Response(serializer.data)
        
        search = request.query_params.get('search')

        ingredients = Ingredients.objects.all()
        if search:
            ingredients = ingredients.filter(name__icontains=search)
        serializer = IngredientSerializer(ingredients, many=True)
        return Response(serializer.data)
    
    @swagger_auto_schema(request_body=IngredientSerializer)
    def post(self, request):
        serializer = IngredientSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message':'Ingredient added successfully', 'data':serializer.data}, status=201)
        return Response(serializer.errors, status=400)
    
    @swagger_auto_schema(request_body=IngredientSerializer)
    def put(self, request, iid):
        ingredient = self.get_object(iid)
        if not ingredient:
            return Response({'error':'Ingredient not found'}, status==404)
        serializer = IngredientSerializer(ingredient, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message':'Ingredient updated', 'data':serializer.data})
        return Response(serializer.errors, status=404)
    
    def delete(self, request, iid):
        ingredient = self.get_object(iid)
        if not ingredient:
            return Response({'error':'Ingredient not found'}, status==404)
        ingredient.delete()
        return Response({'message': 'Ingredient deleted'})
