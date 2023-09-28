from rest_framework import viewsets

from api.permissions.catalogue import IsAdminOrReadOnly
from api.serializers.catalogue import (BrandSerializer, CategorySerializer,
                                       ProductSerializer)
from catalogue.models import Brand, Category, Product


class CategoryViewSet(viewsets.ModelViewSet):
    '''Вьюсет для категорий.'''

    lookup_field = 'slug'
    queryset = Category.objects.all().prefetch_related(
        'products', 'root__root__root', 'branches__branches__branches',
    ).filter(is_prohibited=False)
    serializer_class = CategorySerializer
    permission_classes = (IsAdminOrReadOnly,)
    pagination_class = None


class BrandViewSet(viewsets.ModelViewSet):
    '''Вьюсет для производителей.'''

    lookup_field = 'slug'
    queryset = Brand.objects.all().prefetch_related('products',).filter(
        is_prohibited=False).filter(products__is_deleted=False)
    serializer_class = BrandSerializer
    permission_classes = (IsAdminOrReadOnly,)
    pagination_class = None


class ProductViewSet(viewsets.ModelViewSet):
    '''Вьюсет для товаров.'''

    lookup_field = 'slug'
    queryset = Product.objects.all().prefetch_related(
        'category__root__root__root', 'images',).filter(
            is_deleted=False, category__is_prohibited=False)
    serializer_class = ProductSerializer
    permission_classes = (IsAdminOrReadOnly,)
