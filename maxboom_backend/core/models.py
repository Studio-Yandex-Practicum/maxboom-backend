from django.db import models

from .utils import clean


class BaseCoreModel(models.Model):
    """
    Основная базовая модель, от которой наследуются все
    последующие. Настроены вывод и репрезентация для
    облегчения работы в админке.
    """

    class Meta:
        abstract = True

    # str() будет отображать название объекта в админке в виде
    # названия модели для облегчения работы с ним.
    def __str__(self):
        return self._meta.verbose_name

    # repr() нужен для облегчения более внутренней работы над
    # объектами внутри админки.
    def __repr__(self):
        return self.__class__.__name__


class BaseSingleObjectModel(models.Model):
    """
    Отдельный класс для наследования, который ограничивает
    модель одним возможным созданным объектом.
    """

    # Ordering в мете для гарантии, что в первым
    # элементом в кверисете будет самый старый.
    # От этой меты наследуются модели с единственным объектом.
    class Meta:
        abstract = True
        ordering = ['id']

    def clean(self):
        """
        Вызывает внешнюю функцию clean(), чтобы
        предотвратить создание более одного объекта модели.
        """

        clean(self)


class BaseInfoModel(BaseCoreModel, BaseSingleObjectModel):
    """
    Базовая модель для информационных страниц. Наследуется
    ещё и от BaseSingleObjectModel, чтобы предотвратить создание
    нескольких объектов.
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
    meta_title = models.CharField(
        max_length=255,
        verbose_name="Мета-название страницы",
        null=True,
        blank=True
    )
    meta_description = models.CharField(
        max_length=255,
        verbose_name="Мета-описание страницы",
        null=True,
        blank=True
    )

    class Meta:
        abstract = True


class About(BaseInfoModel):
    """
    Модель страницы "О нас".
    """

    class Meta(BaseSingleObjectModel.Meta):
        verbose_name = "О нас"
        verbose_name_plural = "О нас"


class DeliveryInformation(BaseInfoModel):
    """
    Модель страницы "Информация о доставке".
    """

    class Meta(BaseSingleObjectModel.Meta):
        verbose_name = "Информация о доставке"
        verbose_name_plural = "Информация о доставке"


class Privacy(BaseInfoModel):
    """
    Модель страницы "Политика безопасности".
    """

    class Meta(BaseSingleObjectModel.Meta):
        verbose_name = "Политика безопасности"
        verbose_name_plural = "Политика безопасности"


class Terms(BaseInfoModel):
    """
    Модель страницы "Условия соглашения".
    """

    class Meta(BaseSingleObjectModel.Meta):
        verbose_name = "Условия соглашения"
        verbose_name_plural = "Условия соглашения"


class Contacts(BaseInfoModel):
    """
    Модель страницы "Контакты". Последующие модели
    до статичных элементов сайта связаны с ней.
    """

    text = None

    class Meta(BaseSingleObjectModel.Meta):
        verbose_name = "Контакты"
        verbose_name_plural = "Контакты"


class BaseShop(BaseCoreModel):
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


class MainShop(BaseShop, BaseSingleObjectModel):
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
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    class Meta(BaseSingleObjectModel.Meta):
        verbose_name = "Основной магазин"
        verbose_name_plural = "Основной магазин"


class OurShop(BaseShop):
    """
    Модель элементов раздела "Наши магазины".
    """

    photo = models.ImageField(
        verbose_name="Фотография",
        upload_to='core/news/'
    )
    is_main_shop = models.BooleanField(
        verbose_name="Основной магазин",
        help_text="Укажите статус магазина как основного"
    )
    main_page = models.ForeignKey(
        Contacts,
        related_name='our_shops',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    class Meta:
        verbose_name = "Наши магазины"
        verbose_name_plural = "Наши магазины"


class Requisite(BaseCoreModel):
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
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    class Meta:
        verbose_name = "Реквизиты"
        verbose_name_plural = "Реквизиты"


class MailContactForm(BaseCoreModel, BaseSingleObjectModel):
    """
    Модель формы обращения с сообщением или вопросом к магазину.
    """

    headline = models.CharField(
        max_length=100,
        verbose_name="Заголовок формы"
    )
    ask_name = models.CharField(
        max_length=100,
        verbose_name="Поле для имени"
    )
    ask_email = models.CharField(
        max_length=100,
        verbose_name="Поле для E-Mail"
    )
    ask_message = models.CharField(
        max_length=100,
        verbose_name="Поле для сообщения"
    )
    send_button_text = models.CharField(
        max_length=100,
        verbose_name="Текст на кнопке отправки"
    )
    main_page = models.ForeignKey(
        Contacts,
        on_delete=models.SET_NULL,
        related_name='mail_form',
        null=True,
        blank=True,
        verbose_name="Связанная страница (Контакты)"
    )

    class Meta(BaseSingleObjectModel.Meta):
        verbose_name = "Форма вопроса к магазину"
        verbose_name_plural = "Форма вопроса к магазину"


class MailContact(BaseCoreModel):
    """
    Модель обращения с сообщением или вопросом к магазину.
    """

    person_name = models.CharField(
        max_length=255,
        verbose_name="Имя",
        help_text="Имя"
    )
    person_email = models.EmailField(
        verbose_name="E-mail",
        help_text="E-Mail"
    )
    message = models.TextField(
        verbose_name="Текст сообщения или вопроса",
        help_text="Текст сообщения или вопроса"
    )

    class Meta:
        verbose_name = "Вопрос магазину"
        verbose_name_plural = "Вопросы магазину"


class Header(BaseCoreModel, BaseSingleObjectModel):
    """
    Модель с информацией в шапке страницы.
    Реализована для простого доступа к изменению
    данных о связанной информации в админке.
    """

    class Meta(BaseSingleObjectModel.Meta):
        verbose_name = "Шапка страницы"
        verbose_name_plural = "Шапка страницы"


class Footer(BaseCoreModel, BaseSingleObjectModel):
    """
    Модель с информацией в подвале страницы.
    """

    company_info = models.CharField(
        max_length=255,
        verbose_name="Информация о компании внизу страницы"
    )
    disclaimer = models.CharField(
        max_length=255,
        verbose_name="Авторство внизу страницы"
    )
    support_work_time = models.CharField(
        max_length=100,
        verbose_name="Время работы поддержки"
    )

    class Meta(BaseSingleObjectModel.Meta):
        verbose_name = "Подвал страницы"
        verbose_name_plural = "Подвал страницы"


class BaseLogo(BaseCoreModel):
    """
    Базовая модель логотипа.
    """

    image = models.ImageField(
        verbose_name="Изображение логотипа",
        upload_to='core/logos/'
    )
    url = models.URLField(
        verbose_name="Ссылка на сайт логотипа"
    )

    class Meta:
        abstract = True


class MainLogo(BaseLogo, BaseSingleObjectModel):
    """
    Модель основного логотипа магазина.
    """

    header = models.ForeignKey(
        Header,
        related_name='main_logo',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    footer = models.ForeignKey(
        Footer,
        related_name='main_logo',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    class Meta(BaseSingleObjectModel.Meta):
        verbose_name = "Основной логотип"
        verbose_name_plural = "Основной логотип"


class AdditionalLogo(BaseLogo):
    """
    Модель дополнительных логотипов.
    """

    footer = models.ForeignKey(
        Footer,
        related_name='additional_logos',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    class Meta:
        verbose_name = "Дополнительный логотип"
        verbose_name_plural = "Дополнительные логотипы"


class Support(BaseCoreModel, BaseSingleObjectModel):
    """
    Модель с информацией о поддержке.
    """

    name = models.CharField(
        max_length=255,
        verbose_name="Название блока поддержки"
    )
    phone_number = models.CharField(
        max_length=30,
        verbose_name="Телефон поддержки"
    )
    header = models.ForeignKey(
        Header,
        related_name='support',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    footer = models.ForeignKey(
        Footer,
        related_name='support',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    class Meta(BaseSingleObjectModel.Meta):
        verbose_name = "Поддержка"
        verbose_name_plural = "Поддержка"
