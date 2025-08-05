from rest_framework import serializers
from ..models import DiseaseRequest, IngredientRequest


class IngredientRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = IngredientRequest
        fields = ['id', 'ingredient_name', 'description', 'status', 'created_at']
        read_only_fields = ['status', 'created_at', 'restaurant']

    def validate_ingredient_name(self, value):
        return value.strip().lower()
    

class DiseaseRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = DiseaseRequest
        fields = ['id', 'disease_name', 'description', 'status', 'created_at']
        read_only_fields = ['status', 'created_at']


class ApprovalActionSerializer(serializers.Serializer):
    action = serializers.ChoiceField(choices=['approve', 'reject'])

    