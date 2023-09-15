from rest_framework import serializers

from news.models import News


class NewsSerializer(serializers.ModelSerializer):
    """
    Сериализует данные для новостей.
    """

    class Meta:
        model = News
        fields = (
            'id',
            'title',
            'text',
            'image',
            'pub_date',
            'slug',
            'meta_title',
            'meta_description',
        )
        read_only_fields = fields
