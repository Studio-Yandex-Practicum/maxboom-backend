from rest_framework import serializers

from blog.models import Category, Post, Tag, Comments


class CategoryLightSerializer(serializers.ModelSerializer):
    """
    Сериализует данные для категорий
    без мета-данных.
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


class PostLightSerializer(serializers.ModelSerializer):
    """
    Сериализует данные для постов без мета-данных
    и категории при запросе в категориях по {slug}.
    """

    tags = TagSerializer(read_only=True, many=True)
    author = serializers.SerializerMethodField()
    comments_quantity = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = (
            'id',
            'title',
            'text',
            'pub_date',
            'author',
            'image',
            'tags',
            'views',
            'comments_quantity',
            'slug',
        )
        read_only_fields = fields

    def get_author(self, obj):
        if obj.author:
            return 'Администратор'

    def get_comments_quantity(self, obj):
        comments = Comments.objects.select_related(
            'post').filter(
                post=obj,
                is_published=True)
        return comments.count()


class PostSerializer(serializers.ModelSerializer):
    """
    Сериализует все данные для постов.
    """

    category = CategoryLightSerializer()
    tags = TagSerializer(many=True)
    author = serializers.SerializerMethodField()

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
            'views',
            'slug',
            'meta_title',
            'meta_description',
        )
        read_only_fields = fields

    def get_author(self, obj):
        if obj.author:
            return 'Администратор'


class CategoryListSerializer(serializers.ModelSerializer):
    """
    Сериализует данные для категорий
    при запросе всех категорий без постов.
    """

    class Meta:
        model = Category
        fields = (
            'title',
            'slug',
            'meta_title',
            'meta_description',
        )
        read_only_fields = fields


class CategoryDetailSerializer(serializers.ModelSerializer):
    """
    Сериализует данные для категорий c постами
    при запросе по {slug}.
    """

    posts = PostLightSerializer(many=True)

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


class CommentSerializer(serializers.ModelSerializer):
    """
    Сериализует данные для комментариев для чтения.
    """

    class Meta:
        model = Comments
        fields = (
            'id',
            'author',
            'text',
            'pub_date',
        )
        read_only_fields = fields


class CommentPostSerializer(serializers.ModelSerializer):
    """
    Сериализует данные для комментариев в случае их добавления.
    """

    class Meta:
        model = Comments
        fields = (
            'author',
            'text',
        )
