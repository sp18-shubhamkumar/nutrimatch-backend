from rest_framework import serializers
from ..models import Restaurant


class RestauratCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = ['id', 'name', 'location', 'opening_time', 'closing_time']

    def validate(self, data):
        user = self.context['request'].user
        name = data.get('name')
        location = data.get('location')

        if Restaurant.objects.filter(owner=user, name=name, location=location).exists():
            raise serializers.ValidationError(
                "You already have a restaurant with this name and location."
            )
        return data

    def create(self, validated_data):
        user = self.context['request'].user
        return Restaurant.objects.create(owner=user, **validated_data)
