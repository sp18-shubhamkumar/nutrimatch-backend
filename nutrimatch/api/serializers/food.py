from rest_framework import serializers
from ..models import FoodItem, Ingredients


class FoodItemSerializer(serializers.ModelSerializer):
    ingredient_names = serializers.ListField(
        child=serializers.CharField(),
        write_only=True,
        required=False
    )

    class Meta:
        model = FoodItem
        # fields = '__all__'
        exclude = ['ingredients']
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
    
    def _resolve_ingredients(self, names):
        valid_ingredients = []
        rejected = []
        for name in names:
            normalized = name.strip().lower()
            try:
                ingredient = Ingredients.objects.get(name__iexact=normalized)
                valid_ingredients.append(ingredient)
            except Ingredients.DoesNotExist:
                rejected.append(name)
        return valid_ingredients, rejected
        
    
    def create(self, validated_data):
        names = validated_data.pop('ingredient_names',[])
        ingredients, rejected = self._resolve_ingredients(names)
        food = FoodItem.objects.create(**validated_data)
        food.ingredients.set(ingredients)
        if rejected:
            self.context['rejected_ingredients'] = rejected
        return food

    def update(self, instance, validated_data):
        names = validated_data.pop('ingredient_names', None)
        instance = super().update(instance, validated_data)
        if names is not None:
            ingredients, rejected = self._resolve_ingredients(names)
            instance.ingredients.set(ingredients)
            if rejected:
                self.context['rejected_ingredients'] = rejected
        
        return instance
    
    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['ingredient_names'] = [ing.name for ing in instance.ingredients.all()]
        rejected = self.context.get('rejected_ingredients')
        if rejected:
            data['warning'] = f"The following ingredients were not found and were ignored: {', '.join(rejected)}"

        return data 