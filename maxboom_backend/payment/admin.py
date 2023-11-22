from django.contrib import admin

from .models import OrderPayment, Repayment


@admin.register(OrderPayment)
class OrderPaymentAdmin(admin.ModelAdmin):
    """Админка заказов"""
    model = OrderPayment
    list_display = (
        'id', 'idempotence_key', 'order', 'payment_id', 'status', 'created',
        'value', 'is_paid'
    )
    list_filter = ('status', 'order')
    empty_value_display = '-пусто-'
    readonly_fields = ('is_paid', 'value')


@admin.register(Repayment)
class RepaymentAdmin(admin.ModelAdmin):
    """Админка возвратов платежей"""
    model = Repayment
    list_display = (
        'id', 'idempotence_key', 'order_refund', 'payment', 'refund_id',
        'status', 'created', 'value', 'is_repaid'
    )
    list_filter = ('status', 'payment', 'order_refund')
    empty_value_display = '-пусто-'
    readonly_fields = ('is_repaid', 'value')
