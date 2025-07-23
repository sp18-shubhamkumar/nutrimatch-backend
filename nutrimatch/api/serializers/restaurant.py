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

        qs = Restaurant.objects.filter(owner=user, name__iexact=name.strip(), location__iexact=location.strip())
        if self.instance:
            qs = qs.exclude(id=self.instance.id)
        if qs.exists():
            raise serializers.ValidationError(
                "A restaurant with this owner, name, and location already exists."
            )
        return data

    def create(self, validated_data):
        user = self.context['request'].user
        return Restaurant.objects.create(owner=user, **validated_data)
