from django.contrib import admin
from sorl.thumbnail.admin import AdminImageMixin

from .models import Brand, Category, Product, ProductImage


@admin.register(ProductImage)
class ProductImageAdmin(AdminImageMixin, admin.ModelAdmin):
    """Админка изображений"""
    list_display = ('id', 'product', 'image', 'img_preview')
    list_editable = ('product',)
    search_fields = ('product__name',)
    ordering = ('product',)
    list_per_page = 10


@admin.register(Brand)
class BrandAdmin(AdminImageMixin, admin.ModelAdmin):
    """Админка производителей"""
    list_display = (
        'id', 'slug', 'name', 'is_prohibited', 'is_visible_on_main',
        'img_preview'
    )
    list_editable = ('name', 'is_prohibited', 'is_visible_on_main')
    list_filter = (
        ('name', admin.filters.AllValuesFieldListFilter),
        'is_prohibited',
        'is_visible_on_main'
    )
    search_fields = ('name',)
    empty_value_display = '-пусто-'


class CategoryBranchesInline(admin.TabularInline):
    """Включение подкатегорий в админку категорий"""
    model = Category
    fk_name = 'root'
    fields = ('name',)
    extra = 0
    verbose_name = "Дочерняя категория"
    verbose_name_plural = "Дочерние категории"


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Админка категорий"""
    list_display = (
        'id', 'slug', 'name', 'root',
        'is_visible_on_main', 'is_prohibited', 'wb_category_id',
        'img_preview'
    )
    list_editable = (
        'name', 'root', 'is_prohibited', 'is_visible_on_main', 'wb_category_id'
    )
    list_filter = (
        ('root', admin.filters.AllValuesFieldListFilter),
        'is_visible_on_main',
        'is_prohibited')
    search_fields = ('name', 'wb_category_id')
    empty_value_display = '-пусто-'
    inlines = (
        CategoryBranchesInline,
    )


class ProductImageInline(AdminImageMixin, admin.TabularInline,):
    """Включение изображений в админку товаров"""
    model = ProductImage
    extra = 0
    verbose_name = "Изображение"
    verbose_name_plural = "Изображения"


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """Админка товаров"""
    list_select_related = ('brand', 'category',)
    list_display = (
        'id',
        'name',
        'slug',
        # 'description',
        'price',
        'brand',
        'category',
        'code',
        'vendor_code',
        'imt_id',
        'wb_urls',
        'quantity',
        'is_deleted',
        'wholesale'
    )
    list_editable = (
        'name',
        'price',
        'brand',
        'category',
        'code',
        'wb_urls',
        'quantity',
        'is_deleted',
        'imt_id',
        'vendor_code',
        'wholesale'
    )
    list_filter = ('is_deleted', 'category', 'brand',)
    search_fields = ('name', 'description')
    inlines = (
        ProductImageInline,
    )
    empty_value_display = '-пусто-'
    list_per_page = 10
