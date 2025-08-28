from rest_framework import serializers
from .models import Order, OrderItem, Cart, CartItem, Address


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ["id", "street", "city", "customer", "tenant"]


class CartItemSerializer(serializers.ModelSerializer):
    product_title = serializers.CharField(source="product.title", read_only=True)

    class Meta:
        model = CartItem
        fields = ["id", "cart", "product", "product_title", "quantity"]


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)

    class Meta:
        model = Cart
        fields = ["id", "customer", "tenant", "created_at", "items"]


class OrderItemSerializer(serializers.ModelSerializer):
    product_title = serializers.CharField(source="product.title", read_only=True)

    class Meta:
        model = OrderItem
        fields = ["id", "order", "product", "product_title", "quantity", "price"]


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    customer_name = serializers.CharField(source="customer.username", read_only=True)

    class Meta:
        model = Order
        fields = [
            "id",
            "tenant",
            "customer",
            "customer_name",
            "placed_at",
            "paymob_order_id",
            "paymob_transaction_id",
            "items",
        ]
