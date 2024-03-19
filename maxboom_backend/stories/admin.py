from django.contrib import admin
from django.utils.html import format_html

from stories.models import Story, Picture


class PictureInline(admin.TabularInline):
    model = Story.pictures.through


@admin.register(Story)
class StoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'link', 'image_preview',)
    inlines = [PictureInline]

    def image_preview(self, obj):
        print(obj.pictures.all())
        pictures = [
            (f'<img src="{pic.image.url}" style="max-width:100px; '
             'max-height:100px"/>') for pic in obj.pictures.all()
        ]

        result = '; '.join(pictures)
        try:
            return format_html(result)
        except ValueError:
            pass
    image_preview.short_description = 'Изображение'


@admin.register(Picture)
class PictureAdmin(admin.ModelAdmin):
    list_display = ('image', 'story_name')

    def story_name(self, obj):
        return ", ".join([story.name for story in obj.stories.all()])
    story_name.short_description = "Stories"
