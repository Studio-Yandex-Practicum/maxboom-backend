from rest_framework import viewsets
from catalogue.models import Category, Product, Brand, ProductImage
from api.serializers.catalogue import (
    CategorySerializer, ProductSerializer, BrandSerializer,
    ProductImageSerializer, CategoryProductSerializer,
    ProductNewSerializer
)
from api.permissions.catalogue import IsAdminOrReadOnly


class CategoryViewSet(viewsets.ModelViewSet):
    '''Вьюсет для категорий.'''

    lookup_field = 'slug'
    queryset = Category.objects.all().prefetch_related(
        'products', 'roots__root', 'branches__branch')
    serializer_class = CategoryProductSerializer
    permission_classes = (IsAdminOrReadOnly,)


class BrandViewSet(viewsets.ModelViewSet):
    '''Вьюсет для производителей.'''

    lookup_field = 'slug'
    queryset = Brand.objects.all().prefetch_related('products', )
    serializer_class = BrandSerializer
    permission_classes = (IsAdminOrReadOnly,)


class ProductViewSet(viewsets.ModelViewSet):
    '''Вьюсет для товаров.'''

    lookup_fields = ['pk', 'slug']
    queryset = Product.objects.all().prefetch_related(
        'category__roots__root', 'images', 'category__branches__branch')
    serializer_class = ProductNewSerializer
    permission_classes = (IsAdminOrReadOnly,)


class ProductImageViewSet(viewsets.ModelViewSet):
    '''Вьюсет для товаров.'''

    queryset = ProductImage.objects.all()
    serializer_class = ProductImageSerializer
    permission_classes = (IsAdminOrReadOnly,)
