from rest_framework.permissions import IsAuthenticated, AllowAny
from .permissions import IsSeller
from rest_framework.viewsets import ModelViewSet
from .models import Collection, Product
from .serializers import *
from django.db.models import Count


class CollectionViewSet(ModelViewSet):
    serializer_class = CollectionSerializer

    def get_permissions(self):
        if self.action in ["create", "update", "partial_update", "destroy"]:
            return [IsAuthenticated(), IsSeller()]
        return [AllowAny()]

    def get_queryset(self):
        tenant = self.request.tenant
        return Collection.objects.filter(products__seller__tenant=tenant).annotate(
            products_count=Count("products")
        )

    def perform_create(self, serializer):
        serializer.save(seller=self.request.user.seller_profile)


class ProductViewSet(ModelViewSet):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()

    def get_permissions(self):
        if self.action in ["create", "update", "partial_update", "destroy"]:
            return [IsAuthenticated(), IsSeller()]
        return [AllowAny()]

    def get_queryset(self):
        # print("DEBUG tenant:", self.request.tenant)
        # print("DEBUG user:", self.request.user, self.request.user.role)
        tenant = self.request.tenant
        user = self.request.user

        if user.is_authenticated and user.role == "seller":
            return Product.objects.filter(seller__user=user, seller__tenant=tenant)
        return Product.objects.filter(seller__tenant=tenant)

    def perform_create(self, serializer):
        serializer.save(seller=self.request.user.seller_profile)

class ProductImageViewSet(ModelViewSet):
    serializer_class = ProductImageSerializer

    def get_serializer_context(self):
        return {'product_id':self.kwargs['product_pk'],}

    def get_queryset(self):
        return ProductImage.objects.filter(product_id=self.kwargs['product_pk'])
    
class ReviewViewSet(ModelViewSet):
    serializer_class = ReviewSerializer

    def get_queryset(self):
        tenant = self.request.tenant
        return Review.objects.filter(product_id=self.kwargs['product_pk'], tenant=tenant)

    def get_serializer_context(self):
        return {'product_id':self.kwargs['product_pk']}   
