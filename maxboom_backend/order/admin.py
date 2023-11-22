from django.contrib import admin

from payment.models import OrderPayment, Repayment

from .models import Commodity, CommodityRefund, Order, OrderRefund


class CommodityInline(admin.TabularInline):
    """Включение товаров в админку заказов"""
    model = Commodity
    verbose_name = "Товар"
    verbose_name_plural = "Товары"
    fields = ('product', 'quantity')
    readonly_fields = ('price', 'rest')
    extra = 0


class CommodityRefundInline(admin.TabularInline):
    """Включение товаров в админку заказов"""
    model = CommodityRefund
    verbose_name = "Возвращаемый товар"
    verbose_name_plural = "Возвращаемые товары"
    fields = ('commodity', 'quantity')
    extra = 0


class OrderRefundInline(admin.TabularInline):
    """Включение возвратов в админку заказов"""
    model = OrderRefund
    verbose_name = "Возврат"
    verbose_name_plural = "Возвраты"
    fields = ('order', 'id')
    extra = 0


class OrderPaymentInline(admin.TabularInline):
    """Включение платежей в админку заказов"""
    model = OrderPayment
    verbose_name = "Платеж"
    verbose_name_plural = "Платежи"
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    """Админка заказов"""
    list_display = (
        'id', 'user', 'session_id', 'email', 'status', 'value', 'is_paid'
    )
    list_filter = ('status', 'user')
    list_editable = ('status',)
    empty_value_display = '-пусто-'
    inlines = (
        CommodityInline, OrderRefundInline, OrderPaymentInline
    )
    list_per_page = 10
    readonly_fields = ('value', 'is_paid',)


class OrderRepaymentInline(admin.TabularInline):
    """Включение возвратов платежей в админку заказов"""
    model = Repayment
    verbose_name = "Возврат платежа"
    verbose_name_plural = "Возвраты платежей"
    extra = 0


@admin.register(OrderRefund)
class OrderRefundAdmin(admin.ModelAdmin):
    """Админка возврата заказов"""
    list_display = (
        'id', 'order', 'value', 'is_refunded'
    )
    list_filter = ('order',)
    empty_value_display = '-пусто-'
    inlines = (
        CommodityRefundInline, OrderRepaymentInline
    )
    list_per_page = 10
    readonly_fields = ('value', 'is_refunded')


@admin.register(Commodity)
class CommodityAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'order', 'product', 'price', 'quantity'
    )
    list_filter = ('order__id',)
    list_editable = ('quantity',)
    empty_value_display = '-пусто-'
    list_per_page = 10


@admin.register(CommodityRefund)
class CommodityRefundAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'commodity', 'refund', 'quantity'
    )
    list_filter = ('refund__id',)
    list_editable = ('quantity',)
    empty_value_display = '-пусто-'
    list_per_page = 10
