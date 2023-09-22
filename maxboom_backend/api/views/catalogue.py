from rest_framework import viewsets
from catalogue.models import Category, Product, Brand
from api.serializers.catalogue import (
    CategorySerializer, ProductSerializer, BrandSerializer,
)
from api.permissions.catalogue import IsAdminOrReadOnly


class CategoryViewSet(viewsets.ModelViewSet):
    '''Вьюсет для категорий.'''

    lookup_field = 'slug'
    queryset = Category.objects.all().prefetch_related(
        'products', 'root__root__root', 'branches__branches__branches',
    )
    serializer_class = CategorySerializer
    permission_classes = (IsAdminOrReadOnly,)
    pagination_class = None


class BrandViewSet(viewsets.ModelViewSet):
    '''Вьюсет для производителей.'''

    lookup_field = 'slug'
    queryset = Brand.objects.all().prefetch_related('products', )
    serializer_class = BrandSerializer
    permission_classes = (IsAdminOrReadOnly,)
    pagination_class = None


class ProductViewSet(viewsets.ModelViewSet):
    '''Вьюсет для товаров.'''

    lookup_field = 'slug'
    queryset = Product.objects.all().prefetch_related(
        'category__root__root__root', 'images',)
    serializer_class = ProductSerializer
    permission_classes = (IsAdminOrReadOnly,)
