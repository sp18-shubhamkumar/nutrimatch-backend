from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from ..permissions import IsRestaurantAdminOrEmployee
from ..serializers import FoodItemSerializer


class FoodItemView(APIView):
    permission_classes = [IsAuthenticated, IsRestaurantAdminOrEmployee]

    def post(self, rid, request):
        pass