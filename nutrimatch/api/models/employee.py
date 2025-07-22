from django.db import models
from .restaurant import Restaurant
from .user import User


class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, limit_choices_to={
                                'user_type': 'employee'})
    restaurant = models.ForeignKey(
        Restaurant, on_delete=models.CASCADE, related_name='employees')
    position = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.user.email} - {self.position} at {self.restaurant.name}"
