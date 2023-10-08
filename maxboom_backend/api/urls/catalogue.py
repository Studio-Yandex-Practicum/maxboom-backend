from api.views.catalogue import (
    BrandViewSet, CategoryViewSet, ProductViewSet
)
from django.urls import include, path
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('brand', BrandViewSet, basename='brand')
router.register('category', CategoryViewSet, basename='category')
router.register('', ProductViewSet, basename='product')


urlpatterns = [
    path('catalogue/', include(router.urls)),
]
