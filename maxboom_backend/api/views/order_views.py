from django.db import transaction
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import (OpenApiParameter, extend_schema,
                                   extend_schema_view)
from rest_framework import serializers, status, viewsets
from rest_framework.response import Response

from api.permissions.order_permissions import (IsOwnerOrAdmin,
                                               IsOwnerOrAdminRefund)
from api.serializers.order_serializers import (CommodityRefundSerializer,
                                               OrderRefundSerializer,
                                               OrderSerializer)
from cart.utils import get_cart
from order.models import CommodityRefund, Order, OrderRefund


@extend_schema(
    tags=["Заказ"],
)
@extend_schema_view(
    create=extend_schema(
        summary='Отмена заказа',
        description="""Отмена выполняется успешно, если
        ранее не было оформлено частичного возврата отдельных товаров
        """,
        parameters=[
            OpenApiParameter(
                name='order',
                location=OpenApiParameter.PATH,
                description='id заказа',
                required=True,
                type=int
            ),
        ]
    )
)
class OrderCancelViewSet(viewsets.ModelViewSet):
    http_method_names = ('post', 'head', 'options')
    pagination_class = None
    serializer_class = OrderSerializer

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        order = get_object_or_404(Order, pk=self.kwargs.get('order'))
        self.check_object_permissions_custom(self.request, obj=order)
        if order.status == 'отменен':
            raise serializers.ValidationError('Заказ ранее отменен')
        if order.status == 'выдан':
            raise serializers.ValidationError(
                'Необходимо оформить возврат'
                ' OrderRefund, т.к. заказ "выдан".'
            )
        if order.refunds.all().exists():
            raise serializers.ValidationError(
                'Необходимо оформить возврат'
                ' OrderRefund. Частичная отмена заказа невозможна'
            )
        order.status = 'отменен'
        order.save()
        if not order.is_paid:

            serializer = self.get_serializer(order)
            return Response(
                serializer.data, status=status.HTTP_200_OK
            )
        order_refund = OrderRefund.objects.create(order=order)
        for obj in order.commodities.all():
            CommodityRefund.objects.create(
                commodity=obj,
                refund=order_refund,
                quantity=obj.quantity
            )
        serializer = self.get_serializer(order)
        return Response(
            serializer.data, status=status.HTTP_200_OK
        )

    def check_object_permissions_custom(self, request, obj):
        """
        Check if the request should be permitted for a given object.
        Raises an appropriate exception if the request is not permitted.
        """
        permission = IsOwnerOrAdmin()
        if not permission.has_object_permission(request, self, obj):
            self.permission_denied(
                request,
                message=getattr(permission, 'message', None),
                code=getattr(permission, 'code', None)
            )


@extend_schema(
    tags=["Заказ"],
)
@extend_schema_view(
    create=extend_schema(
        summary='Оформление возврата к заказу',
        description="""Оформление возврата согласно
        предоставленным данным о количестве и id товара
        """,
        parameters=[
            OpenApiParameter(
                name='order',
                location=OpenApiParameter.PATH,
                description='id заказа',
                required=True,
                type=int
            ),
        ]
    ),
    list=extend_schema(
        summary='Просмотр возвратов к заказу',
    ),
    retrieve=extend_schema(
        summary='Просмотр возврата к заказу',
        parameters=[
            OpenApiParameter(
                name='order',
                location=OpenApiParameter.PATH,
                description='id заказа',
                required=True,
                type=int
            ),
            OpenApiParameter(
                name='id',
                location=OpenApiParameter.PATH,
                description='id возврата заказа',
                required=True,
                type=int
            ),
        ]
    )
)
class OrderRefundViewSet(viewsets.ModelViewSet):
    http_method_names = ('post', 'get', 'head', 'options')
    pagination_class = None
    serializer_class = OrderRefundSerializer
    permission_classes = (IsOwnerOrAdminRefund,)

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        order = get_object_or_404(Order, pk=self.kwargs.get('order'))
        self.check_object_permissions_custom(self.request, obj=order)
        order_refund = OrderRefund.objects.create(order=order)
        commodities = request.data.get('commodities', False)
        serializer_commodities = CommodityRefundSerializer(
            data=commodities, many=True, order=order)
        serializer_commodities.is_valid(raise_exception=True)
        self.perform_create(serializer_commodities, order_refund=order_refund)
        serializer = self.get_serializer(order_refund)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )

    def perform_create(self, serializer, order_refund):
        serializer.save(
            refund=order_refund
        )

    def get_queryset(self):
        order = get_object_or_404(Order, pk=self.kwargs.get('order'))
        self.check_object_permissions_custom(self.request, obj=order)
        return order.refunds.all()

    def check_object_permissions_custom(self, request, obj):
        """
        Check if the request should be permitted for a given object.
        Raises an appropriate exception if the request is not permitted.
        """
        permission = IsOwnerOrAdmin()
        if not permission.has_object_permission(request, self, obj):
            self.permission_denied(
                request,
                message=getattr(permission, 'message', None),
                code=getattr(permission, 'code', None)
            )


@extend_schema(
    tags=["Заказ"],
)
@extend_schema_view(
    create=extend_schema(
        summary='Оформление заказа',
    ),
    list=extend_schema(
        summary='Просмотр заказов',
    ),
    retrieve=extend_schema(
        summary='Просмотр заказа',
        parameters=[
            OpenApiParameter(
                name='id',
                location=OpenApiParameter.PATH,
                description='id заказа',
                required=True,
                type=int
            ),
        ]
    )
)
class OrderViewSet(viewsets.ModelViewSet):
    http_method_names = ('post', 'get', 'head', 'options')
    pagination_class = None
    serializer_class = OrderSerializer
    permission_classes = (IsOwnerOrAdmin,)

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            if user.is_staff:
                return Order.objects.all()
            order = Order.objects.filter(user=user)
            if order.exists():
                return order
        session_id = self.request.session.get('anonymous_id')
        return Order.objects.filter(session_id=session_id)

    @transaction.atomic
    def perform_create(self, serializer):
        user = self.request.user
        cart = get_cart(self.request)
        if not cart.products.all():
            raise serializers.ValidationError('Добавьте товары в корзину')
        if user.is_authenticated:
            serializer.save(
                user=user,
                is_active=True,
            )
        else:
            serializer.save(
                session_id=str(cart.session_id),
                is_active=False,
            )
        cart.delete()
