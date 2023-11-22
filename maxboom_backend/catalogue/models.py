import logging
import os

from django.db import models
from django.db.models.signals import pre_delete, pre_save
from django.dispatch.dispatcher import receiver
from django.utils.html import mark_safe
from pytils.translit import slugify
from sorl.thumbnail import ImageField, delete
from sorl.thumbnail.shortcuts import get_thumbnail

logger = logging.getLogger(__name__)


def get_slug(instance):
    if type(instance) is Brand:
        name = instance.name.replace('   ', ' ').replace('  ', ' ')
        slug_n = slugify(name)[:200]
        i = 1
        while Brand.objects.filter(slug=slug_n).exists():
            if len(slug_n) == 200:
                slug_n = slug_n[:-1]
            slug_n = slug_n + str(i)
            i += 1
        return slug_n

    if type(instance) is Category:
        name = instance.name.replace('   ', ' ').replace('  ', ' ')
        slug_n = slugify(name)[:200]
        i = 1
        while Category.objects.filter(slug=slug_n).exists():
            if len(slug_n) == 200:
                slug_n = slug_n[:-1]
            slug_n = slug_n + str(i)
            i += 1
        return slug_n

    if type(instance) is Product:
        name = instance.name.replace('   ', ' ').replace('  ', ' ')
        code = str(instance.code)
        slug_n = (slugify(name)[:199 - len(code)]
                  + '-' + code)
        i = 1
        while Product.objects.filter(slug=slug_n).exists():
            if len(slug_n) == 200:
                slug_n = slug_n[:-1]
            slug_n = slug_n + str(i)
            i += 1
        return slug_n


def image_upload_path(instance, filename):
    if type(instance) is Brand:
        return os.path.join(
            'brand-images', instance.slug, filename
        )
    if type(instance) is ProductImage:
        return os.path.join('product-images', instance.product.slug, filename)
    if type(instance) is Category:
        return os.path.join(
            'category-images', instance.slug, filename
        )


