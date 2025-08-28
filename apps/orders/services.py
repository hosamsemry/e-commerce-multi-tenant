# apps/orders/services.py
import requests
from django.conf import settings

def get_paymob_token():
    url = settings.PAYMOB_AUTH_URL
    data = {"api_key": settings.PAYMOB_API_KEY}
    res = requests.post(url, json=data)
    res.raise_for_status()
    return res.json()["token"]

def register_paymob_order(order, token):
    url = settings.PAYMOB_ORDER_URL
    items = [{
        "name": item.product.title,
        "amount_cents": int(item.price * item.quantity * 100),
        "quantity": item.quantity
    } for item in order.items.all()]

    data = {
        "auth_token": token,
        "delivery_needed": False,
        "merchant_id": settings.PAYMOB_MERCHANT_ID,
        "amount_cents": int(sum(i['amount_cents'] for i in items)),
        "currency": "EGP",
        "items": items,
        "merchant_order_id": str(order.id),
    }
    res = requests.post(url, json=data)
    res.raise_for_status()
    return res.json()

def generate_payment_key(order, billing_data, token):
    url = settings.PAYMOB_PAYMENT_KEY_URL
    amount_cents = int(sum(i.price * i.quantity for i in order.items.all()) * 100)
    
    data = {
        "auth_token": token,
        "amount_cents": amount_cents,
        "expiration": 3600,
        "order_id": order.paymob_order_id,
        "billing_data": billing_data,
        "currency": "EGP",
        "integration_id": settings.PAYMOB_INTEGRATION_ID,
    }
    res = requests.post(url, json=data)
    res.raise_for_status()
    return res.json()["token"]
