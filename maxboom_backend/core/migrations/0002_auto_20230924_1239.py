# Generated by Django 3.2.3 on 2023-09-24 09:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AdditionalLogo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='', verbose_name='Изображение логотипа')),
                ('url', models.URLField(verbose_name='Ссылка на сайт логотипа')),
            ],
            options={
                'verbose_name': 'Дополнительный логотип',
                'verbose_name_plural': 'Дополнительные логотипы',
            },
        ),
        migrations.CreateModel(
            name='Contacts',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('headline', models.CharField(help_text='Введите заголовок страницы', max_length=255, verbose_name='Заголовок страницы')),
                ('meta_title', models.CharField(blank=True, max_length=255, null=True, verbose_name='Мета-название страницы')),
                ('meta_description', models.CharField(blank=True, max_length=255, null=True, verbose_name='Мета-описание страницы')),
            ],
            options={
                'verbose_name': 'Контакты',
                'verbose_name_plural': 'Контакты',
                'ordering': ['id'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Footer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company_info', models.CharField(max_length=255, verbose_name='Информация о компании внизу страницы')),
                ('disclaimer', models.CharField(max_length=255, verbose_name='Авторство внизу страницы')),
                ('support_work_time', models.CharField(max_length=100, verbose_name='Время работы поддержки')),
            ],
            options={
                'verbose_name': 'Подвал страницы',
                'verbose_name_plural': 'Подвал страницы',
                'ordering': ['id'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Header',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'verbose_name': 'Шапка страницы',
                'verbose_name_plural': 'Шапка страницы',
                'ordering': ['id'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='MailContact',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('person_name', models.CharField(help_text='Имя', max_length=255, verbose_name='Имя')),
                ('person_email', models.EmailField(help_text='E-Mail', max_length=254, verbose_name='E-mail')),
                ('message', models.TextField(help_text='Текст сообщения или вопроса', verbose_name='Текст сообщения или вопроса')),
            ],
            options={
                'verbose_name': 'Вопрос магазину',
                'verbose_name_plural': 'Вопросы магазину',
            },
        ),
        migrations.CreateModel(
            name='MailContactForm',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('headline', models.CharField(max_length=100, verbose_name='Заголовок формы')),
                ('ask_name', models.CharField(max_length=100, verbose_name='Поле для имени')),
                ('ask_email', models.CharField(max_length=100, verbose_name='Поле для E-Mail')),
                ('ask_message', models.CharField(max_length=100, verbose_name='Поле для сообщения')),
                ('send_button_text', models.CharField(max_length=100, verbose_name='Текст на кнопке отправки')),
                ('main_page', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='mail_form', to='core.contacts', verbose_name='Связанная страница (Контакты)')),
            ],
            options={
                'verbose_name': 'Форма вопроса к магазину',
                'verbose_name_plural': 'Форма вопроса к магазину',
                'ordering': ['id'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='MainLogo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='', verbose_name='Изображение логотипа')),
                ('url', models.URLField(verbose_name='Ссылка на сайт логотипа')),
                ('footer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='main_logo', to='core.footer')),
                ('header', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='main_logo', to='core.header')),
            ],
            options={
                'verbose_name': 'Основной логотип',
                'verbose_name_plural': 'Основной логотип',
                'ordering': ['id'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Privacy',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('headline', models.CharField(help_text='Введите заголовок страницы', max_length=255, verbose_name='Заголовок страницы')),
                ('text', models.TextField(help_text='Введите текст страницы', verbose_name='Текст страницы')),
                ('meta_title', models.CharField(blank=True, max_length=255, null=True, verbose_name='Мета-название страницы')),
                ('meta_description', models.CharField(blank=True, max_length=255, null=True, verbose_name='Мета-описание страницы')),
            ],
            options={
                'verbose_name': 'Политика безопасности',
                'verbose_name_plural': 'Политика безопасности',
                'ordering': ['id'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Support',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Название блока поддержки')),
                ('phone_number', models.CharField(max_length=30, verbose_name='Телефон поддержки')),
                ('footer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='support', to='core.footer')),
                ('header', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='support', to='core.header')),
            ],
            options={
                'verbose_name': 'Поддержка',
                'verbose_name_plural': 'Поддержка',
                'ordering': ['id'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Terms',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('headline', models.CharField(help_text='Введите заголовок страницы', max_length=255, verbose_name='Заголовок страницы')),
                ('text', models.TextField(help_text='Введите текст страницы', verbose_name='Текст страницы')),
                ('meta_title', models.CharField(blank=True, max_length=255, null=True, verbose_name='Мета-название страницы')),
                ('meta_description', models.CharField(blank=True, max_length=255, null=True, verbose_name='Мета-описание страницы')),
            ],
            options={
                'verbose_name': 'Условия соглашения',
                'verbose_name_plural': 'Условия соглашения',
                'ordering': ['id'],
                'abstract': False,
            },
        ),
        migrations.DeleteModel(
            name='Agreements',
        ),
        migrations.DeleteModel(
            name='ContactUs',
        ),
        migrations.DeleteModel(
            name='Policy',
        ),
        migrations.AlterModelOptions(
            name='about',
            options={'ordering': ['id'], 'verbose_name': 'О нас', 'verbose_name_plural': 'О нас'},
        ),
        migrations.AlterModelOptions(
            name='deliveryinformation',
            options={'ordering': ['id'], 'verbose_name': 'Информация о доставке', 'verbose_name_plural': 'Информация о доставке'},
        ),
        migrations.AlterModelOptions(
            name='mainshop',
            options={'ordering': ['id'], 'verbose_name': 'Основной магазин', 'verbose_name_plural': 'Основной магазин'},
        ),
        migrations.AlterModelOptions(
            name='ourshop',
            options={'verbose_name': 'Наши магазины', 'verbose_name_plural': 'Наши магазины'},
        ),
        migrations.AlterModelOptions(
            name='requisite',
            options={'verbose_name': 'Реквизиты', 'verbose_name_plural': 'Реквизиты'},
        ),
        migrations.AddField(
            model_name='about',
            name='meta_description',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Мета-описание страницы'),
        ),
        migrations.AddField(
            model_name='about',
            name='meta_title',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Мета-название страницы'),
        ),
        migrations.AddField(
            model_name='deliveryinformation',
            name='meta_description',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Мета-описание страницы'),
        ),
        migrations.AddField(
            model_name='deliveryinformation',
            name='meta_title',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Мета-название страницы'),
        ),
        migrations.AlterField(
            model_name='mainshop',
            name='comment',
            field=models.CharField(help_text='Время работы и дополнительная информация', max_length=255, verbose_name='Комментарий о магазине'),
        ),
        migrations.AlterField(
            model_name='mainshop',
            name='email',
            field=models.EmailField(help_text='Введите электронную почту магазина', max_length=254, verbose_name='Почта магазина'),
        ),
        migrations.AlterField(
            model_name='ourshop',
            name='comment',
            field=models.CharField(help_text='Время работы и дополнительная информация', max_length=255, verbose_name='Комментарий о магазине'),
        ),
        migrations.AddField(
            model_name='additionallogo',
            name='footer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='additional_logos', to='core.footer'),
        ),
        migrations.AddField(
            model_name='mainshop',
            name='main_page',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='main_shop', to='core.contacts'),
        ),
        migrations.AddField(
            model_name='ourshop',
            name='main_page',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='our_shops', to='core.contacts'),
        ),
        migrations.AddField(
            model_name='requisite',
            name='main_page',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='requisites', to='core.contacts'),
        ),
    ]