class Brand(models.Model):
    """Модель производителей."""

    name = models.CharField(
        verbose_name='Наименование',
        max_length=500,
        unique=True,
    )
    slug = models.SlugField(
        verbose_name='Уникальный слаг', unique=True, max_length=200,
        null=True,
        blank=True,
        editable=False
    )
    is_prohibited = models.BooleanField(
        verbose_name='Запрещенный для публикации производитель',
        help_text='Бренд, которые не публикуются на сайте',
        default=False
    )
    is_visible_on_main = models.BooleanField(
        verbose_name='Производитель на главной странице',
        help_text=('Брэнд, которая '
                   'отображаются на главной странице'),
        default=False
    )
    image = ImageField(
        upload_to=image_upload_path,
        max_length=1000,
        verbose_name='Логотип',
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = 'Производитель'
        verbose_name_plural = 'Производители'
        ordering = ('name',)

    def __str__(self) -> str:
        return self.name

    def save(self, *args, **kwargs):
        self.slug = get_slug(self)
        super().save(*args, **kwargs)

    def img_preview(self):
        value = self.image
        if value and hasattr(value, 'url'):
            ext = 'JPEG'
            try:
                aux_ext = str(value).split('.')
                if aux_ext[len(aux_ext) - 1].lower() == 'png':
                    ext = 'PNG'
                elif aux_ext[len(aux_ext) - 1].lower() == 'gif':
                    ext = 'GIF'
            except Exception:
                pass
            try:
                mini = get_thumbnail(value, 'x80', upscale=False, format=ext)
            except Exception as e:
                logger.warning("Unable to get the thumbnail", exc_info=e)
            else:
                try:
                    output = (
                        '<div style="float:left">'
                        '<a style="width:%spx;display:block;margin:0 0 10px" '
                        'class="thumbnail" '
                        'target="_blank" href="%s">'
                        '<img src="%s"></a></div>'
                    ) % (mini.width, value.url, mini.url, )
                except (AttributeError, TypeError):
                    return None
            return mark_safe(output)
        return None
    img_preview.short_description = 'Изображение'


class Category(models.Model):
    """Модель категорий."""

    name = models.CharField(
        verbose_name='Название',
        max_length=500,
        unique=True,
    )
    slug = models.SlugField(
        verbose_name='Уникальный слаг', unique=True, max_length=200,
        null=True,
        blank=True,
        editable=False
    )
    wb_category_id = models.PositiveIntegerField(
        verbose_name='Id категории на wildberries',
        help_text='objectID на wildberries',
        unique=True,
    )
    is_visible_on_main = models.BooleanField(
        verbose_name='Категория видимая на главной странице',
        help_text=('Категория, которая '
                   'отображаются на главной странице'),
        default=False
    )
    is_prohibited = models.BooleanField(
        verbose_name='Запрещенная для публикации категория',
        help_text='Категория, которая не публикуются на сайте',
        default=False
    )
    root = models.ForeignKey(
        'self', related_name='branches',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name='Родительская категория'
    )
    image = ImageField(
        upload_to=image_upload_path,
        max_length=1000,
        verbose_name='Эскиз',
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ('name',)

    def __str__(self) -> str:
        return self.name

    def save(self, *args, **kwargs):
        self.slug = get_slug(self)
        super().save(*args, **kwargs)

    def img_preview(self):
        value = self.image
        if value and hasattr(value, 'url'):
            ext = 'JPEG'
            try:
                aux_ext = str(value).split('.')
                if aux_ext[len(aux_ext) - 1].lower() == 'png':
                    ext = 'PNG'
                elif aux_ext[len(aux_ext) - 1].lower() == 'gif':
                    ext = 'GIF'
            except Exception:
                pass
            try:
                mini = get_thumbnail(value, 'x80', upscale=False, format=ext)
            except Exception as e:
                logger.warning("Unable to get the thumbnail", exc_info=e)
            else:
                try:
                    output = (
                        '<div style="float:left">'
                        '<a style="width:%spx;display:block;margin:0 0 10px" '
                        'class="thumbnail" '
                        'target="_blank" href="%s">'
                        '<img src="%s"></a></div>'
                    ) % (mini.width, value.url, mini.url, )
                except (AttributeError, TypeError):
                    return None
            return mark_safe(output)
        return None
    img_preview.short_description = 'Эскиз'


class Product(models.Model):
    """Модель товаров."""

    name = models.CharField(verbose_name='Название', max_length=500)
    slug = models.SlugField(
        verbose_name='Уникальный слаг', unique=True, max_length=200,
        null=True,
        blank=True,
        editable=False
    )
    description = models.TextField(verbose_name='Описание')
    price = models.DecimalField(
        verbose_name='Цена',
        decimal_places=3,
        max_digits=10,
    )
    brand = models.ForeignKey(
        Brand, related_name='products', on_delete=models.SET_NULL, null=True,
        verbose_name='Производитель'
    )
    category = models.ForeignKey(
        Category, related_name='products', on_delete=models.SET_NULL,
        null=True,
        verbose_name='Категория'
    )
    code = models.IntegerField(verbose_name='Код товара', unique=True)
    vendor_code = models.CharField(
        verbose_name='Артикул продавца',
        unique=True,
        max_length=100
    )
    imt_id = models.IntegerField(
        verbose_name='id карточки на WB',
        null=True,
        blank=True,
    )
    wb_urls = models.URLField(verbose_name='Ссылка на WB')
    quantity = models.FloatField(
        verbose_name='Количество',
        default=999999,
    )
    is_deleted = models.BooleanField(
        verbose_name='Удаленный товар',
        default=False,
    )
    wholesale = models.IntegerField(
        verbose_name='Количество в оптовой партии',
        default=0
    )

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
        ordering = ('name',)

    def __str__(self) -> str:
        return self.name

    def save(self, *args, **kwargs):
        self.slug = get_slug(self)
        if not self.wb_urls:
            self.wb_urls = ('https://www.wildberries.ru/catalog/'
                            f'{self.code}/detail.aspx')
        super().save(*args, **kwargs)


class ProductImage(models.Model):
    """Модель изображений товаров"""
    product = models.ForeignKey(
        Product, related_name='images', on_delete=models.CASCADE,
        verbose_name='Продукт',
    )
    image = ImageField(
        upload_to=image_upload_path,
        max_length=1000,
        verbose_name='Изображение',
    )

    class Meta:
        verbose_name = 'Изображение товара'
        verbose_name_plural = 'Изображения товаров'

    def __str__(self) -> str:
        return self.image.name

    def img_preview(self):
        value = self.image
        if value and hasattr(value, 'url'):
            ext = 'JPEG'
            try:
                aux_ext = str(value).split('.')
                if aux_ext[len(aux_ext) - 1].lower() == 'png':
                    ext = 'PNG'
                elif aux_ext[len(aux_ext) - 1].lower() == 'gif':
                    ext = 'GIF'
            except Exception:
                pass
            try:
                mini = get_thumbnail(value, 'x80', upscale=False, format=ext)
            except Exception as e:
                logger.warning("Unable to get the thumbnail", exc_info=e)
            else:
                try:
                    output = (
                        '<div style="float:left">'
                        '<a style="width:%spx;display:block;margin:0 0 10px" '
                        'class="thumbnail" '
                        'target="_blank" href="%s">'
                        '<img src="%s"></a></div>'
                    ) % (mini.width, value.url, mini.url, )
                except (AttributeError, TypeError):
                    return None
            return mark_safe(output)
        return None
    img_preview.short_description = 'Изображение'


@receiver(pre_delete, sender=Brand)
@receiver(pre_delete, sender=ProductImage)
def image_model_delete(sender, instance, **kwargs):
    if instance.image.name:
        delete(instance.image)


@receiver(pre_save, sender=Category)
@receiver(pre_save, sender=Brand)
@receiver(pre_save, sender=ProductImage)
def image_model_update(sender, instance, **kwargs):
    pk = instance.pk
    if sender.objects.filter(pk=pk).exists():
        old_item = sender.objects.get(pk=pk)
        if old_item.image.name != instance.image.name:
            delete(old_item.image.name)
