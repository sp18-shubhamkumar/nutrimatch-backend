from rest_framework.views import APIView
from ..serializers import UserRegistrationSerializer
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema


class RegisterView(APIView):

    @swagger_auto_schema(request_body=UserRegistrationSerializer)
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": f"User is Successfully Registered as a {serializer.validated_data.get("user_type")}."},
                            status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
