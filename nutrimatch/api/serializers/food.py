from rest_framework import serializers
from ..models import FoodItem


class FoodItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = FoodItem
        fields = '__all__'
        read_only_fields = ['restaurant']

    def validate(self, data):
        restaurant = self.context.get('restaurant') or (
            self.instance.restaurant if self.instance else None)
        name = data.get('name', self.instance.name if self.instance else None)
        variant = data.get(
            'variant', self.instance.variant if self.instance else None)

        normalized_name = name.strip().lower() if name else ''
        normalized_variant = variant.strip().lower() if variant else None

        existing_items = FoodItem.objects.filter(
            restaurant=restaurant
        ).exclude(id=self.instance.id if self.instance else None)

        filter_kwargs = {'name__iexact': normalized_name}
        if normalized_variant is not None:
            filter_kwargs['variant__iexact'] = normalized_variant
        else:
            filter_kwargs['variant__isnull'] = True

        if existing_items.filter(**filter_kwargs).exists():
            raise serializers.ValidationError(
                "This Food item already exists in the restaurant with the same name and variant."
            )
        return data
