from django.db import models
from .user import User


class Restaurant(models.Model):
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='restaurants')
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=255)
    opening_time = models.TimeField(null=True, blank=True)
    closing_time = models.TimeField(null=True, blank=True)

    class Meta:
        unique_together = ('owner', 'name', 'location')

    def __str__(self):
        return self.name
