from rest_framework import serializers
from ..models import Diseases, Ingredients
from ..serializers import IngredientSerializer


class DiseaseSerializer(serializers.ModelSerializer):
    restricted_ingredients_ids = serializers.PrimaryKeyRelatedField(
        source='restricted_ingredients',
        queryset=Ingredients.objects.all(),
        many=True,
        write_only=True
    )

    restricted_ingredients = serializers.PrimaryKeyRelatedField(
        many=True,
        read_only=True
    )

    class Meta:
        model = Diseases
        fields = ['id', 'name', 'restricted_ingredients_ids',
                  'restricted_ingredients']

    def create(self, validated_data):
        ingredients = validated_data.pop('retricted_ingredients', [])
        disease = Diseases.objects.create(**validated_data)
        disease.restricted_ingredients.set(ingredients)
        return disease

    def update(self, instance, validated_data):
        ingredients = validated_data.pop('restricted_ingredients', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        if ingredients is not None:
            instance.restricted_ingredients.set(ingredients)
        return instance

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['restricted_ingredients'] = list(
            instance.restricted_ingredients.values_list('id', flat=True))
        return rep
