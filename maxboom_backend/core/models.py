from django.db import models

from .utils import clean


class BaseCoreModel(models.Model):
    """
    Базовая модель для информационных страниц.
    """

    headline = models.CharField(
        max_length=255,
        verbose_name="Заголовок страницы",
        help_text="Введите заголовок страницы"
    )
    text = models.TextField(
        verbose_name="Текст страницы",
        help_text="Введите текст страницы"
    )

    class Meta:
        abstract = True

    def clean(self):
        """
        Вызывает внешнюю функцию clean(), чтобы
        предотвратить создание более одного объекта модели.
        """

        clean(self)


class About(BaseCoreModel):
    """
    Модель страницы "О нас".
    """

    class Meta:
        verbose_name = "О нас"


class Policy(BaseCoreModel):
    """
    Модель страницы "Политика безопасности".
    """

    class Meta:
        verbose_name = "Политика безопасности"


class Agreements(BaseCoreModel):
    """
    Модель страницы "Условия соглашения".
    """

    class Meta:
        verbose_name = "Условия соглашения"


class DeliveryInformation(BaseCoreModel):
    """
    Модель страницы "Информация о доставке".
    """

    class Meta:
        verbose_name = "Информация о доставке"


class ContactUs(BaseCoreModel):
    """
    Модель страницы "Контакты".
    """

    class Meta:
        verbose_name = "Контакты"


class Requisite(models.Model):
    """
    Модель элемента раздела "Наши реквизиты".
    """

    requisite_name = models.CharField(
        max_length=100,
        verbose_name="Название реквизита",
        help_text="Укажите название реквизита"
    )
    requisite_description = models.CharField(
        max_length=255,
        verbose_name="Описание реквизита",
        help_text="Укажите описание реквизита"
    )

    class Meta:
        verbose_name = "Реквизиты"


class BaseShop(models.Model):
    """
    Базовая модель описания магазина
    в разделе "Контакты".
    """

    name = models.CharField(
        max_length=255,
        verbose_name="Название магазина",
        help_text="Укажите название магазина"
    )
    comment = models.CharField(
        max_length=255,
        verbose_name="Комментарий о магазине",
        help_text=""
    )
    phone_number = models.CharField(
        max_length=20,
        verbose_name="Номер телефона",
        help_text="Укажите номер телефона магазина"
    )

    class Meta:
        abstract = True


class MainShop(BaseShop):
    """
    Модель для описания основного магазина.
    """

    email = models.EmailField()
    location = models.CharField(
        max_length=510,
        verbose_name="Адрес магазина",
        help_text="Укажите адрес магазина"
    )

    class Meta:
        verbose_name = "Основной магазин"

    def clean(self):
        """
        Вызывает внешнюю функцию clean(), чтобы
        предотвратить создание более одного объекта модели.
        """

        clean(self)


class OurShop(BaseShop):
    """
    Модель элементов раздела "Наши магазины".
    """

    photo = models.ImageField(
        verbose_name="Фотография",
    )
    is_main_shop = models.BooleanField(
        verbose_name="Основной магазин",
        help_text="Укажите статус магазина как основного"
    )

    class Meta:
        verbose_name = "Наши магазины"
