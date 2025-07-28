from rest_framework.decorators import action
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from ..models import Ingredients, IngredientRequest
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema
from ..serializers import ApprovalActionSerializer




class IngredientRequestApprovalView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    
    @swagger_auto_schema(request_body=ApprovalActionSerializer)
    def patch(self, request, pk):
        try:
            req = IngredientRequest.objects.get(id=pk)
        except IngredientRequest.DoesNotExist:
            return Response({'error':'Request not found'}, status=404)
        
        if req.status != 'pending':
            return Response({'detail': f'Request is already {req.status}'}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = ApprovalActionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        action_type = serializer.validated_data['action']
        
        if action_type not in ['approve', 'reject']:
            return Response({'error':"Action must be 'approve' and 'reject'"}, status=400)
        
        if action_type == "approve":
            ingredient_name = req.ingredient_name.strip().lower()
            if not Ingredients.objects.filter(name__iexact=ingredient_name).exists():
                Ingredients.objects.create(name=ingredient_name)
                req.status = "approved"
            else:
                req.status = "Already Exists"
        else:
            req.status = "rejected"
        
        req.save()
        return Response({'message': f"Request handled successfully."}, status=status.HTTP_200_OK)
    