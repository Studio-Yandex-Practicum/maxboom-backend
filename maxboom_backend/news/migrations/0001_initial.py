# Generated by Django 3.2.3 on 2023-09-25 17:34

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='News',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=250, verbose_name='Заголовок')),
                ('text', models.TextField(verbose_name='Текст')),
                ('image', models.ImageField(blank=True, null=True, upload_to='news/', verbose_name='Изображение')),
                ('pub_date', models.DateField(auto_now_add=True, verbose_name='Дата публикации')),
                ('slug', models.SlugField(unique=True, verbose_name='Слаг')),
                ('meta_title', models.CharField(blank=True, max_length=255, null=True, verbose_name='Мета-название страницы')),
                ('meta_description', models.CharField(blank=True, max_length=255, null=True, verbose_name='Мета-описание страницы')),
            ],
            options={
                'verbose_name': 'Новость',
                'verbose_name_plural': 'Новости',
                'ordering': ['-pub_date'],
            },
        ),
    ]
