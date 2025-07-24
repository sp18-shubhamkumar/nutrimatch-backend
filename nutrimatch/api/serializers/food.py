from rest_framework import serializers
from ..models import FoodItem


class FoodItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = FoodItem
        fields = '__all__'
        read_only_fields = ['restaurant']

    def validate(self, data):
        restaurant = self.context.get('restaurant') or self.instance.restaurant
        name = data.get('name', self.instance.name if self.instance else None)
        desc = data.get(
            'description', self.instance.description if self.instance else None)

        if FoodItem.objects.filter(
            restaurant=restaurant,
            name=name,
            description=desc
        ).exclude(id=self.instance.id if self.instance else None).exists():
            raise serializers.ValidationError(
                "This Food item already exists in the restaurant with the same name and description."
            )
        return data
