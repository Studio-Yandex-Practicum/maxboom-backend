from rest_framework import viewsets

from news.models import News
from api.serializers.news import NewsSerializer


class NewsViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Вьюсет только для SAFE methods к новостям.
    """
    queryset = News.objects.all()
    serializer_class = NewsSerializer
    lookup_field = 'slug'

    def get_queryset(self):
        return News.objects.all().order_by('-pub_date')
