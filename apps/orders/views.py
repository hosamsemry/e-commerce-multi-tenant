from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.conf import settings
from django.db import transaction

from .models import Order, OrderItem, Cart, CartItem, Address
from .serializers import (
    OrderSerializer,
    OrderItemSerializer,
    CartSerializer,
    CartItemSerializer,
    AddressSerializer,
)

import requests, json


class AddressViewSet(viewsets.ModelViewSet):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer

    def perform_create(self, serializer):
        serializer.save(
            tenant=self.request.tenant,
            customer=self.request.user
        )


class CartViewSet(viewsets.ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer

    def perform_create(self, serializer):
        serializer.save(
            tenant=self.request.tenant,
            customer=self.request.user
        )


class CartItemViewSet(viewsets.ModelViewSet):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all().select_related("customer").prefetch_related("items")
    serializer_class = OrderSerializer

    @action(detail=False, methods=["post"], url_path="checkout")
    def checkout(self, request):
        cart_id = request.data.get("cart_id")
        if not cart_id:
            return Response({"error": "cart_id is required"}, status=400)

        try:
            cart = Cart.objects.get(id=cart_id, tenant=request.tenant)
        except Cart.DoesNotExist:
            return Response({"error": "Cart not found"}, status=404)

        if not cart.items.exists():
            return Response({"error": "Cart is empty"}, status=400)

        with transaction.atomic():
            order = Order.objects.create(
                tenant=request.tenant,
                customer=request.user,
                payment_status=Order.PENDING,
            )

            total = 0
            for item in cart.items.all():
                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    quantity=item.quantity,
                    price=item.product.price,
                )
                total += item.quantity * item.product.price

            cart.items.all().delete()

            token = get_paymob_token()
            paymob_order = register_paymob_order(order, total, token)
            order.paymob_order_id = paymob_order["id"]
            order.save()

            billing_data = {
                "apartment": "NA",
                "email": request.user.email,
                "floor": "NA",
                "first_name": request.user.first_name or "Customer",
                "last_name": request.user.last_name or "",
                "phone_number": getattr(request.user, "phone", ""),
                "street": "NA",
                "building": "NA",
                "city": "Cairo",
                "country": "EG",
            }

            payment_token = generate_payment_key(order, billing_data, total, token)

            return Response({
                "order_id": order.id,
                "paymob_order_id": paymob_order["id"],
                "iframe_url": f"https://accept.paymob.com/api/acceptance/iframes/{settings.PAYMOB_IFRAME_ID}?payment_token={payment_token}",
                "amount_cents": int(total * 100),
            }, status=201)


class OrderItemViewSet(viewsets.ModelViewSet):
    queryset = OrderItem.objects.all().select_related("product", "order")
    serializer_class = OrderItemSerializer


# -------------------------------
# Paymob Helpers
# -------------------------------
def get_paymob_token():
    url = "https://accept.paymob.com/api/auth/tokens"
    resp = requests.post(url, json={"api_key": settings.PAYMOB_API_KEY})
    resp.raise_for_status()
    return resp.json()["token"]


def register_paymob_order(order, total, token):
    url = "https://accept.paymob.com/api/ecommerce/orders"
    data = {
        "auth_token": token,
        "delivery_needed": False,
        "amount_cents": int(total * 100),
        "currency": "EGP",
        "merchant_order_id": str(order.id),
        "items": [],
    }
    resp = requests.post(url, json=data)
    resp.raise_for_status()
    return resp.json()


def generate_payment_key(order, billing_data, total, token):
    url = "https://accept.paymob.com/api/acceptance/payment_keys"
    data = {
        "auth_token": token,
        "amount_cents": int(total * 100),
        "expiration": 3600,
        "order_id": order.paymob_order_id,
        "currency": "EGP",
        "integration_id": settings.PAYMOB_INTEGRATION_ID,
        "billing_data": billing_data,
    }
    resp = requests.post(url, json=data)
    resp.raise_for_status()
    return resp.json()["token"]


# -------------------------------
# Paymob Webhook
# -------------------------------
@csrf_exempt
def paymob_webhook(request):
    if request.method not in ["POST", "GET"]:
        return JsonResponse({"message": "Method not allowed"}, status=405)

    try:
        if request.method == "POST" and request.content_type == "application/json":
            raw_data = json.loads(request.body.decode())
            data = raw_data.get("obj", raw_data)
        elif request.method == "POST":
            data = request.POST.dict()
        else:
            data = request.GET.dict()
    except Exception:
        return JsonResponse({"message": "invalid json"}, status=400)

    success = str(data.get("success", "")).lower() == "true"
    order_data = data.get("order")
    paymob_order_id = str(order_data.get("id")) if isinstance(order_data, dict) else str(order_data)

    try:
        order = Order.objects.get(paymob_order_id=paymob_order_id)
        order.payment_status = Order.COMPLETE if success else Order.CANCELED
        order.paymob_transaction_id = str(data.get("id"))
        order.save()
        return JsonResponse({"message": "success"}, status=200)
    except Order.DoesNotExist:
        return JsonResponse({"message": "order not found"}, status=404)
