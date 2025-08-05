from django.db import models
from .restaurant import Restaurant
from .ingredients import Ingredients


class FoodItem(models.Model):
    restaurant = models.ForeignKey(
        Restaurant, on_delete=models.CASCADE, related_name='food_items')
    name = models.CharField(max_length=100)
    variant = models.CharField(max_length=40, blank=True, null=True)
    category = models.CharField(max_length=40, blank=True, null=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=15, decimal_places=2)
    available = models.BooleanField(default=True)
    ingredients = models.ManyToManyField(Ingredients, related_name='food_items')
    image = models.ImageField(upload_to='food_items/', blank=True, null=True)

    class Meta:
        unique_together = ('restaurant', 'name', 'variant')

    def __str__(self):
        if self.variant:
            return f"{self.name} ({self.variant})- {self.restaurant.name}"
        return f"{self.name} - {self.restaurant.name}"
