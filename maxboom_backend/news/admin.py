from django.contrib import admin
from django.utils.html import format_html

from news.models import News


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    """
    Админка для новостей.
    """

    @admin.display(description='Изображение')
    def image_preview(self, obj):
        try:
            return format_html(
                '<img src="{}" style="max-width:50px; max-height:50px"/>'.
                format(obj.image.url))
        except ValueError:
            pass

    list_display = (
        'pk',
        'pub_date',
        'title',
        'text',
        'image_preview',
        'slug',
        'meta_title',
        'meta_description',)
    list_filter = (
        'title',
        'pub_date',)
    search_fields = ('title',)
