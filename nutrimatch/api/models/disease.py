from django.db import models
from .ingredients import Ingredients


class Diseases(models.Model):
    name = models.CharField(max_length=255)
    restricted_ingredients = models.ManyToManyField(Ingredients, related_name='diseases')

    def __str__(self):
        return self.name