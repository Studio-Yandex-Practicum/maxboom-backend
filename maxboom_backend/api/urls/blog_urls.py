from django.urls import include, path, re_path
from rest_framework import routers

from api.views.blog_views import (CategoryViewSet,
                                  PostViewSet, CommentViewSet)

router = routers.DefaultRouter()
router.register(r'posts', PostViewSet)
router.register(r'categories', CategoryViewSet)


urlpatterns = [
    path('shopblog/', include(router.urls)),
    re_path(
        r'^shopblog/posts/(?P<post_slug>[\w-]+)/comments/$',
        CommentViewSet.as_view(
            {'get': 'list', 'post': 'create'}),
        name='post-comments'),
]
