from django.db import models
from .restaurant import Restaurant


class FoodItem(models.Model):
    restaurant = models.ForeignKey(
        Restaurant, on_delete=models.CASCADE, related_name='food_items')
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    price = models.DecimalField(decimal_places=2)
    available = models.BooleanField(default=True)

    class Meta :
        unique_together = ('restaurant', 'name', 'description')

    def __str__(self):
        return f"{self.name} - {self.restaurant.name}"
