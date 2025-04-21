from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Profile
from exp.models import Wallet
from CustomUser.models import CustomUser


@receiver(post_save, sender=CustomUser)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    else:
        instance.profile.save()

@receiver(post_save, sender=CustomUser)
def create_wallet(sender, instance, created, **kwargs):
    if created:
        Wallet.objects.create(user=instance, balance=0)
    else:
        instance.wallet.save()

