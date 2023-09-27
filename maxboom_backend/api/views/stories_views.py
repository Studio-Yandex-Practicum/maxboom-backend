from rest_framework import viewsets, mixins
from stories.models import Story
from api.serializers.stories_serializers import StorySerializer


class StoryViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Story.objects.all().filter(show=True)
    serializer_class = StorySerializer
