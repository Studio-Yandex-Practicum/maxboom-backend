# Generated by Django 3.2.3 on 2024-06-17 12:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0002_orderreturn'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderreturn',
            name='order_date',
            field=models.DateField(blank=True, help_text='дата заказа', verbose_name='дата заказа'),
        ),
    ]