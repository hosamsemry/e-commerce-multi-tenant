from .views import *
from rest_framework_nested import routers

router = routers.DefaultRouter()
router.register("collections", CollectionViewSet, basename="collections")
router.register("products", ProductViewSet, basename="products")

products_router =  routers.NestedDefaultRouter(router, 'products', lookup='product')
products_router.register('reviews',ReviewViewSet,basename='product-reviews')
products_router.register('images',ProductImageViewSet,basename='product-images')

urlpatterns = router.urls + products_router.urls 
