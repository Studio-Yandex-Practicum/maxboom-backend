from django.urls import include, path
from rest_framework import routers

from api.views.blog_views import CategoryViewSet, PostViewSet

router = routers.DefaultRouter()
router.register(r'posts', PostViewSet)
router.register(r'categories', CategoryViewSet)


urlpatterns = [
    path('shopblog/', include(router.urls)),
]
