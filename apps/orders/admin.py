from django.contrib import admin
from .models import Order, OrderItem, Address, Cart, CartItem


admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Address)
admin.site.register(Cart)
admin.site.register(CartItem)