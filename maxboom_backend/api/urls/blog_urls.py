from django.urls import include, path
from rest_framework import routers

from api.views.blog_views import (PostViewSet, CategoryViewSet)


router = routers.DefaultRouter()
router.register(r'posts', PostViewSet, basename='post')
router.register(r'categories', CategoryViewSet, basename='category')


urlpatterns = [
    path('shopblog/', include(router.urls)),
]
