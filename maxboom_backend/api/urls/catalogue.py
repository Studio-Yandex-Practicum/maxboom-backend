from api.views.catalogue import (
    BrandViewSet, CategoryViewSet, ProductViewSet,
    SearchView
)
from django.urls import include, path
from rest_framework.routers import DefaultRouter

app_name = 'catalogue'

router = DefaultRouter()
router.register('brand', BrandViewSet, basename='brand')
router.register('category', CategoryViewSet, basename='category')
router.register('', ProductViewSet, basename='product')


urlpatterns = [
    path('catalogue/', include(router.urls)),
    path('search/', SearchView.as_view(),
         name='search')
]
