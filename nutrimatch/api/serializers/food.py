from rest_framework import serializers
from ..models import FoodItem, Ingredients


class FoodItemSerializer(serializers.ModelSerializer):
    ingredients_ids = serializers.CharField(required=False, write_only=True)
    image = serializers.ImageField(required=False, allow_null=True)

    class Meta:
        model = FoodItem
        fields = [
            'id', 'image', 'name', 'variant', 'category',
            'description', 'price', 'available', 'ingredients_ids'
        ]
        read_only_fields = ['id']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        request = self.context.get('request')
        if request and request.method in ['PUT', 'PATCH']:
            self.fields['name'].required = False
            self.fields['price'].required = False

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

    def _parse_ingredient_ids(self, raw):
        if not raw:
            return []
        if isinstance(raw, list):
            # For MultiPart: ['4,8']
            raw = raw[0]
        try:
            return [int(i.strip()) for i in raw.split(',') if i.strip().isdigit()]
        except Exception:
            raise serializers.ValidationError({
                'ingredients_ids': 'All IDs must be integers separated by commas.'
            })

    def create(self, validated_data):
        ingredient_ids_raw = validated_data.pop('ingredients_ids', '')
        ingredient_ids = self._parse_ingredient_ids(ingredient_ids_raw)

        food = FoodItem.objects.create(**validated_data)
        food.ingredients.set(Ingredients.objects.filter(id__in=ingredient_ids))
        return food

    def update(self, instance, validated_data):
        ingredient_ids_raw = validated_data.pop('ingredients_ids', None)
        instance = super().update(instance, validated_data)

        if ingredient_ids_raw is not None:
            ingredient_ids = self._parse_ingredient_ids(ingredient_ids_raw)
            instance.ingredients.set(Ingredients.objects.filter(id__in=ingredient_ids))
        return instance

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['ingredients_ids'] = list(instance.ingredients.values_list('id', flat=True))

        request = self.context.get('request')
        if instance.image and request:
            data['image'] = request.build_absolute_uri(instance.image.url)

        return data
