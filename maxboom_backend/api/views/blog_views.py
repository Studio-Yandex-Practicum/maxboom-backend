from django.shortcuts import get_object_or_404
from rest_framework import viewsets

from api.serializers.blog_serializers import (CategoryDetailSerializer,
                                              CategoryListSerializer,
                                              PostSerializer,
                                              CommentSerializer,
                                              CommentPostSerializer)
from blog.models import Category, Post, Comments


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


class CommentViewSet(viewsets.ModelViewSet):
    """
    Вьюсет только для [GET, POST, HEAD] methods к комментариям.
    Доступ разрешен всем пользователем.
    """

    http_method_names = ['get', 'post', 'head']

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CommentPostSerializer
        return CommentSerializer

    def get_queryset(self):
        return Comments.objects.select_related(
            'post').filter(
                post__slug=self.kwargs[
                    'post_slug'], is_published=True)

    def perform_create(self, serializer):
        post_slug = self.kwargs['post_slug']
        post = get_object_or_404(Post, slug=post_slug)
        serializer.save(post=post)
