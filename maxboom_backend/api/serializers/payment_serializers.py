from rest_framework import serializers

from maxboom.settings import VAT_CODE
from order.models import Order
from payment.models import OrderPayment, Repayment


class DataRepaymentSerializer(serializers.BaseSerializer):
    def to_representation(self, obj):
        items = []
        for item in obj.order_refund.commodities.all():
            items.append({
                'description': item.commodity.product.name,
                'quantity': str(item.quantity),
                'amount': {
                    'value': str(item.commodity.price),
                    'currency': 'RUB'
                },
                'vat_code': int(VAT_CODE),
                'payment_mode': 'full_payment',
                'payment_subject': 'commodity'
            })
        return {
            'payment_id': str(obj.payment.payment_id),
            'amount': {
                'value': str(obj.value),
                'currency': 'RUB'
            },
            'description': str(obj.order_refund),
            'metadata': {
                'orderNumber': obj.order_refund.id
                # 'orderNumber': str(obj.idempotence_key)
            },
            'receipt': {
                'customer': {
                    'email': obj.order_refund.order.email
                },
                'items': items
            }
        }


class DataSerializer(serializers.BaseSerializer):
    def to_representation(self, obj):
        items = []
        for item in obj.order.commodities.all():
            items.append({
                'description': item.product.name,
                'quantity': str(item.quantity),
                'amount': {
                    'value': str(item.price),
                    'currency': 'RUB'
                },
                'vat_code': int(VAT_CODE),
                'payment_mode': 'full_payment',
                'payment_subject': 'commodity'
            })
        return {
            'amount': {
                'value': str(obj.order.value),
                'currency': 'RUB'
            },
            'confirmation': {
                'type': 'redirect',
                'return_url': 'https://www.maxboom.ru/'
            },
            'capture': True,
            'description': str(obj.order),
            'metadata': {
                'orderNumber': obj.order.id
                # 'orderNumber': str(obj.idempotence_key)
            },
            'receipt': {
                'customer': {
                    'email': obj.order.email
                },
                'items': items
            }
        }


class PrePaymentSerializer(serializers.ModelSerializer):
    data = serializers.SerializerMethodField()
    order = serializers.PrimaryKeyRelatedField(queryset=Order.objects.all())

    class Meta:
        model = OrderPayment
        fields = (
            'id', 'idempotence_key', 'order',
            'payment_id', 'status', 'created',
            'data',
            'is_paid'
        )

    def get_data(self, obj):
        return DataSerializer(instance=obj, read_only=True).data


class PreRepaymentSerializer(serializers.ModelSerializer):
    data = serializers.SerializerMethodField()
    order_refund = serializers.PrimaryKeyRelatedField(
        read_only=True,
    )

    class Meta:
        model = Repayment
        fields = (
            'idempotence_key', 'order_refund', 'data'
        )

    def get_data(self, obj):
        return DataRepaymentSerializer(instance=obj, read_only=True).data


class PaymentSerializer(serializers.ModelSerializer):
    order = serializers.PrimaryKeyRelatedField(queryset=Order.objects.all())

    class Meta:
        model = OrderPayment
        fields = (
            'id', 'idempotence_key', 'order',
            'payment_id', 'status', 'created',
            'is_paid', 'value'
        )


class RepaymentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Repayment
        fields = (
            'id', 'idempotence_key', 'refund_id',
            'payment', 'status', 'order_refund', 'created',
            'value', 'is_repaid'
        )
