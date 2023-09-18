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
        'text',
        'category',
        'show_tags',
        'author',
        'slug',
        'image_preview',
        'viewers',
        'comments',
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

    def image_preview(self, obj):
        try:
            return format_html(
                '<img src="{}" style="max-width:100px; max-height:100px"/>'.format(
                    obj.image.url))
        except ValueError:
            pass
    image_preview.short_description = 'Изображение'

    @admin.display(description='теги')
    def show_tags(self, obj):
        tags = [tag.name for tag in obj.tags.all()]
        if len(obj.tags.all()) > 0:
            return ', '.join(tags)


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
        'text',
        'pub_date',
        'is_published',
    )
    list_filter = (
        'author',
        'pub_date',
        'is_published',
    )