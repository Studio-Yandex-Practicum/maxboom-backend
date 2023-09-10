from django.urls import include, path
from rest_framework import routers

from api.views.news_views import NewsViewSet

router = routers.DefaultRouter()
router.register(r'shopnews', NewsViewSet)

urlpatterns = [
    path('', include(router.urls))
]
