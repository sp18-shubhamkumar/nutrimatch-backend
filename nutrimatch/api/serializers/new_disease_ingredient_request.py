from rest_framework import serializers
from ..models import NewDiseaseIngredientRequest


class NewRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewDiseaseIngredientRequest
        fields = ['id', 'name', 'type', 'description', 'restaurant', 'is_reviewed', 'created_at']
        read_only_fields = ['is_reviewed', 'created_at', 'restaurant']
        