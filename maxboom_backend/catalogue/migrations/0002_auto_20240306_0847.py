# Generated by Django 3.2.3 on 2024-03-06 05:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalogue', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='label_hit',
            field=models.BooleanField(default=False, verbose_name='Ярлык Хит'),
        ),
        migrations.AddField(
            model_name='product',
            name='label_popular',
            field=models.BooleanField(default=False, verbose_name='Ярлык Популярный'),
        ),
    ]
