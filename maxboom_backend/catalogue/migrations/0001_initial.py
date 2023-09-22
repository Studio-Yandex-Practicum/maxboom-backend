# Generated by Django 3.2.3 on 2023-09-22 19:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Brand',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=500, unique=True, verbose_name='Наименование')),
                ('slug', models.SlugField(blank=True, editable=False, max_length=200, null=True, unique=True, verbose_name='Уникальный слаг')),
                ('is_prohibited', models.BooleanField(default=False, help_text='Бренды, которые не публикуются на сайте', verbose_name='Запрещенный для публикации производитель')),
            ],
            options={
                'verbose_name': 'Производитель',
                'verbose_name_plural': 'Производители',
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=500, unique=True, verbose_name='Название')),
                ('slug', models.SlugField(blank=True, editable=False, max_length=200, null=True, unique=True, verbose_name='Уникальный слаг')),
                ('meta_title', models.CharField(blank=True, max_length=255, null=True, verbose_name='Мета-название категории')),
                ('meta_description', models.CharField(blank=True, max_length=255, null=True, verbose_name='Мета-описание категории')),
                ('is_visible_on_main', models.BooleanField(default=False, help_text='Категория, которая отображаются на главной странице', verbose_name='Категория видимая на главной странице')),
                ('is_prohibited', models.BooleanField(default=False, help_text='Категория, которая не публикуются на сайте', verbose_name='Запрещенная для публикации категория')),
                ('root', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='branches', to='catalogue.category', verbose_name='Родительская категория')),
            ],
            options={
                'verbose_name': 'Категория',
                'verbose_name_plural': 'Категории',
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=500, verbose_name='Название')),
                ('slug', models.SlugField(blank=True, editable=False, max_length=200, null=True, unique=True, verbose_name='Уникальный слаг')),
                ('description', models.TextField(verbose_name='Описание')),
                ('price', models.DecimalField(decimal_places=3, max_digits=10, verbose_name='Цена')),
                ('code', models.IntegerField(unique=True, verbose_name='Код товара')),
                ('wb_urls', models.URLField(verbose_name='Ссылка на WB')),
                ('quantity', models.FloatField(default=999999, verbose_name='Количество')),
                ('is_deleted', models.BooleanField(default=False, verbose_name='Удален ли товар')),
                ('meta_title', models.CharField(blank=True, max_length=255, null=True, verbose_name='Мета-название товара')),
                ('meta_description', models.CharField(blank=True, max_length=255, null=True, verbose_name='Мета-описание товара')),
                ('brand', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='products', to='catalogue.brand', verbose_name='Бренд')),
                ('category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='products', to='catalogue.category', verbose_name='Категория')),
            ],
            options={
                'verbose_name': 'Товар',
                'verbose_name_plural': 'Товары',
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='ProductImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='products-images', verbose_name='Изображение')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='catalogue.product', verbose_name='Продукт')),
            ],
            options={
                'verbose_name': 'Изображение товара',
                'verbose_name_plural': 'Изображения товаров',
            },
        ),
    ]
