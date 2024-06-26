from django.db.models.signals import post_save
from django.dispatch import receiver

from django.contrib.auth.models import User
from .models import Customer

@receiver(post_save, sender=User)
def create_customer_profile(sender, instance, created,**kwargs):

    if created:
        Customer.objects.create(user=instance)
        print('Profile created!')

@receiver(post_save, sender=User)
def update_customer_profile(sender, instance, created, **kwargs):

    if not created:
        Customer.objects.get_or_create(user=instance)
        instance.customer.save()
        print('profile updated')