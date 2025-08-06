from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from rest_framework.parsers import MultiPartParser, FormParser
from django.db import transaction
from drf_yasg.utils import swagger_auto_schema
from ..serializers import ExcelUploadSerializer
import tempfile
from api.tasks import process_disease_upload, process_ingredient_upload
from rest_framework import status


class IngredientBulkUploadView(APIView):
    permission_classes = [IsAdminUser]
    parser_classes = [MultiPartParser, FormParser]

    @swagger_auto_schema(request_body=ExcelUploadSerializer)
    def post(self, request):
        serializer = ExcelUploadSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        file = serializer.validated_data['file']

        with tempfile.NamedTemporaryFile(delete=False, suffix=".xlsx") as temp:
            for chunk in file.chunks():
                temp.write(chunk)
            temp_path = temp.name

        process_ingredient_upload.delay(temp_path)
        return Response({"message": "Ingredient upload is being processed in the background"})
    
    


class DiseaseBulkUploadView(APIView):
    permission_classes = [IsAdminUser]
    parser_classes = [MultiPartParser, FormParser]

    @swagger_auto_schema(request_body=ExcelUploadSerializer)
    @transaction.atomic
    def post(self, request):
        serializer = ExcelUploadSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        file = serializer.validated_data['file']

        with tempfile.NamedTemporaryFile(delete=False, suffix=".xlsx") as temp:
            for chunk in file.chunks(chunk_size=1*1024):
                temp.write(chunk)
            temp_path = temp.name

        process_disease_upload.delay(temp_path)

        return Response({
            "message": "Disease bulk upload is being processed in the background."
        })
