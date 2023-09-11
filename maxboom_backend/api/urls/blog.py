from django.urls import include, path
from rest_framework import routers

from api.views.blog import (PostViewSet, CategoryViewSet)


router = routers.DefaultRouter()
router.register(r'shopblog', PostViewSet)
router.register(r'shopblog/(?P<category_id>\d+)',
                CategoryViewSet, basename='categories')


urlpatterns = [
    path('', include(router.urls))
]
