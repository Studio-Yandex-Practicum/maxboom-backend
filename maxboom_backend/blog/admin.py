from django.contrib import admin
from django.utils.html import format_html

from .models import Category, Post, Tag, Comments


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    """
    Админка для постов.
    """

    list_display = (
        'pk',
        'pub_date',
        'title',
        'short_text_view',
        'category',
        'show_tags',
        'author',
        'image_preview',
        'show_comments',
        'views',
        'slug',
        'meta_title',
        'meta_description',
    )
    list_filter = (
        'author',
        'title',
        'category',
        'tags',
    )
    filter_horizontal = ('tags',)
    empty_value_display = '-пусто-'

    @admin.display(description='Изображение')
    def image_preview(self, obj):
        try:
            return format_html(
                '<img src="{}" style="max-width:100px; max-height:100px"/>'.format(
                    obj.image.url))
        except ValueError:
            pass

    @admin.display(description='Теги')
    def show_tags(self, obj):
        tags = [tag.name for tag in obj.tags.all()]
        return ', '.join(tags) if len(obj.tags.all()) > 1 else '-пусто-'

    @admin.display(description='Текст')
    def short_text_view(self, obj):
        return obj.text[:50] + '...' if len(obj.text) > 50 else obj.text[:50]

    @admin.display(description='Комментарии')
    def show_comments(self, obj):
        return len(Comments.objects.select_related(
            'post').filter(post=obj))


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """
    Админка для категорий.
    """

    list_display = (
        'pk',
        'title',
        'slug',
        'meta_title',
        'meta_description',
    )
    list_filter = (
        'title',
    )
    empty_value_display = '-пусто-'


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    """
    Админка для тегов.
    """

    list_display = (
        'name',
    )
    list_filter = (
        'name',
    )


@admin.register(Comments)
class CommentsAdmin(admin.ModelAdmin):
    """
    Админка для комментариев.
    """

    list_display = (
        'id',
        'author',
        'post',
        'short_comment_view',
        'pub_date',
        'is_published',
    )
    list_filter = (
        'author',
        'pub_date',
        'is_published',
    )

    @admin.display(description='Комментарии')
    def short_comment_view(self, obj):
        return obj.text[:50] + '...' if len(obj.text) > 50 else obj.text[:50]
