from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views.shop_reviews_views import (ReplayToReviewViewSet,
                                          ShopReviewsViewSet)

router = DefaultRouter()
router.register(r'store-reviews', ShopReviewsViewSet, basename='store-reviews')
router.register(r'store-reviews/(?P<review_id>\d+)/replay',
                ReplayToReviewViewSet, basename='replay')

urlpatterns = [
    path('', include(router.urls)),
]
