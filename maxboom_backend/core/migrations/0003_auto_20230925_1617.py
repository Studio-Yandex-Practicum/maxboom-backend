# Generated by Django 3.2.3 on 2023-09-25 13:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_auto_20230924_1239'),
    ]

    operations = [
        migrations.AlterField(
            model_name='additionallogo',
            name='image',
            field=models.ImageField(upload_to='core/logos/', verbose_name='Изображение логотипа'),
        ),
        migrations.AlterField(
            model_name='mainlogo',
            name='image',
            field=models.ImageField(upload_to='core/logos/', verbose_name='Изображение логотипа'),
        ),
        migrations.AlterField(
            model_name='ourshop',
            name='photo',
            field=models.ImageField(upload_to='core/news/', verbose_name='Фотография'),
        ),
    ]
