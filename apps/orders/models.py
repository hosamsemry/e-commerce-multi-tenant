import uuid
from django.db import models
from apps.accounts.models import User
from apps.products.models import Product
from apps.tenancy.models import Tenant


class Order(models.Model):
    PENDING = 'P'
    COMPLETE = 'C'
    CANCELED = 'X'
    STATUS_CHOICES = [
        (PENDING, 'Pending'),
        (COMPLETE, 'Complete'),
        (CANCELED, 'Canceled'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name="orders")

    customer = models.ForeignKey(User, on_delete=models.PROTECT, related_name="orders")
    placed_at = models.DateTimeField(auto_now_add=True)
    payment_status = models.CharField(max_length=1, choices=STATUS_CHOICES, default=PENDING)

    paymob_order_id = models.CharField(max_length=100, blank=True, null=True)
    paymob_transaction_id = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"Order {self.id} - {self.get_payment_status_display()}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.PROTECT, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name='orderitems')
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)  # better to allow > 9999

    def __str__(self):
        return f"{self.product.title} x {self.quantity}"


class Address(models.Model):
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name="addresses")
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="addresses")
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.street}, {self.city}"


class Cart(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name="carts")
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="carts", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField()

    class Meta:
        unique_together = [['cart', 'product']]

    def __str__(self):
        return f"{self.product.title} ({self.quantity})"
