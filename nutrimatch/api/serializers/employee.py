from rest_framework import serializers
from ..models import Employee
from django.contrib.auth import get_user_model

User = get_user_model()


class EmployeeSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(write_only=True)
    password = serializers.CharField(write_only=True)
    position = serializers.CharField()

    class Meta:
        model = Employee
        fields = ['id', 'email', 'password', 'position']

    def create(self, validated_data):
        email = validated_data.pop('email')
        password = validated_data.pop('password')
        restaurant = self.context['restaurant']

        user = User.objects.create_user(
            email=email, password=password, user_type='employee')
        employee = Employee.objects.create(
            user=user, restaurant=restaurant, **validated_data)
        return employee

    def to_representation(self, instance):
        return {
            "id": instance.id,
            "email": instance.user.email,
            "position": instance.position,
            "restaurant": instance.restaurant.name
        }
