from django.contrib import admin

from .models import Category, Product, ProductImage


admin.site.register(ProductImage)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Кастомный класс админки категорий."""
    list_display = ("id", "name", "meta_title", "meta_description")
    list_filter = ("name",)
    search_fields = ("name", "author_name")


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """Кастомный класс админки товаров."""
    list_display = (
        "id",
        "name",
        "description",
        "price",
        "brand",
        "category",
        "code",
        "wb_urls",
        "quantity",
        "is_deleted",
        # 'images'
        "meta_title",
        "meta_description",
    )
    list_filter = ("name",)
    search_fields = ("name", "author_name")
