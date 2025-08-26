from django.contrib import admin
from .models import *


class ProductImageInline(admin.TabularInline):
    model = ProductImage


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    autocomplete_fields = ["collection"]
    inlines = [ProductImageInline]
    list_display = ["title", "price", "collection"]
    list_editable = ["price"]
    search_fields = ["title"]


@admin.register(Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ["title"]
    search_fields = ["title"]


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['user', 'product','created_at']
    list_filter = ['created_at']
    search_fields = ['user__username', 'product__title']
