from django.db import models
from .user import User


class NewDiseaseIngredientRequest(models.Model):
    name = models.CharField(max_length=255)
    type = models.CharField(max_length=11, choices=[('ingredient', 'Ingredient'), ('disease', 'Disease')])
    description = models.TextField(blank=True, null=True)
    requested_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='requests')
    restaurant = models.ForeignKey('Restaurant', on_delete=models.CASCADE, null=True, blank=True, related_name='requests')
    status = models.CharField(max_length=20, choices=(
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ), default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=['request_type', 'status'])
        ]

    def __str__(self):
        who = self.restaurant.name if self.restaurant else self.user.email
        return f"{self.name} ({self.type}) ({self.status}) by {who}"
    

