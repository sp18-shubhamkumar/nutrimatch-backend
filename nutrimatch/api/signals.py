
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Customer, User

# print("Signals module loaded")


@receiver(post_save, sender=User)
def create_customer_profile(sender, instance, created, **kwargs):
    # print("Signal triggered for User post_save")
    if created and instance.user_type == 'customer':
        Customer.objects.create(user=instance)
