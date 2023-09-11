from rest_framework import serializers

from blog.models import Post, Category, Tag


class CategorySerializer(serializers.ModelSerializer):
    """
    Сериализует данные для категорий.
    """

    class Meta:
        model = Category
        fields = (
            'title',
            'slug',
            'meta_title',
            'meta_description',
        )


class TagSerializer(serializers.ModelSerializer):
    """
    Сериализует данные для тегов.
    """

    class Meta:
        model = Tag
        fields = ('name',)


class PostSerializer(serializers.ModelSerializer):
    """
    Сериализует данные для постов.
    """
    category = CategorySerializer()
    tags = TagSerializer(many=True)
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username')

    class Meta:
        model = Post
        fields = (
            'id',
            'title',
            'text',
            'author',
            'image',
            'category',
            'tags',
            'slug',
            'meta_title',
            'meta_description',
        )
        # read_only_fields = fields
