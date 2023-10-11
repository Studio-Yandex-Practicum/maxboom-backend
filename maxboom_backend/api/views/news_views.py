from rest_framework import viewsets, status

from api.serializers.news_serializers import NewsSerializer
from news.models import News

from drf_spectacular.utils import (extend_schema,
                                   extend_schema_view,
                                   OpenApiParameter,
                                   OpenApiResponse)


@extend_schema(
    tags=['Shopnews'],
    description='Эндпоинт для доступа к новостям',
)
@extend_schema_view(
    list=extend_schema(
        summary='Получить список новостей',
        responses={
            status.HTTP_200_OK: NewsSerializer(many=True),
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
        summary='Получить отдельную новость',
        responses={
            status.HTTP_200_OK: NewsSerializer,
            status.HTTP_404_NOT_FOUND: OpenApiResponse(
                description='Страница не найдена.')
        },
        parameters=[
            OpenApiParameter(
                name='slug',
                location=OpenApiParameter.PATH,
                description='slug новости',
                required=True,
                type=str
            ),
        ]
    )
)
class NewsViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Вьюсет только для SAFE methods для доступа к новостям.
    """

    queryset = News.objects.all()
    serializer_class = NewsSerializer
    lookup_field = 'slug'

    def get_queryset(self):
        return News.objects.all().order_by('-pub_date')
