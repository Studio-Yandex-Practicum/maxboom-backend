from rest_framework import viewsets

from api.serializers.news_serializers import NewsSerializer
from news.models import News

from drf_spectacular.utils import extend_schema


@extend_schema(
        description='Получение списка всех доступных новостей,\n'
        'либо одной новости по slug (только безопасные запросы).',
        responses={200: NewsSerializer(many=True)},
    )
class NewsViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Вьюсет только для SAFE methods к новостям.
    """

    queryset = News.objects.all()
    serializer_class = NewsSerializer
    lookup_field = 'slug'

    def get_queryset(self):
        return News.objects.all().order_by('-pub_date')
