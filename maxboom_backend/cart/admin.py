from django.contrib import admin

from cart.models import Cart, ProductCart


class ProductCartInline(admin.StackedInline):
    model = ProductCart
    extra = 0


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    inlines = [ProductCartInline, ]


@admin.register(ProductCart)
class ProductCartAdmin(admin.ModelAdmin):
    ...
