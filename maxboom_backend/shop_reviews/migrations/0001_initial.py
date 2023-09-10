# Generated by Django 3.2.3 on 2023-09-08 18:01

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ShopReviews',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(help_text='Отзыв о магазине', verbose_name='Отзыв')),
                ('pub_date', models.DateTimeField(auto_now_add=True, help_text='Дата создания отзыва', verbose_name='Дата создания отзыва')),
                ('author_name', models.CharField(help_text='Имя автора отзыва', max_length=200, verbose_name='Имя')),
                ('author_email', models.EmailField(blank=True, help_text='Почта автора отзыва', max_length=200, null=True, verbose_name='Почта')),
                ('delivery_speed_score', models.PositiveIntegerField(help_text='Оценка скорости доставки товаров', validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)], verbose_name='Скорость доставки')),
                ('quality_score', models.PositiveIntegerField(help_text='Оценка качества товара в магазине', validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)], verbose_name='Качество товара')),
                ('price_score', models.PositiveIntegerField(help_text='Оценка цен в магазине', validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)], verbose_name='Цена')),
                ('is_published', models.BooleanField(default=False, help_text='Разрешить публикацию отзыва', verbose_name='Публикация')),
            ],
            options={
                'verbose_name': 'Отзыв о магазине',
                'verbose_name_plural': 'Отзывы о магазине',
                'ordering': ('-pub_date',),
            },
        ),
        migrations.CreateModel(
            name='ReplayToReview',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(help_text='Ответ на отзыв', verbose_name='Ответ')),
                ('name', models.CharField(default='Администратор', help_text='Имя автора ответа', max_length=200, verbose_name='Имя')),
                ('pub_date', models.DateTimeField(auto_now_add=True, help_text='Дата создания ответа', verbose_name='Дата')),
                ('review_id', models.OneToOneField(help_text='Отзыв о магазине, на который отвечает администратор', on_delete=django.db.models.deletion.CASCADE, related_name='replay', to='shop_reviews.shopreviews', verbose_name='Отзыв о магазине')),
            ],
            options={
                'verbose_name': 'Ответ на отзыв',
                'verbose_name_plural': 'Ответы на отзывы',
                'ordering': ('-pub_date',),
            },
        ),
    ]
