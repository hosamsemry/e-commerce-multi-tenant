from rest_framework import serializers
from .models import *

class CollectionSerializer(serializers.ModelSerializer):
    products_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Collection
        fields = ["id", "title", "products_count"]

class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ["id", "image"]


class ProductSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True, read_only=True)
    collection = serializers.StringRelatedField()
    seller = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Product
        fields = [
            "id", "seller", "title", "description", "price",
            "inventory", "last_updated", "collection", "images"
        ]


class ReviewSerializer(serializers.ModelSerializer):
    product = serializers.StringRelatedField()
    user = serializers.StringRelatedField(read_only=True)

    def create(self, validated_data):
        product_id = self.context['product_id']
        return Review.objects.create(product_id=product_id,**validated_data)
    class Meta:
        model = Review
        fields = ['id','user','product','description', 'rating', 'created_at']   