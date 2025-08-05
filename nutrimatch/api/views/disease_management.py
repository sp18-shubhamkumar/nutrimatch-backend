from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from ..permissions import IsAdminOrCustomerReadOnly
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from ..serializers import DiseaseSerializer
from ..models import Diseases
from rest_framework import status


class DiseaseManagementView(APIView):
    permission_classes = [IsAuthenticated, IsAdminOrCustomerReadOnly]

    def get_object(self, pk):
        try:
            return Diseases.objects.get(pk=pk)
        except Diseases.DoesNotExist:
            return None
    
    @swagger_auto_schema(manual_parameters=[
        openapi.Parameter('search', openapi.IN_QUERY,
                          description="Search disease by name(case-insensitive)",
                          type=openapi.TYPE_STRING
                          )
            ]
    )
    def get(self, request, pk=None):
        if pk:
            disease = self.get_object(pk)
            if disease:
                serializer = DiseaseSerializer(disease)
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response({'error': 'Disease not found'}, status=status.HTTP_400_BAD_REQUEST)
        
        search = request.query_params.get('search')
        diseases = Diseases.objects.all()
        if search:
            diseases = diseases.filter(name__icontains=search)
        serializer = DiseaseSerializer(diseases, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(request_body=DiseaseSerializer)
    def post(self, request):
        if not request.user.is_superuser:
            return Response({'error': 'Only admin has access to this.'}, status=status.HTTP_403_FORBIDDEN)
        serializer = DiseaseSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(request_body=DiseaseSerializer)
    def put(self, request, pk):
        if not request.user.is_superuser:
            return Response({'error': 'Only admin has access to this.'}, status=status.HTTP_403_FORBIDDEN)
        disease = self.get_object(pk)
        if disease:
            serializer = DiseaseSerializer(
                disease, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({'error': 'Disease not found'}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk):
        if not request.user.is_superuser:
            return Response({'error': 'Only admin has access to this.'}, status=status.HTTP_403_FORBIDDEN)
        disease = self.get_object(pk)
        if disease:
            disease.delete()
            return Response({'message': 'Disease deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
        return Response({'error': 'Disease not found'}, status=status.HTTP_404_NOT_FOUND)
