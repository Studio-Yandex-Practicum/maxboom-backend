from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

from catalogue.models import Product
from maxboom.settings import DISCOUNT_ANONYM, DISCOUNT_USER, MIN_AMOUNT_PRODUCT

User = get_user_model()


class CommodityRefund(models.Model):
    commodity = models.ForeignKey(
        'Commodity',
        on_delete=models.CASCADE,
        verbose_name='Возвращаемый товар',
        related_name='refunds', help_text='id товара в заказе'
    )
    refund = models.ForeignKey(
        'OrderRefund',
        on_delete=models.CASCADE,
        verbose_name='Возврат',
        related_name='commodities',
        help_text='id возврата заказа'
    )
    quantity = models.PositiveIntegerField(
        verbose_name='Количество', help_text='количество'
    )

    class Meta:
        verbose_name = 'Возвращаемый товар'
        verbose_name_plural = 'Возвращаемые товары'
        constraints = (
            models.UniqueConstraint(
                fields=('commodity', 'refund'),
                name='unique_commodity_refund'
            ),
        )

    def __str__(self):
        return f'{self.commodity.product.name} - {self.quantity}'

    def save(self, *args, **kwargs) -> None:
        self.full_clean()
        return super().save(*args, **kwargs)

    def clean(self) -> None:
        if self.commodity.rest < self.quantity:
            raise ValidationError(
                {'quantity': ('quantity should have at least '
                              f'{self.commodity.rest=}')}
            )
        return super().clean()


class OrderRefund(models.Model):
    order = models.ForeignKey(
        'Order',
        on_delete=models.CASCADE,
        verbose_name='Заказ',
        related_name='refunds',
        help_text='id Заказа'
    )
    created = models.DateTimeField(
        verbose_name='Дата создания',
        auto_now_add=True,
        help_text='дата создания'
    )
    comment = models.TextField(
        verbose_name='Комментарии',
        blank=True,
        null=True,
        help_text='текст комментария'
    )

    class Meta:
        verbose_name = 'Возврат'
        verbose_name_plural = 'Возвраты'

    @property
    def value(self, *args, **kwargs):
        value = 0
        commodities = self.commodities.all()
        if commodities.exists():
            for item in commodities:
                value += item.quantity * item.commodity.price
        type(value)
        return value
    value.fget.short_description = 'Стоимость'

    @property
    def is_refunded(self, *args, **kwargs):
        if getattr(self, 'refunds', False):
            refunds = self.refunds.exclude(status='canceled')
            for refund in refunds:
                if refund.is_refunded:
                    True
        return False
    is_refunded.fget.short_description = 'Возврат средств выполнен'

    def __str__(self) -> str:
        return f'Возврат № {self.id}.'


class Order(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
        null=True,
        blank=True,
        help_text='id создателя заказа'
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name='Авторизованный',
        help_text='авторизованный'
    )
    session_id = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        verbose_name='id сессии',
        help_text='id сессии'

    )
    address = models.CharField(
        max_length=500,
        verbose_name='Адрес',
        help_text='адрес доставки заказа',
        null=True,
        blank=True,
    )
    phone = PhoneNumberField(
        verbose_name='Телефон',
        null=True,
        blank=True,
        help_text='номер телефона'
    )
    email = models.EmailField(
        verbose_name='Почта',
        max_length=255,
        blank=True,
        help_text='электронная почта'
    )
    comment = models.TextField(
        verbose_name='Комментарии',
        blank=True,
        null=True,
        help_text='текст комментария'
    )
    status = models.CharField(
        verbose_name='Статус заказа',
        max_length=20,
        blank=True,
        default='создан',
        help_text='статус заказа'
    )
    created = models.DateTimeField(
        verbose_name='Дата создания', auto_now_add=True,
        help_text='дата создания')

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
        ordering = ('-created',)

    def __str__(self) -> str:
        return f'Заказ № {self.id}.'

    def save(self, *args, **kwargs):
        if not self.email:
            self.email = self.user.email
        super().save(*args, **kwargs)

    @property
    def value(self, *args, **kwargs):
        value = 0
        if getattr(self, 'commodities', False):
            commodities = self.commodities.all()
            if commodities.exists():
                for item in commodities:
                    value += item.quantity * item.price
        return value
    value.fget.short_description = 'Стоимость'

    @property
    def is_paid(self, *args, **kwargs):
        if getattr(self, 'payments', False):
            payments = self.payments.exclude(status='canceled')
            for payment in payments:
                if payment.is_paid:
                    return True
        return False
    is_paid.fget.short_description = 'Заказ оплачен'


class Commodity(models.Model):
    price = models.DecimalField(
        verbose_name='Цена',
        decimal_places=2,
        max_digits=10,
        blank=True,
        editable=False,
        help_text='цена товара'

    )
    quantity = models.PositiveSmallIntegerField(
        verbose_name='Количество',
        validators=(MinValueValidator(MIN_AMOUNT_PRODUCT),),
        help_text='количество'
    )
    product = models.ForeignKey(
        Product, on_delete=models.SET_NULL,
        related_name='commodities',
        verbose_name='Товар в заказе',
        null=True,
        help_text='id товара в каталоге'
    )
    order = models.ForeignKey(
        'Order', on_delete=models.CASCADE,
        related_name='commodities', verbose_name='Заказ',
        help_text='id заказа'
    )

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
        constraints = (
            models.UniqueConstraint(
                fields=('product', 'order'),
                name='unique_commodity_order'
            ),
        )

    def __str__(self) -> str:
        return f'{self.product.name}'

    def save(self, *args, **kwargs):
        if self.price:
            return super().save(*args, **kwargs)
        if self.order.is_active and self.order.user.userprofile.is_vendor:
            discount = DISCOUNT_USER
        else:
            discount = DISCOUNT_ANONYM
        self.price = self.product.price * discount
        self.price = round(self.product.price * discount, 2)
        self.full_clean()
        super().save(*args, **kwargs)

    @property
    def rest(self):
        if not self.refunds.all().exists():
            return self.quantity
        rest = self.quantity
        for obj in self.refunds.all():
            rest -= obj.quantity
        return rest
