from django.db import transaction
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAdminUser

from api.permissions.shop_reviews_permissions import IsAdminOrAnyUser
from api.serializers.shop_reviews_serializers import (
    ReplayToReviewAdminSerializer, ShopReviewsAdminSerializer,
    ShopReviewsSerializer)
from shop_reviews.models import ReplayToReview, ShopReviews


class ReplayToReviewViewSet(viewsets.ModelViewSet):
    http_method_names = ('get', 'post', 'put', 'patch',
                         'delete', 'head', 'options')
    serializer_class = ReplayToReviewAdminSerializer
    permission_classes = (IsAdminUser,)
    pagination_class = None

    @transaction.atomic
    def perform_create(self, serializer):
        review = get_object_or_404(
            ShopReviews, pk=self.kwargs.get('review_id'))
        serializer.save(review_id=review)

    def get_queryset(self):
        queryset = ReplayToReview.objects.filter(
            review_id=self.kwargs.get('review_id')
        )
        return queryset


class ShopReviewsViewSet(viewsets.ModelViewSet):
    http_method_names = ('get', 'post', 'patch', 'put',
                         'delete', 'head', 'options')
    pagination_class = PageNumberPagination
    permission_classes = (IsAdminOrAnyUser,)

    def get_serializer_class(self):
        if self.request.user and self.request.user.is_staff:
            return ShopReviewsAdminSerializer
        return ShopReviewsSerializer

    def get_queryset(self):
        if self.request.user and self.request.user.is_staff:
            return ShopReviews.objects.prefetch_related(
                'replay'
            ).all()
        return ShopReviews.objects.prefetch_related(
            'replay'
        ).all().filter(is_published=True)
