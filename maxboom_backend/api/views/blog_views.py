from rest_framework import viewsets

from api.serializers.blog_serializers import (CategoryDetailSerializer,
                                              CategoryListSerializer,
                                              PostSerializer)
from blog.models import Category, Post


class PostViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Вьюсет только для SAFE methods к постам.
    """

    queryset = Post.objects.all()
    serializer_class = PostSerializer
    lookup_field = 'slug'

    def get_queryset(self):
        return Post.objects.all().order_by('-pub_date')


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Вьюсет только для SAFE methods к категориям.
    """

    queryset = Category.objects.all()
    lookup_field = 'slug'

    def get_serializer_class(self):
        if 'slug' in self.kwargs:
            return CategoryDetailSerializer
        return CategoryListSerializer

    def get_queryset(self):
        return Category.objects.all().order_by('title')
