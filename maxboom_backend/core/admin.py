from django.contrib import admin

from .models import (
    About, Terms, DeliveryInformation, Privacy, Contacts, Requisite,
    MainShop, OurShop, MailContact, MainLogo, AdditionalLogo,
    Support, Header, Footer, MailContactForm
)


class BaseAdmin(admin.ModelAdmin):
    list_display = ['element_name']

    # Настройка для вывода названия модели вместо
    # id объекта в админке для явного доступа.
    def element_name(self, obj):
        return obj._meta.verbose_name


class MainShopInline(admin.StackedInline):
    """
    Инлайн для отображения информации об основном
    магазине на странице "Контакты".
    """

    model = MainShop
    extra = 1
    max_num = 1


class OurShopInline(admin.StackedInline):
    """
    Инлайн для отображения информации об остальных
    магазинах на странице "Контакты".
    """

    model = OurShop
    extra = 1


class MailContactFormInline(admin.StackedInline):
    """
    Инлайн для отображения параметров формы
    для вопросов на странице "Контакты".
    """

    model = MailContactForm
    max_num = 1


class RequisiteInline(admin.StackedInline):
    """
    Инлайн для отображения реквизитов на странице
    "Контакты".
    """

    model = Requisite
    extra = 1


class MainLogoInline(admin.StackedInline):
    """
    Инлайн для отображения информации об основном
    логотипе магазина.
    """

    model = MainLogo
    max_num = 1


class AdditionalLogoInline(admin.StackedInline):
    """
    Инлайн для отображения информации о дополнительных
    логотипах в магазине.
    """

    model = AdditionalLogo
    extra = 1


class SupportInline(admin.StackedInline):
    """
    Инлайн для отображения информации о поддержке
    в шапке и подвале.
    """

    model = Support
    max_num = 1


@admin.register(Contacts)
class ContactUsAdmin(BaseAdmin):
    inlines = [
        MainShopInline,
        MailContactFormInline,
        RequisiteInline,
        OurShopInline
    ]


@admin.register(About)
class AboutAdmin(BaseAdmin):
    ...


@admin.register(DeliveryInformation)
class DeliveryInformationAdmin(BaseAdmin):
    ...


@admin.register(Privacy)
class PrivacyAdmin(BaseAdmin):
    ...


@admin.register(Terms)
class TermsAdmin(BaseAdmin):
    ...


@admin.register(Requisite)
class RequisiteAdmin(admin.ModelAdmin):
    list_display = ['requisite_name']


@admin.register(MainShop)
class MainShopAdmin(BaseAdmin):
    ...


@admin.register(OurShop)
class OurShopAdmin(BaseAdmin):
    list_display = ['name']


@admin.register(MailContactForm)
class MailContactFormAdmin(BaseAdmin):
    ...


@admin.register(MailContact)
class MailContactAdmin(admin.ModelAdmin):
    list_display = ['get_id', 'person_name', 'person_email', 'message']

    def get_id(self, obj):
        return f"ID обращения: {obj.pk}"


@admin.register(MainLogo)
class MainLogoAdmin(BaseAdmin):
    ...


@admin.register(AdditionalLogo)
class AdditionalLogoAdmin(BaseAdmin):
    list_display = ['url']


@admin.register(Support)
class SupportAdmin(BaseAdmin):
    ...


@admin.register(Header)
class HeaderAdmin(BaseAdmin):
    inlines = [MainLogoInline, SupportInline]


@admin.register(Footer)
class FooterAdmin(BaseAdmin):
    inlines = [MainLogoInline, SupportInline, AdditionalLogoInline]
