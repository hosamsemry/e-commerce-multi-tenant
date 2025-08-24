from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings

from apps.marketplace.models import BuyerProfile, SellerProfile

User = settings.AUTH_USER_MODEL


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if not created:
        return

    if instance.role == "customer":
        BuyerProfile.objects.create(user=instance)
    elif instance.role == "seller":
        SellerProfile.objects.create(user=instance)
