from django.shortcuts import get_object_or_404
from django.db import transaction
from rest_framework import viewsets, status
from rest_framework.response import Response

from api.serializers.blog_serializers import (CategoryDetailSerializer,
                                              CategoryListSerializer,
                                              PostSerializer,
                                              CommentSerializer,
                                              CommentPostSerializer)
from blog.models import Category, Post, Comments
from drf_spectacular.utils import (extend_schema,
                                   extend_schema_view,
                                   OpenApiParameter,
                                   OpenApiResponse)


@extend_schema(
    tags=['Блог'],
    description='Эндпоинт для доступа к постам блога',
)
@extend_schema_view(
    list=extend_schema(
        summary='Получение списка постов',
        responses={
            status.HTTP_200_OK: PostSerializer(many=True),
            status.HTTP_404_NOT_FOUND: OpenApiResponse(
                description='Страница не найдена.')
        },
        parameters=[
            OpenApiParameter(
                name='page',
                location=OpenApiParameter.QUERY,
                description='Номер страницы',
                required=False,
                type=int
            ),
        ],
    ),
    retrieve=extend_schema(
        summary='Получение отдельного поста',
        responses={
            status.HTTP_200_OK: PostSerializer,
            status.HTTP_404_NOT_FOUND: OpenApiResponse(
                description='Страница не найдена.')
        },
        parameters=[
            OpenApiParameter(
                name='slug',
                location=OpenApiParameter.PATH,
                description='slug поста',
                required=True,
                type=str
            ),
        ]
    )
)
class PostViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Вьюсет только для SAFE methods к постам.
    """

    queryset = Post.objects.all()
    serializer_class = PostSerializer
    lookup_field = 'slug'

    def get_queryset(self):
        return Post.objects.all().order_by('-pub_date')

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.views += 1
        instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


@extend_schema(
    tags=['Блог'],
    description='Эндпоинт для доступа к категориям блога',
)
@extend_schema_view(
    list=extend_schema(
        summary='Получение списка категорий',
        responses={
            status.HTTP_200_OK: CategoryListSerializer(many=True),
            status.HTTP_404_NOT_FOUND: OpenApiResponse(
                description='Страница не найдена.')
        },
        parameters=[
            OpenApiParameter(
                name='page',
                location=OpenApiParameter.QUERY,
                description='Номер страницы',
                required=False,
                type=int
            ),
        ],
    ),
    retrieve=extend_schema(
        summary='Получение отдельной категории',
        responses={
            status.HTTP_200_OK: CategoryDetailSerializer,
            status.HTTP_404_NOT_FOUND: OpenApiResponse(
                description='Страница не найдена.')
        },
        parameters=[
            OpenApiParameter(
                name='slug',
                location=OpenApiParameter.PATH,
                description='slug категории',
                required=True,
                type=str
            ),
        ]
    )
)
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


@extend_schema(
    tags=['Блог'],
    description='Эндпоинт для доступа к комментариям постов',
)
@extend_schema_view(
    list=extend_schema(
        summary='Получение списка комментариев',
        responses={
            status.HTTP_200_OK: CommentSerializer(many=True),
            status.HTTP_404_NOT_FOUND: OpenApiResponse(
                description='Страница не найдена.')
        },
        parameters=[
            OpenApiParameter(
                name='page',
                location=OpenApiParameter.QUERY,
                description='Номер страницы',
                required=False,
                type=int
            ),
            OpenApiParameter(
                name='post_slug',
                location=OpenApiParameter.PATH,
                description='slug поста',
                required=True,
                type=str
            ),
        ],
    ),
    create=extend_schema(
        summary='Создание комментария для поста',
        responses={
            status.HTTP_201_CREATED: CommentPostSerializer,
            status.HTTP_404_NOT_FOUND: OpenApiResponse(
                description='Страница не найдена.')
        },
        parameters=[
            OpenApiParameter(
                name='post_slug',
                location=OpenApiParameter.PATH,
                description='slug поста',
                required=True,
                type=str
            ),
        ]
    )
)
class CommentViewSet(viewsets.ModelViewSet):
    """
    Вьюсет только для [GET, POST, HEAD, OPTIONS] methods к комментариям.
    Доступ разрешен всем пользователем.
    """

    http_method_names = ['get', 'post', 'head', 'options']

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CommentPostSerializer
        return CommentSerializer

    def get_queryset(self):
        return Comments.objects.select_related(
            'post').filter(
                post__slug=self.kwargs[
                    'post_slug'], is_published=True)

    @transaction.atomic
    def perform_create(self, serializer):
        post_slug = self.kwargs['post_slug']
        post = get_object_or_404(Post, slug=post_slug)
        serializer.save(post=post)
