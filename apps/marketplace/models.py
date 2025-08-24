from django.db import models
from django.conf import settings
from apps.tenancy.models import Tenant

User = settings.AUTH_USER_MODEL


class BuyerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="buyer_profile")
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name="buyers")
    loyalty_points = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"BuyerProfile({self.user.email})"


class SellerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="seller_profile")
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name="sellers")
    store_name = models.CharField(max_length=255)
    payout_account = models.CharField(max_length=255, blank=True, null=True)  # later for escrow/split payments
    rating = models.FloatField(default=0.0)

    def __str__(self):
        return f"SellerProfile({self.store_name})"
