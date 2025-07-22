from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    user_type = serializers.ChoiceField(
        choices=User.USER_TYPE_CHOICES, help_text="Choose user_type from: 'customer', 'restaurant_admin'")

    class Meta:
        model = User
        fields = ['id', 'email', 'password', 'user_type']

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            user_type=validated_data['user_type']
        )
        return user
