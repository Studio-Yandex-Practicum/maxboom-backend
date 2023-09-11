from rest_framework import viewsets

from blog.models import Post, Category, Tag, PostTag
from api.serializers.blog import (PostSerializer,
                                  CategorySerializer,)


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
    serializer_class = CategorySerializer
    # lookup_field = 'slug'

    def get_queryset(self):
        return Category.objects.all().order_by('-pub_date')
