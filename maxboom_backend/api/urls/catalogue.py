from api.views.catalogue import BrandViewSet, CategoryViewSet, ProductViewSet
from django.urls import include, path
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('categories', CategoryViewSet, basename='category')
router.register('products', ProductViewSet, basename='product')
router.register('brands', BrandViewSet, basename='brand')


urlpatterns = [
    path('catalogue/', include(router.urls)),
]
