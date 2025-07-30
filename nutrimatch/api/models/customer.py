from django.db import models
from ..models import Diseases, Ingredients, User


class Customer(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='customer_profile')
    diseases = models.ManyToManyField(Diseases, blank=True)
    restricted_ingredients = models.ManyToManyField(
        Ingredients, blank=True, related_name='restricted_ingredients')
    allowed_ingredients = models.ManyToManyField(
        Ingredients, blank=True, related_name='allowed_ingredients')

    def __str__(self):
        return f"Customer Profile = {self.user.email}"
