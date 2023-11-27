# Generated by Django 3.2.3 on 2023-11-22 18:37

import uuid

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('order', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrderPayment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('idempotence_key', models.UUIDField(default=uuid.uuid4, editable=False, help_text='ключ идемпотентности', verbose_name='Ключ идемпотентности')),
                ('payment_id', models.CharField(blank=True, help_text='id патежа от yookassa', max_length=40, null=True, unique=True, verbose_name='id_платежа от yookassa')),
                ('status', models.CharField(blank=True, default='created', help_text='статус платежа', max_length=20, verbose_name='Статус платежа')),
                ('created', models.DateTimeField(auto_now_add=True, help_text='дата создания', verbose_name='Дата создания')),
                ('value', models.DecimalField(blank=True, decimal_places=2, editable=False, help_text='общая сумма', max_digits=10, verbose_name='Сумма')),
                ('order', models.ForeignKey(help_text='id заказа', on_delete=django.db.models.deletion.CASCADE, related_name='payments', to='order.order', verbose_name='Заказ')),
            ],
            options={
                'verbose_name': 'Платеж',
                'verbose_name_plural': 'Платежи',
            },
        ),
        migrations.CreateModel(
            name='Repayment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('idempotence_key', models.UUIDField(default=uuid.uuid4, editable=False, help_text='ключ идемпотентности', verbose_name='Ключ идемпотентности')),
                ('refund_id', models.CharField(blank=True, max_length=40, null=True, unique=True, verbose_name='id_возврата от yookassa')),
                ('status', models.CharField(blank=True, default='created', help_text='статус возврата', max_length=20, verbose_name='Статус возврата')),
                ('created', models.DateTimeField(auto_now_add=True, help_text='дата создания', verbose_name='Дата создания')),
                ('value', models.DecimalField(blank=True, decimal_places=2, editable=False, help_text='общая сумма', max_digits=10, verbose_name='Сумма')),
                ('order_refund', models.ForeignKey(help_text='id возврата заказа', on_delete=django.db.models.deletion.CASCADE, related_name='repayments', to='order.orderrefund', verbose_name='Возвращаемый заказ')),
                ('payment', models.ForeignKey(help_text='id_возврата от yookassa', on_delete=django.db.models.deletion.CASCADE, related_name='repayments', to='payment.orderpayment', verbose_name='Платеж')),
            ],
            options={
                'verbose_name': 'Возвращаемый платеж',
                'verbose_name_plural': 'Возвращаемые платежи',
            },
        ),
    ]
