from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from ..permissions import IsAdminOrCustomerReadOnly
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from ..serializers import DiseaseSerializer
from ..models import Diseases


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
                return Response(serializer.data, status=200)
            return Response({'error': 'Disease not found'}, status=400)
        
        search = request.query_params.get('search')
        diseases = Diseases.objects.all()
        if search:
            diseases = diseases.filter(name__icontains=search)
        serializer = DiseaseSerializer(diseases, many=True)
        return Response(serializer.data, status=200)

    @swagger_auto_schema(request_body=DiseaseSerializer)
    def post(self, request):
        if not request.user.is_superuser:
            return Response({'error': 'Only admin has access to this.'}, status=403)
        serializer = DiseaseSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    @swagger_auto_schema(request_body=DiseaseSerializer)
    def put(self, request, pk):
        if not request.user.is_superuser:
            return Response({'error': 'Only admin has access to this.'}, status=403)
        disease = self.get_object(pk)
        if disease:
            serializer = DiseaseSerializer(
                disease, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=200)
            return Response(serializer.errors, status=400)
        return Response({'error': 'Disease not found'}, status=404)

    def delete(self, request, pk):
        if not request.user.is_superuser:
            return Response({'error': 'Only admin has access to this.'}, status=403)
        disease = self.get_object(pk)
        if disease:
            disease.delete()
            return Response({'message': 'Disease deleted successfully'}, status=204)
        return Response({'error': 'Disease not found'}, status=404)
