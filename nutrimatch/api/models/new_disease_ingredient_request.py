from django.db import models
from .user import User
from ..models import Restaurant


class IngredientRequest(models.Model):
    ingredient_name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ingredient_requests')
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, null=True, blank=True, related_name='ingredient_requests')
    status = models.CharField(max_length=20, choices=(
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ), default='pending')
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        who = self.restaurant.name if self.restaurant else self.user.email
        return f"{self.ingredient_name} ({self.status}) by {who}"
    

class DiseaseRequest(models.Model):
    disease_name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='disease_requests')
    status = models.CharField(max_length=20, choices=(
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ), default='pending')
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"{self.disease_name} ({self.status}) by {self.user.email}"
    

