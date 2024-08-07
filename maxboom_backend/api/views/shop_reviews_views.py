from django.db import transaction
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import OpenApiParameter, OpenApiExample
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response

from api.permissions.shop_reviews_permissions import IsAdminOrAnyUser
from api.serializers.shop_reviews_serializers import (
    ReplayToReviewAdminSerializer, ShopReviewsAdminSerializer,
    ShopReviewsSerializer)
from shop_reviews.models import ReplayToReview, ShopReviews


@extend_schema(
    tags=["Отзывы о магазине"],
)
@extend_schema_view(
    list=extend_schema(
        summary='Получение списка ответов на отзыв',
        parameters=[
            OpenApiParameter(
                name='review_id',
                location=OpenApiParameter.PATH,
                description='id отзыва о магазине',
                required=True,
                type=int
            ),
        ]
    ),
    retrieve=extend_schema(
        summary='Получение отдельного ответа на отзыв',
        parameters=[
            OpenApiParameter(
                name='review_id',
                location=OpenApiParameter.PATH,
                description='id отзыва о магазине',
                required=True,
                type=int
            ),
            OpenApiParameter(
                name='id',
                location=OpenApiParameter.PATH,
                description='id ответа на отзыв',
                required=True,
                type=int
            ),
        ]
    ),
    create=extend_schema(
        summary='Запись ответа на отзыв',
        description='Запись ответа на отзыв, доступна только администратору',
        parameters=[
            OpenApiParameter(
                name='review_id',
                location=OpenApiParameter.PATH,
                description='id отзыва о магазине',
                required=True,
                type=int
            ),
        ]
    ),
    update=extend_schema(
        summary='Замена ответа на отзыв',
        description='Замена ответа на отзыв, доступна только администратору',
        parameters=[
            OpenApiParameter(
                name='review_id',
                location=OpenApiParameter.PATH,
                description='id отзыва о магазине',
                required=True,
                type=int
            ),
            OpenApiParameter(
                name='id',
                location=OpenApiParameter.PATH,
                description='id ответа на отзыв',
                required=True,
                type=int
            ),
        ]
    ),
    partial_update=extend_schema(
        summary='Частичная замена ответа на отзыв',
        description='''
        Частичная замена ответа на отзыв, доступна только администратору
        ''',
        parameters=[
            OpenApiParameter(
                name='review_id',
                location=OpenApiParameter.PATH,
                description='id отзыва о магазине',
                required=True,
                type=int
            ),
            OpenApiParameter(
                name='id',
                location=OpenApiParameter.PATH,
                description='id ответа на отзыв',
                required=True,
                type=int
            ),
        ]
    ),
    destroy=extend_schema(
        summary='Удаление ответа на отзыв',
        description='Удаление ответа на отзыв, доступна только администратору',
        parameters=[
            OpenApiParameter(
                name='review_id',
                location=OpenApiParameter.PATH,
                description='id отзыва о магазине',
                required=True,
                type=int
            ),
            OpenApiParameter(
                name='id',
                location=OpenApiParameter.PATH,
                description='id ответа на отзыв',
                required=True,
                type=int
            ),
        ]
    ),
)
class ReplayToReviewViewSet(viewsets.ModelViewSet):
    """Ответ на отзыв"""
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


@extend_schema(
    tags=["Отзывы о магазине"],
    summary='Отзывы о магазине'
)
@extend_schema_view(
    list=extend_schema(
        summary='Получение списка отзывов о магазине',
    ),
    retrieve=extend_schema(
        summary='Получение отдельного отзыва о магазине',
        parameters=[
            OpenApiParameter(
                name='id',
                location=OpenApiParameter.PATH,
                description='id отзыва о магазине',
                required=True,
                type=int
            ),
        ]
    ),
    create=extend_schema(
        summary='Запись отзыва о магазине',
    ),
    update=extend_schema(
        summary='Замена отзыва о магазине',
        description='''
        Замена отзыва о магазине, доступна только администратору
        ''',
        parameters=[
            OpenApiParameter(
                name='id',
                location=OpenApiParameter.PATH,
                description='id отзыва о магазине',
                required=True,
                type=int
            ),
        ]
    ),
    partial_update=extend_schema(
        summary='Частичная замена отзыва о магазине',
        description='''
        Частичная замена отзыва о магазине, доступна только администратору
        ''',
        parameters=[
            OpenApiParameter(
                name='id',
                location=OpenApiParameter.PATH,
                description='id отзыва о магазине',
                required=True,
                type=int
            ),
        ]
    ),
    destroy=extend_schema(
        summary='Удаление отзыва о магазине',
        description='''
        Удаление отзыва о магазине, доступна только администратору
        ''',
        parameters=[
            OpenApiParameter(
                name='id',
                location=OpenApiParameter.PATH,
                description='id отзыва о магазине',
                required=True,
                type=int
            ),
        ]
    ),
    average_rate=extend_schema(
        summary='Среднее значение рейтинга',
        description='''
        Получение средней оценки магазина
        ''',
        examples=[
            OpenApiExample(
                'Среднее значение рейтинга',
                value={
                    'delivery_speed_score__avg': 2.5,
                    'quality_score__avg': 2.5,
                    'price_score__avg': 3.0,
                    'average_score__avg': 2.7
                },
                status_codes=[str(status.HTTP_200_OK)],
                response_only=True,
            ),
        ],
    )
)
class ShopReviewsViewSet(viewsets.ModelViewSet):
    """Отзыв о магазине"""
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

    @action(methods=['get'], url_path='average-rate', detail=False)
    def average_rate(self, request):
        data = self.get_queryset().aggregate(
            Avg('delivery_speed_score'), Avg('quality_score'),
            Avg('price_score')
        )
        for key, val in data.items():
            data[key] = round(val, 2)
        data['average_score__avg'] = round(sum(data.values()) / 3, 1)
        return Response(data=data)
