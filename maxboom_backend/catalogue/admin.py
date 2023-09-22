from django.contrib import admin

from .models import (
    Category, Product, ProductImage, Brand,
)


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'image', 'thumbnail',
                    'img_preview', 'thumb_preview')
    list_editable = ('product',)
    list_filter = ('product',)
    readonly_fields = ('img_preview', 'thumb_preview')


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    '''Кастомный класс админки производителей.'''
    list_display = (
        'id', 'slug', 'name', 'is_prohibited'
    )
    list_editable = ('name', 'is_prohibited')
    list_filter = ('name', 'is_prohibited')
    search_fields = ('name',)
    empty_value_display = '-пусто-'


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    readonly_fields = ('img_preview', 'thumb_preview')
    extra = 0
    verbose_name = "Изображение"
    verbose_name_plural = "Изображения"


class CategoryBranchesInline(admin.TabularInline):
    model = Category
    fk_name = 'root'
    fields = ('name',)
    extra = 0
    verbose_name = "Дочерняя категория"
    verbose_name_plural = "Дочерние категории"


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    '''Кастомный класс админки категорий.'''
    list_display = (
        'id', 'slug', 'name', 'root', 'meta_title', 'meta_description',
        'is_visible_on_main', 'is_prohibited'
    )
    list_editable = ('name', 'root', 'is_prohibited', 'is_visible_on_main')
    list_filter = ('name', 'root', 'is_visible_on_main', 'is_prohibited')
    search_fields = ('name', 'meta_description')
    empty_value_display = '-пусто-'
    inlines = (
        CategoryBranchesInline,
    )


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    '''Кастомный класс админки товаров.'''
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
        'wb_urls',
        'quantity',
        'is_deleted',
        'meta_title',
        'meta_description',
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
        'meta_title',
        'meta_description',
    )
    list_filter = ('name', 'is_deleted')
    search_fields = ('name', 'description')
    inlines = (
        ProductImageInline,
    )
    empty_value_display = '-пусто-'
