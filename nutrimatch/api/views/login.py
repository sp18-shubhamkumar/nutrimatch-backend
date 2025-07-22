from rest_framework.response import Response
from rest_framework.views import APIView
from ..serializers import UserLoginSerializer
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema


class LoginView (APIView):

    @swagger_auto_schema(request_body=UserLoginSerializer)
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            serializer.validated_data
            return Response(serializer.validated_data, status=status.HTTP_200_OK)
        return Response( serializer.errors, status=status.HTTP_401_UNAUTHORIZED)