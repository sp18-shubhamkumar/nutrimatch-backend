from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, user_type=None):
        if not email:
            raise ValueError("Email is required")
        if not user_type:
            raise ValueError("User_Type is required")
        email = self.normalize_email(email)
        user = self.model(email=email, user_type=user_type)
        user.set_password(password)
        user.save(using=self.db)
        return user

    def create_superuser(self, email, password=None):
        user = self.model(email=self.normalize_email(email), user_type='admin')
        user.set_password(password)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self.db)
        return user
