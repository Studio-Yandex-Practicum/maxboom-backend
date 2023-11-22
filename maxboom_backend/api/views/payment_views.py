import logging

from django.db import transaction
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import (OpenApiParameter, extend_schema,
                                   extend_schema_view)
from rest_framework import status, viewsets
from rest_framework.exceptions import APIException
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.serializers import ValidationError
from yookassa import Payment, Refund

from api.permissions.order_permissions import (IsOwnerOrAdmin,
                                               IsOwnerOrAdminPayment)
from api.serializers.payment_serializers import (PaymentSerializer,
                                                 PrePaymentSerializer,
                                                 PreRepaymentSerializer,
                                                 RepaymentSerializer)
from order.models import Order, OrderRefund
from payment.models import OrderPayment, Repayment


class RepeatPaymentException(APIException):
    status_code = 400
    default_detail = 'Статус платежа - succeeded.'
    default_code = 'Платеж оплачен.'


class RepeatRepaymentException(APIException):
    status_code = 400
    default_detail = (
        'Повторный возврат невозможен. '
        'Статус возврата платежа - succeeded.'
    )
    default_code = 'Возврат платежа выполнен.'


@extend_schema(
    tags=["Платеж"],
)
@extend_schema_view(
    create=extend_schema(
        summary='Возврат платежа',
        parameters=[
            OpenApiParameter(
                name='order',
                location=OpenApiParameter.PATH,
                description='id заказа',
                required=True,
                type=int
            ),
            OpenApiParameter(
                name='refund',
                location=OpenApiParameter.PATH,
                description='id возврата',
                required=True,
                type=int
            ),
        ]
    ),
    list=extend_schema(
        summary='Просмотр возвратов платежей',
        parameters=[
            OpenApiParameter(
                name='order',
                location=OpenApiParameter.PATH,
                description='id заказа',
                required=True,
                type=int
            ),
            OpenApiParameter(
                name='refund',
                location=OpenApiParameter.PATH,
                description='id возврата',
                required=True,
                type=int
            ),
        ]
    ),
    retrieve=extend_schema(
        summary='Просмотр возврата платежа',
        parameters=[
            OpenApiParameter(
                name='order',
                location=OpenApiParameter.PATH,
                description='id заказа',
                required=True,
                type=int
            ),
            OpenApiParameter(
                name='refund',
                location=OpenApiParameter.PATH,
                description='id возврата',
                required=True,
                type=int
            ),
            OpenApiParameter(
                name='id',
                location=OpenApiParameter.PATH,
                description='id возврата платежа',
                required=True,
                type=int
            ),
        ]
    )
)
class RepaymentView(viewsets.ModelViewSet):
    http_method_names = ('post', 'get', 'head', 'options')
    pagination_class = None
    serializer_class = RepaymentSerializer
    permission_classes = (IsAdminUser,)

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        order = get_object_or_404(Order, pk=self.kwargs.get('order'))
        refund = get_object_or_404(OrderRefund, pk=self.kwargs.get('refund'))
        payment = get_object_or_404(order.payments, status='succeeded')
        repayment = Repayment.objects.exclude(
            status='canceled').filter(order_refund=refund)
        if not repayment.exists():
            repayment = Repayment.objects.create(
                payment=payment,
                order_refund=refund
            )
        else:
            if repayment.filter(status='succeeded').exists():
                raise RepeatRepaymentException
            repayment = repayment[0]
        data = PreRepaymentSerializer(repayment).data
        try:
            resp = Refund.create(data['data'], data['idempotence_key'])
        except Exception as e:
            code = getattr(type(e), 'HTTP_CODE', False)
            if code:
                raise ValidationError(
                    detail=e, code=e.HTTP_CODE)
            raise ValidationError(f'{e}')
        else:
            repayment.refund_id = resp.id
            repayment.status = resp.status
            repayment.save(
                update_fields=('refund_id', 'status')
            )
            serializer = self.get_serializer(repayment)
            data = serializer.data
            headers = self.get_success_headers(serializer.data)
            return Response(
                data, status=status.HTTP_201_CREATED, headers=headers
            )

    def get_queryset(self):
        refund = get_object_or_404(OrderRefund, pk=self.kwargs.get('refund'))
        for obj in refund.repayments.exclude(
            refund_id__isnull=True,
            status__in=['canceled', 'succeeded']
        ):
            self.update_repayment(obj=obj)
        return refund.repayments.all()

    def update_repayment(self, obj):
        try:
            resp = Refund.find_one(refund_id=obj.refund_id)
        except Exception as e:
            code = getattr(type(e), 'HTTP_CODE', False)
            if code:
                raise ValidationError(
                    detail=e, code=e.HTTP_CODE)
            raise ValidationError(f'{e}')
        else:
            obj.status = resp.status
            obj.save(
                update_fields=('status',)
            )


@extend_schema(
    tags=["Платеж"],
)
@extend_schema_view(
    create=extend_schema(
        summary='Оплата заказа',
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
        summary='Просмотр платежей к заказу',
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
    retrieve=extend_schema(
        summary='Просмотр оплаты заказа',
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
                description='id платежа',
                required=True,
                type=int
            ),
        ]
    )
)
class OrderPaymentView(viewsets.ModelViewSet):
    http_method_names = ('post', 'get', 'head', 'options')
    pagination_class = None
    serializer_class = PaymentSerializer
    permission_classes = (IsOwnerOrAdminPayment,)

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        order = get_object_or_404(Order, pk=self.kwargs.get('order'))
        self.check_object_permissions_custom(self.request, obj=order)
        payment = OrderPayment.objects.exclude(
            status='canceled').filter(order=order)
        if not payment.exists():
            payment = OrderPayment.objects.create(order=order)
        else:
            if payment.filter(status='succeeded').exists():
                raise RepeatPaymentException()
            payment = payment[0]
        data = PrePaymentSerializer(payment).data
        try:
            resp = Payment.create(data['data'], data['idempotence_key'])
        except Exception as e:
            code = getattr(type(e), 'HTTP_CODE', False)
            if code and args:
                raise ValidationError(
                    detail=e, code=e.HTTP_CODE)
            raise ValidationError(f'{e}')
        else:
            payment.payment_id = resp.id
            payment.status = resp.status

            payment.save(
                update_fields=('payment_id', 'status'))
            serializer = self.get_serializer(payment)
            data = serializer.data
            data['confirmation_url'] = resp.confirmation.confirmation_url
            headers = self.get_success_headers(serializer.data)
            return Response(
                data, status=status.HTTP_201_CREATED, headers=headers
            )

    def get_queryset(self):
        order = get_object_or_404(Order, pk=self.kwargs.get('order'))
        self.check_object_permissions_custom(self.request, obj=order)
        for obj in order.payments.exclude(
            payment_id__isnull=True,
            status__in=['canceled', 'succeeded']
        ):
            self.update_payment(obj=obj)
        return order.payments.all()

    def update_payment(self, obj):
        try:
            resp = Payment.find_one(payment_id=obj.payment_id)
        except Exception as e:
            logging.error(e)
        else:
            obj.status = resp.status
            obj.save(update_fields=('status',))

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
