import pandas as pd
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from ..serializers import ExcelUploadSerializer
from ..models import Ingredients, Diseases
from django.db.models import Q
from drf_yasg.utils import swagger_auto_schema
from rest_framework.parsers import MultiPartParser, FormParser


class IngredientBulkUploadView(APIView):
    permission_classes = [IsAdminUser]
    parser_classes = [MultiPartParser, FormParser]

    @swagger_auto_schema(request_body=ExcelUploadSerializer)
    def post(self, request):
        serializer = ExcelUploadSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=400)

        file = serializer.validated_data['file']
        df = pd.read_excel(file)

        df['name'] = df['name'].str.strip().str.lower()

        existing = Ingredients.objects.filter(
            name__in=df['name']).values_list('name', flat=True)
        new_ingredients = df[~df['name'].isin(existing)]
        objs = [Ingredients(name=name)
                for name in new_ingredients['name'].unique()]
        Ingredients.objects.bulk_create(objs)

        return Response({
            "message": "Ingredients Upload Completed",
            "created": len(objs),
            "existing": len(existing)
        }, status=201)


class DiseaseBulkUploadView(APIView):
    permission_classes = [IsAdminUser]
    parser_classes = [MultiPartParser, FormParser]

    @swagger_auto_schema(request_body=ExcelUploadSerializer)
    def post(self, request):
        serializer = ExcelUploadSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=400)

        file = serializer.validated_data['file']
        df = pd.read_excel(file)
        df['name'] = df['name'].str.strip().str.lower()
        df['restricted_ingredients'] = df['restricted_ingredients'].astype(
            str).str.strip()

        all_ingredients = Ingredients.objects.all()
        ingredient_name_map = {
            ing.name.strip().lower(): ing.id for ing in all_ingredients}
        ingredient_id_set = set(i.id for i in all_ingredients)

        existing_diseases = Diseases.objects.prefetch_related(
            'restricted_ingredients').all()
        disease_map = {d.name.lower(): d for d in existing_diseases}

        created, updated, skipped = 0, 0, 0

        missing_ingredients_report = {}

        for _, row in df.iterrows():
            disease_name = row['name']
            raw_items = [x.strip().lower()
                         for x in row['restricted_ingredients'].split(',') if x.strip()]

            ingredient_ids = set()
            missing = []

            for item in raw_items:
                if item in ingredient_name_map:
                    ingredient_ids.add(ingredient_name_map[item])
                else:
                    missing.append(item)

            if not ingredient_ids:
                skipped += 1
                missing_ingredients_report[disease_name] = missing
                continue

            if disease_name in disease_map:
                disease = disease_map[disease_name]
                current_ids = set(
                    disease.restricted_ingredients.values_list('id', flat=True))
                union_ids = current_ids.union(ingredient_ids)
                disease.restricted_ingredients.set(union_ids)
                updated += 1
            else:
                disease = Diseases.objects.create(name=disease_name)
                disease.restricted_ingredients.set(ingredient_ids)
                created += 1

            if missing:
                missing_ingredients_report[disease_name] = missing

        return Response({
            "message": "Diseases Uploaded Successfully",
            "created": created,
            "updated": updated,
            "skipped": skipped,
            "missing_ingredients": missing_ingredients_report
        }, status=201)
