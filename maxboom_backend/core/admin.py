from django.contrib import admin

from .models import About, Agreements, DeliveryInformation, Policy, Contacts, Requisite, MainShop, OurShop


class RequisiteInline(admin.StackedInline):
    """
    Инлайн для отображения реквизитов на странице
    "Контакты".
    """

    model = Requisite
    extra = 1


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


@admin.register(Contacts)
class ContactUsAdmin(admin.ModelAdmin):
    inlines = [MainShopInline, RequisiteInline, OurShopInline]
    fields = ('headline',)
    list_display = ('headline',)


@admin.register(About)
class AboutAdmin(admin.ModelAdmin):
    list_display = ('headline',)


@admin.register(Agreements)
class AgreementsAdmin(admin.ModelAdmin):
    list_display = ('headline',)


@admin.register(DeliveryInformation)
class DeliveryInformationAdmin(admin.ModelAdmin):
    list_display = ('headline',)


@admin.register(Policy)
class PolicyAdmin(admin.ModelAdmin):
    list_display = ('headline',)


@admin.register(Requisite)
class RequisiteAdmin(admin.ModelAdmin):
    list_display = ('requisite_name', )


@admin.register(MainShop)
class MainShopAdmin(admin.ModelAdmin):
    list_display = ('name', )


@admin.register(OurShop)
class OurShopAdmin(admin.ModelAdmin):
    list_display = ('name', )
