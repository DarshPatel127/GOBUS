from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Profile
from exp.models import Wallet


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

def save_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)  # Create profile if it doesn't exist
    else:
        instance.profile.save()

@receiver(post_save, sender=User)
def create_wallet(sender, instance, created, **kwargs):
    if created:
        Wallet.objects.create(user=instance, balance=0)

def save_wallet(sender, instance, created, **kwargs):
    if created:
        Wallet.objects.create(user=instance)  # Create profile if it doesn't exist
    else:
        instance.wallet.save()
