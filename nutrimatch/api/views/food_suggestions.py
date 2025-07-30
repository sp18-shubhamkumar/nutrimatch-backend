from rest_framework.views import APIView
from rest_framework.response import Response
from ..models import Customer, FoodItem, Ingredients
from ..permissions import IsCustomer
from rest_framework.permissions import IsAuthenticated
from ..serializers import CustomerSerializer, FoodItemSerializer
from drf_yasg.utils import swagger_auto_schema
from django.db.models import Count


class FoodSuggestionsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        if user.user_type != 'customer':
            return Response({"error": "Only customers can access this endpoint."}, status=403)
        try:
            customer = user.customer_profile
        except Customer.DoesNotExist:
            return Response({"error": "Customer profile not found."}, status=404)

        disease_ingredient_ids = Ingredients.objects.filter(
            diseases__in=customer.diseases.all()
        ).values_list('id', flat=True)

        direct_ingredient_ids = customer.restricted_ingredients.values_list(
            'id', flat=True)
        allowed_ingredient_ids = customer.allowed_ingredients.values_list(
            'id', flat=True)

        restricted_ingredient_ids = set(disease_ingredient_ids).union(
            set(direct_ingredient_ids)) - set(allowed_ingredient_ids)

        food_items = FoodItem.objects.exclude(ingredients__id__in=restricted_ingredient_ids).annotate(
            num_ingredients=Count('ingredients')).filter(num_ingredients__gt=0).distinct()
        serializer = FoodItemSerializer(
            food_items, many=True, context={'request': request})
        return Response(serializer.data, status=200)
