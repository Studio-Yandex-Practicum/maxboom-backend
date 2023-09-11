from rest_framework import serializers

from blog.models import Post, Category, Tag


class CategoryLightSerializer(serializers.ModelSerializer):
    """
    Сериализует данные для категорий без мета-данных.
    """

    class Meta:
        model = Category
        fields = (
            'title',
            'slug',
        )
        read_only_fields = fields


class TagSerializer(serializers.ModelSerializer):
    """
    Сериализует данные для тегов.
    """

    class Meta:
        model = Tag
        fields = ('name',)
        read_only_fields = fields


class PostSerializer(serializers.ModelSerializer):
    """
    Сериализует данные для постов.
    """
    category = CategoryLightSerializer()
    tags = TagSerializer(many=True)
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='email')

    class Meta:
        model = Post
        fields = (
            'id',
            'title',
            'text',
            'pub_date',
            'author',
            'image',
            'category',
            'tags',
            'slug',
            'meta_title',
            'meta_description',
        )
        read_only_fields = fields


class CategorySerializer(serializers.ModelSerializer):
    """
    Сериализует данные для категорий.
    """
    posts = PostSerializer(many=True)

    class Meta:
        model = Category
        fields = (
            'title',
            'slug',
            'meta_title',
            'meta_description',
            'posts',
        )
        read_only_fields = fields
