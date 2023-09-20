from django.contrib import admin

from .models import (
    Category, Product, ProductImage, Brand, CategoryTree
)


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'image', 'img_preview',)
    list_editable = ('product',)
    list_filter = ('product',)
    readonly_fields = ('img_preview',)


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    '''Кастомный класс админки производителей.'''
    list_display = (
        'id', 'slug', 'name', 'is_prohibited'
    )
    list_editable = ('name',)
    list_filter = ('name', 'is_prohibited')
    search_fields = ('name',)
    empty_value_display = '-пусто-'


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    readonly_fields = ('img_preview',)
    extra = 0


class CategoryTreeRootInline(admin.TabularInline):
    model = CategoryTree
    fk_name = 'parent_id'
    extra = 0


class CategoryTreeAffiliatedInline(admin.TabularInline):
    model = CategoryTree
    fk_name = 'affiliated_id'
    extra = 0


@admin.register(CategoryTree)
class CategoryTreeAdmin(admin.ModelAdmin):
    '''Кастомный класс админки дерева категорий.'''
    list_display = (
        'id', 'parent_id', 'affiliated_id',
    )
    list_editable = (
        'parent_id', 'affiliated_id',
    )


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    '''Кастомный класс админки категорий.'''
    list_display = (
        'id', 'slug', 'name', 'meta_title', 'meta_description',
        'is_visible_on_main', 'is_prohibited'
    )
    list_editable = ('name',)
    list_filter = ('name', 'is_visible_on_main', 'is_prohibited')
    search_fields = ('name', 'meta_description')
    empty_value_display = '-пусто-'
    inlines = (
        CategoryTreeRootInline,
        CategoryTreeAffiliatedInline
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
