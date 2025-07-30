from rest_framework import serializers
from ..models import Customer, Diseases, Ingredients, User
from . import IngredientSerializer


class CustomerSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(source='user.email', read_only=True)
    disease_ids = serializers.PrimaryKeyRelatedField(
        source='diseases',
        queryset=Diseases.objects.all(),
        many=True,
        write_only=True,
        required=False
    )

    restricted_ingredients_ids = serializers.PrimaryKeyRelatedField(
        source='restricted_ingredients',
        queryset=Ingredients.objects.all(),
        many=True,
        write_only=True,
        required=False
    )

    allowed_ingredients_ids = serializers.PrimaryKeyRelatedField(
        source='allowed_ingredients',
        queryset=Ingredients.objects.all(),
        many=True,
        write_only=True,
        required=False
    )

    class Meta:
        model = Customer
        fields = ['id', 'email', 'disease_ids',
                  'restricted_ingredients_ids', 'allowed_ingredients_ids']
        read_only_fields = ['id']

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['disease_ids'] = list(
            instance.diseases.values_list('id', flat=True))
        rep['restricted_ingredients_ids'] = list(
            instance.restricted_ingredients.values_list('id', flat=True))
        rep['allowed_ingredients_ids'] = list(
            instance.allowed_ingredients.values_list('id', flat=True))
        return rep

    def update(self, instance, validated_data):
        diseases = validated_data.pop('diseases', None)
        ingredients = validated_data.pop('restricted_ingredients', None)
        allowed = validated_data.pop('allowed_ingredients', None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if diseases is not None:
            instance.diseases.set(diseases)

        if ingredients is not None:
            instance.restricted_ingredients.set(ingredients)

        if allowed is not None:
            instance.allowed_ingredients.set(allowed)

        return instance
