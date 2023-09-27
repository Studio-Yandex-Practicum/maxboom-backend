from rest_framework import serializers
from stories.models import Story, Picture


class PictureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Picture
        fields = ('image',)


class StorySerializer(serializers.ModelSerializer):
    pictures = PictureSerializer(many=True)

    class Meta:
        model = Story
        fields = ('id', 'name', 'link', 'pictures')
