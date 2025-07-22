from rest_framework.views import APIView
from rest_framework.response import Response
from ..models import Employee, Restaurant
from ..permissions import IsRestaurantAdmin
from ..serializers import EmployeeSerializer
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema


class EmployeeManagementView(APIView):
    permission_classes = [IsAuthenticated, IsRestaurantAdmin]

    def get_restaurant(self, rid, user):
        try:
            return Restaurant.objects.get(id=rid, owner=user)
        except Restaurant.DoesNotExist:
            return None

    def get(self, request, rid, eid=None):
        restaurant = self.get_restaurant(rid, request.user)
        if not restaurant:
            return Response({"error": "Unauthorized or restaurant not found."}, status=403)
        if eid:
            try:
                employee = Employee.objects.get(id=eid, restaurant=restaurant)
                serializer = EmployeeSerializer(employee)
                return Response(serializer.data)
            except Employee.DoesNotExist:
                return Response({'error': 'Employee not found'}, status=404)
        employees = Employee.objects.filter(restaurant=restaurant)
        serializer = EmployeeSerializer(employees, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(request_body=EmployeeSerializer)
    def post(self, request, rid):
        restaurant = self.get_restaurant(rid, request.user)
        if not restaurant:
            return Response({'detail': 'Restaurant not found or authorized'}, status=404)

        serializer = EmployeeSerializer(data=request.data, context={
                                        'restaurant': restaurant})
        if serializer.is_valid():
            serializer.save()
            return Response({"message": f"Employee is added successfully."}, status=201)
        return Response(serializer.errors, status=400)

    @swagger_auto_schema(request_body=EmployeeSerializer)
    def patch(self, request, rid, eid):
        restaurant = self.get_restaurant(rid, request.user)
        if restaurant is None:
            return Response({'error': 'Unauthorized or Restaurant not found'}, status=403)
        try:
            employee = Employee.objects.get(id=eid, restaurant=restaurant)
        except Employee.DoesNotExist:
            return Response({"error": "Employee not Found"}, status=404)
        data = request.data.copy()
        if 'restaurant' in data:
            data.pop('restaurant')
            Response({"message": "restaurant field can't be updated"})
        serializer = EmployeeSerializer(employee, data=data, partial=True, context={
                                        "restaurant": restaurant})
        if serializer.is_valid():
            serializer.save()
            return Response({'message': "Employee details is Successfully Updated. Restaurant field can't be Updated", 'data': serializer.data})
        return Response(serializer.errors, status=400)

    def delete(self, request, rid, eid):
        restaurant = self.get_restaurant(rid, request.user)
        if restaurant is None:
            return Response({"error": "Unauthorized or it doesn't exists."})
        try:
            employee = Employee.objects.get(id=eid, restaurant=restaurant)
            employee.user.delete()
            employee.delete()
            return Response({"message": "Employee Deleted Successfully."}, status=204)
        except Employee.DoesNotExist:
            return Response({"error": "Employee not found."}, status=404)
