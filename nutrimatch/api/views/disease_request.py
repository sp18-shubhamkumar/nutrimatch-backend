from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from ..models import DiseaseRequest
from ..serializers import DiseaseRequestSerializer
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema


class DiseaseRequestView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self,request):
        if request.user.is_superuser:
            requests = DiseaseRequest.objects.all()
        elif request.user.user_type == 'customer':
            requests = DiseaseRequest.objects.filter(user=request.user)
        else:
            return Response({"error": "Only customers have authorization for this."}, status=status.HTTP_400_BAD_REQUEST)
        


        if requests:
            serializer = DiseaseRequestSerializer(requests, many=True)
            return Response(serializer.data)
        return Response({"message": "No disease requests found."}, status=status.HTTP_404_NOT_FOUND)
    
    @swagger_auto_schema(request_body=DiseaseRequestSerializer)
    def post(self, request):
        if request.user.user_type != 'customer':
            return Response({"error": "Only customers can raise disease requests."}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = DiseaseRequestSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    

