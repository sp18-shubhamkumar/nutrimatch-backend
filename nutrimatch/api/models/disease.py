from django.db import models
from .ingredients import Ingredients


class Diseases(models.Model):
    name = models.CharField(max_length=255, unique=True)
    restricted_ingredients = models.ManyToManyField(
        Ingredients, related_name='diseases')

    def save(self, *args, **kwargs):
        self.name = self.name.strip().lower()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        constraints = [
            models.UniqueConstraint(
                name='unique_disease_name_case_insensitive',
                fields=['name']
            )
        ]
