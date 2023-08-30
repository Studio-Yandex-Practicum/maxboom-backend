from django.contrib import admin

from .models import About, Agreements, DeliveryInformation, Policy, ContactUs, Requisite, MainShop, OurShop


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


@admin.register(ContactUs)
class ContactUsAdmin(admin.ModelAdmin):
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
