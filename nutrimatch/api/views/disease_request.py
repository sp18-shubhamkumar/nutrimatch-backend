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
            return Response({"error": "Only customers have authorization for this."}, status=400)
        


        if requests:
            serializer = DiseaseRequestSerializer(requests, many=True)
            return Response(serializer.data)
        return Response({"message": "No disease requests found."}, status=404)
    
    @swagger_auto_schema(request_body=DiseaseRequestSerializer)
    def post(self, request):
        if request.user.user_type != 'customer':
            return Response({"error": "Only customers can raise disease requests."}, status=400)
        
        serializer = DiseaseRequestSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
    
    

