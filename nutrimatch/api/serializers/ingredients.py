from rest_framework import serializers
from ..models import Ingredients


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredients
        fields = '__all__'

    def validate_name(self, value):
        value = value.strip().lower()
        if Ingredients.objects.filter(name__iexact=value).exists():
            raise serializers.ValidationError("Ingredient with name already exists.")
        return value
    