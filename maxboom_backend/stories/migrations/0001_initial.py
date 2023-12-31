# Generated by Django 3.2.3 on 2023-09-24 17:55

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Picture',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Имя картинки')),
                ('image', models.ImageField(upload_to='story_pictures/')),
                ('pub_date', models.DateField(auto_now_add=True, verbose_name='Дата добавления')),
            ],
            options={
                'verbose_name': 'Картинка к истории',
                'verbose_name_plural': 'Картинки к историям',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Story',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Заголовок')),
                ('link', models.URLField(blank=True, null=True)),
                ('pub_date', models.DateField(auto_now_add=True, verbose_name='Дата добавления')),
                ('show', models.BooleanField(default=False, verbose_name='Показать')),
                ('pictures', models.ManyToManyField(related_name='stories', to='stories.Picture', verbose_name='Картинки к истории')),
            ],
            options={
                'verbose_name': 'История',
                'verbose_name_plural': 'Истории',
                'ordering': ['id'],
            },
        ),
    ]
