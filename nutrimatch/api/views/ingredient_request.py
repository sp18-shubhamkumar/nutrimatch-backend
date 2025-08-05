from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from ..models import Restaurant, Employee, IngredientRequest
from ..serializers import IngredientRequestSerializer
from drf_yasg.utils import swagger_auto_schema 
from datetime import datetime
from django.db import models
from drf_yasg import openapi

class IngredientRequestView(APIView):
    permission_classes = [IsAuthenticated]

    def get_user_restaurant(self, user):
        if user.user_type == 'restaurant_admin':
            return Restaurant.objects.filter(owner=user).first()
        if user.user_type == 'employee':
            emp = Employee.objects.filter(user=user).first()
            return emp.restaurant if emp else None
        return None
    
    status_param = openapi.Parameter(
        'status', openapi.IN_QUERY,
        description="Comma separated statues (pending,approved,rejected,already_exists)",
        type=openapi.TYPE_STRING
    )
    search_param = openapi.Parameter(
        'search', openapi.IN_QUERY,
        description="Case-insensitive search on ingredient_name",
        type=openapi.TYPE_STRING
    )
    from_param = openapi.Parameter(
        'from', openapi.IN_QUERY,
        description="Created from date (YYYY-MM-DD)",
        type=openapi.TYPE_STRING
    )
    to_param = openapi.Parameter(
        'to', openapi.IN_QUERY,
        description="Created to data (YYYY-MM-DD)",
        type=openapi.TYPE_STRING
    )
    summary_param = openapi.Parameter(
        'summary', openapi.IN_QUERY,
        description="If true, also return counts by status",
        type=openapi.TYPE_BOOLEAN
    )

    @swagger_auto_schema(manual_parameters=[status_param, search_param, from_param, to_param, summary_param],
                         responses={200: IngredientRequestSerializer(many=True)})
    def get(self, request):
        if request.user.is_superuser:
            requests = IngredientRequest.objects.all()
        elif request.user.user_type in ['restaurant_admin', 'employee']:
            restaurant = self.get_user_restaurant(request.user)
            requests = IngredientRequest.objects.filter(restaurant=restaurant)
        else:
            requests = IngredientRequest.objects.filter(user=request.user)

        status_val = request.query_params.get('status')
        if status_val:
            statuses = [s.strip().lower() for s in status_val.split(',') if s.strip()]
            requests = requests.filter(status__in=statuses)
        search = request.query_params.get('search')

        if search:
            requests = requests.filter(ingredient_name__icontains=search.strip())
        
        date_from = request.query_params.get('from')
        date_to = request.query_params.get('to')
        if date_from:
            requests = requests.filter(created_at__date__gte=date_from)
        if date_to:
            requests = requests.filter(created_at__date__lte=date_to)

        
        serializer = IngredientRequestSerializer(requests.order_by('-created_at'), many=True)

        if request.query_params.get('summary') in ['true', '1', 'yes']:
            counts = requests.values('status').order_by().annotate(count=models.Count('id'))
            summary = {row['status']: row['count'] for row in counts}
            return Response({"results": serializer.data, "summary": summary})
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

# GET /api/v1/requests/ingredients/?status=pending
# GET /api/v1/requests/ingredients/?status=approved,rejected
# GET /api/v1/requests/ingredients/?search=sugar
# GET /api/v1/requests/ingredients/?from=2025-07-01&to=2025-07-25
# GET /api/v1/requests/ingredients/?status=pending&summary=true
    
