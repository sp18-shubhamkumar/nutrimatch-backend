from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from .user_manager import UserManager
from django.db import models


class User(AbstractBaseUser, PermissionsMixin):
    USER_TYPE_CHOICES = (
        ('restaurant_admin', 'Restaurant Admin'),
        ('customer', 'Customer'),
    )

    email = models.EmailField(unique=True, max_length=255)
    user_type = models.CharField(max_length=25, choices=USER_TYPE_CHOICES)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return f"{self.email} ({self.user_type})"
