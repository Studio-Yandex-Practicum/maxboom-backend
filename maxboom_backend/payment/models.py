import logging
import uuid

from django.contrib.auth import get_user_model
from django.db import models
from yookassa import Payment as RequestPayment
from yookassa import Refund as RequestRefund

from order.models import Order, OrderRefund

User = get_user_model()


class OrderPayment(models.Model):
    idempotence_key = models.UUIDField(
        verbose_name='Ключ идемпотентности',
        max_length=40,
        default=uuid.uuid4,
        editable=False,
        help_text='ключ идемпотентности'
    )
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        verbose_name='Заказ',
        related_name='payments',
        help_text='id заказа'
    )
    payment_id = models.CharField(
        'id_платежа от yookassa',
        max_length=40,
        unique=True,
        blank=True,
        null=True,
        help_text='id патежа от yookassa'
    )
    status = models.CharField(
        verbose_name='Статус платежа',
        max_length=20,
        blank=True,
        default='created',
        help_text='статус платежа'
    )
    created = models.DateTimeField(
        verbose_name='Дата создания',
        auto_now_add=True,
        help_text='дата создания'
    )
    value = models.DecimalField(
        verbose_name='Сумма',
        decimal_places=2,
        max_digits=10,
        blank=True,
        editable=False,
        help_text='общая сумма'
    )

    class Meta:
        verbose_name = 'Платеж'
        verbose_name_plural = 'Платежи'

    def __str__(self) -> str:
        return f'Платеж № {self.id}'

    def save(self, *args, **kwargs):
        if self.value:
            return super().save(*args, **kwargs)
        self.value = self.order.value
        super().save(*args, **kwargs)

    @property
    def is_paid(self):
        if not self.payment_id:
            return False
        if self.status == 'succeeded':
            return True
        if (
           self.payment_id is not None
           and self.status != 'canceled'
           ):
            try:
                resp = RequestPayment.find_one(self.payment_id)
            except Exception as e:
                logging.error(e)
            else:
                if self.status != resp.status:
                    self.status = resp.status
                    self.save()
                    print(self.order)
        return self.status == 'succeeded'
    is_paid.fget.short_description = 'Платеж оплачен'


class Repayment(models.Model):
    idempotence_key = models.UUIDField(
        verbose_name='Ключ идемпотентности',
        max_length=40,
        default=uuid.uuid4,
        editable=False,
        help_text='ключ идемпотентности'
    )
    refund_id = models.CharField(
        'id_возврата от yookassa',
        max_length=40,
        unique=True,
        blank=True,
        null=True,
        help_text=''
    )
    payment = models.ForeignKey(
        OrderPayment,
        on_delete=models.CASCADE,
        verbose_name='Платеж',
        related_name='repayments',
        help_text='id_возврата от yookassa'
    )
    status = models.CharField(
        verbose_name='Статус возврата',
        max_length=20,
        blank=True,
        default='created',
        help_text='статус возврата'
    )
    created = models.DateTimeField(
        verbose_name='Дата создания',
        auto_now_add=True,
        help_text='дата создания'
    )
    order_refund = models.ForeignKey(
        OrderRefund,
        on_delete=models.CASCADE,
        verbose_name='Возвращаемый заказ',
        related_name='repayments',
        help_text='id возврата заказа'
    )
    value = models.DecimalField(
        verbose_name='Сумма',
        decimal_places=2,
        max_digits=10,
        blank=True,
        editable=False,
        help_text='общая сумма'
    )

    class Meta:
        verbose_name = 'Возвращаемый платеж'
        verbose_name_plural = 'Возвращаемые платежи'

    def __str__(self) -> str:
        return f'Возврат № {self.id}'

    def save(self, *args, **kwargs):
        if self.value:
            return super().save(*args, **kwargs)
        self.value = self.order_refund.value
        super().save(*args, **kwargs)

    @property
    def is_repaid(self):
        if self.status == 'succeeded':
            return True
        if (
            self.refund_id is not None
            and self.status != 'canceled'
        ):
            try:
                resp = RequestRefund.find_one(self.payment_id)
            except Exception as e:
                logging.error(e)
            else:
                if self.status != resp.status:
                    self.status = resp.status
                    self.save()
        return self.status == 'succeeded'
    is_repaid.fget.short_description = 'Выполнен возврат средств'


# # @receiver(post_save, sender=OrderPayment)
# @receiver(request_finished,)
# def get_status_order_payment(sender, instance, **kwargs):
#     key = kwargs.get('update_fields')
#     if key is None:
#         return
#     update_payment_id = bool('payment_id' in key)
#     if (
#         update_payment_id and
#         not instance.is_paid and instance.payment_id is not None
#         and instance.status != 'canceled'
#     ):
#         status = 'pending'
#         i = 0
#         while status == 'pending' and i < 3:
#             try:
#                 resp = RequestPayment.find_one(instance.payment_id)
#             except Exception as e:
#                 logging.error(e)
#                 break
#             else:
#                 status = resp.status
#             sleep(10)
#             i += 1
#         instance.status = status
#         instance.save()


# @receiver(post_save, sender=Repayment)
# def get_status_repayment(sender, instance, **kwargs):
#     key = kwargs.get('update_fields')
#     if key is None:
#         return
#     update_refund_id = bool('refund_id' in key)
#     if (
#         update_refund_id and
#         not instance.is_refunded and instance.refund_id is not None
#         and instance.status != 'canceled'
#     ):
#         status = 'pending'
#         i = 0
#         while status == 'pending' and i < 3:
#             try:
#                 resp = RequestRefund.find_one(instance.refund_id)
#             except Exception as e:
#                 logging.error(e)
#                 break
#             else:
#                 status = resp.status
#             sleep(1800)
#             i += 1
#         instance.status = status
#         instance.save()
