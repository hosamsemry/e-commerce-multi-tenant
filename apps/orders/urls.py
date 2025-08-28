from rest_framework_nested import routers
from .views import *
from django.urls import path

router = routers.DefaultRouter()
router.register(r"addresses", AddressViewSet, basename="address")
router.register(r"carts", CartViewSet, basename="cart")
router.register(r"orders", OrderViewSet, basename="order")

carts_router = routers.NestedDefaultRouter(router,'carts',lookup='cart')
carts_router.register('items',CartItemViewSet,basename='cart-items')

order_router = routers.NestedDefaultRouter(router,'orders',lookup='order')
order_router.register('items',OrderItemViewSet,basename='order-items')

urlpatterns =[
    path('paymob-webhook/',paymob_webhook,name='paymob-webhook')
]+ router.urls + carts_router.urls + order_router.urls