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

    def __str__(self):
        return self.__class__._meta.verbose_name

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
        verbose_name_plural = "О нас"


class Policy(BaseCoreModel):
    """
    Модель страницы "Политика безопасности".
    """

    class Meta:
        verbose_name = "Политика безопасности"
        verbose_name_plural = "Политика безопасности"


class Agreements(BaseCoreModel):
    """
    Модель страницы "Условия соглашения".
    """

    class Meta:
        verbose_name = "Условия соглашения"
        verbose_name_plural = "Условия соглашения"


class DeliveryInformation(BaseCoreModel):
    """
    Модель страницы "Информация о доставке".
    """

    class Meta:
        verbose_name = "Информация о доставке"
        verbose_name_plural = "Информация о доставке"


class Contacts(BaseCoreModel):
    """
    Модель страницы "Контакты".
    """

    class Meta:
        verbose_name = "Контакты"
        verbose_name_plural = "Контакты"


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
    main_page = models.ForeignKey(
        Contacts,
        related_name='requisites',
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    class Meta:
        verbose_name = "Реквизиты"
        verbose_name_plural = "Реквизиты"


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
        help_text="Время работы и дополнительная информация"
    )
    phone_number = models.CharField(
        max_length=20,
        verbose_name="Номер телефона",
        help_text="Укажите номер телефона магазина"
    )

    class Meta:
        abstract = True

    def __str__(self):
        return self.__class__.__name__


class MainShop(BaseShop):
    """
    Модель для описания основного магазина.
    """

    email = models.EmailField(
        verbose_name="Почта магазина",
        help_text="Введите электронную почту магазина"
    )
    location = models.CharField(
        max_length=510,
        verbose_name="Адрес магазина",
        help_text="Укажите адрес магазина"
    )
    main_page = models.ForeignKey(
        Contacts,
        related_name='main_shop',
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    class Meta:
        verbose_name = "Основной магазин"
        verbose_name_plural = "Основной магазин"

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
    main_page = models.ForeignKey(
        Contacts,
        related_name='our_shops',
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    class Meta:
        verbose_name = "Наши магазины"
        verbose_name_plural = "Наши магазины"
