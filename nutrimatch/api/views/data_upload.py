import pandas as pd
import spacy
from rapidfuzz import fuzz
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from rest_framework.parsers import MultiPartParser, FormParser
from django.db import transaction
from drf_yasg.utils import swagger_auto_schema

from ..models import Diseases, Ingredients
from ..serializers import ExcelUploadSerializer
from django.db.models import Q

nlp = spacy.load("en_core_web_sm")


def normalize_text(text):
    return text.strip().lower().rstrip('s')  # to handle plurals like sugars -> sugar


def fuzzy_match(name, queryset, threshold=85):
    name = normalize_text(name)
    best_match = None
    highest_score = threshold
    for obj in queryset:
        score = fuzz.token_sort_ratio(name, normalize_text(obj.name))
        if score > highest_score:
            highest_score = score
            best_match = obj
    return best_match


class IngredientBulkUploadView(APIView):
    permission_classes = [IsAdminUser]
    parser_classes = [MultiPartParser, FormParser]

    @swagger_auto_schema(request_body=ExcelUploadSerializer)
    def post(self, request):
        serializer = ExcelUploadSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=400)

        file = serializer.validated_data['file']
        try:
            df = pd.read_excel(file)
        except Exception as e:
            return Response({"error": "Invalid Excel file"}, status=400)

        ingredients_to_create = []
        existing_ingredients = Ingredients.objects.all()
        existing_names = [normalize_text(i.name) for i in existing_ingredients]
        newly_created = []

        for name in df.iloc[:, 0].dropna().unique():
            cleaned_name = normalize_text(str(name))
            if cleaned_name not in existing_names:
                match = fuzzy_match(cleaned_name, existing_ingredients)
                if not match:
                    ingredients_to_create.append(Ingredients(name=cleaned_name))
                    newly_created.append(cleaned_name)

        Ingredients.objects.bulk_create(ingredients_to_create, ignore_conflicts=True)

        return Response({
            "message": "Ingredient upload complete.",
            "newly_created_ingredients": newly_created,
            "total_created": len(newly_created)
        })


class DiseaseBulkUploadView(APIView):
    permission_classes = [IsAdminUser]
    parser_classes = [MultiPartParser, FormParser]

    @swagger_auto_schema(request_body=ExcelUploadSerializer)
    @transaction.atomic
    def post(self, request):
        serializer = ExcelUploadSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=400)

        file = serializer.validated_data['file']
        try:
            df = pd.read_excel(file)
        except Exception:
            return Response({"error": "Invalid Excel file"}, status=400)

        created_diseases = []
        updated_diseases = {}
        new_ingredients = []

        existing_diseases = Diseases.objects.all()
        existing_ingredients = Ingredients.objects.all()
        ingredient_dict = {normalize_text(i.name): i for i in existing_ingredients}

        for _, row in df.iterrows():
            disease_name = normalize_text(str(row.iloc[0]))
            ingredients_str = row.iloc[1]

            if pd.isna(ingredients_str):
                continue

            restricted_names = [normalize_text(i) for i in str(ingredients_str).split(',') if i.strip()]
            matched_disease = fuzzy_match(disease_name, existing_diseases)

            if matched_disease:
                disease_obj = matched_disease
                action = 'updated'
            else:
                disease_obj = Diseases(name=disease_name)
                disease_obj.save()
                created_diseases.append(disease_name)
                action = 'created'

            ingredient_ids = []
            for ing_name in restricted_names:
                if ing_name in ingredient_dict:
                    ingredient_ids.append(ingredient_dict[ing_name].id)
                else:
                    matched_ing = fuzzy_match(ing_name, existing_ingredients)
                    if matched_ing:
                        ingredient_ids.append(matched_ing.id)
                    else:
                        new_ing = Ingredients(name=ing_name)
                        new_ing.save()
                        ingredient_dict[normalize_text(new_ing.name)] = new_ing
                        existing_ingredients |= Ingredients.objects.filter(id=new_ing.id)
                        ingredient_ids.append(new_ing.id)
                        new_ingredients.append(ing_name)

            disease_obj.restricted_ingredients.add(*ingredient_ids)
            if action == 'updated':
                updated_diseases.setdefault(disease_obj.name, []).extend(ingredient_ids)

        return Response({
            "message": "Disease bulk upload completed.",
            "summary": {
                "new_diseases_created": created_diseases,
                "existing_diseases_updated": {k: list(set(v)) for k, v in updated_diseases.items()},
                "new_ingredients_created": list(set(new_ingredients))
            }
        })
