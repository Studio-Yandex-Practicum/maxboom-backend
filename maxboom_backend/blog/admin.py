from django.contrib import admin
from django.utils.html import format_html

from .models import Category, Tag, Post, PostTag


class PostTagInLine(admin.TabularInline):
    """
    Инлайн для постов и тегов.
    """
    model = PostTag
    extra = 1


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    """
    Админка для постов.
    """
    def image_preview(self, obj):
        return format_html(
            '<img src="{}" style="max-width:100px; max-height:100px"/>'.format(
                obj.image.url))

    image_preview.short_description = 'Изображение'

    list_display = (
        'pk',
        'pub_date',
        'title',
        'text',
        'category',
        'author',
        'slug',
        'image_preview',
        'meta_title',
        'meta_description',
    )
    list_filter = (
        'author',
        'title',
        'category',
        'tags',
    )
    inlines = (PostTagInLine,)


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


@admin.register(PostTag)
class PostTagAdmin(admin.ModelAdmin):
    """
    Админка для постов и тегов.
    """
    list_display = (
        'pk',
        'post',
        'tag',
    )
