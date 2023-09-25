
from django.db import models
from pytils.translit import slugify
from django.utils.html import mark_safe
from django.db.models.signals import pre_delete
from django.dispatch.dispatcher import receiver
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFit, Resize, Image


class Brand(models.Model):
    '''Модель производителей.'''

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
        help_text='Бренды, которые не публикуются на сайте',
        default=False
    )

    class Meta:
        verbose_name = 'Производитель'
        verbose_name_plural = 'Производители'
        ordering = ('name',)

    def __str__(self) -> str:
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)[:200]
        super().save(*args, **kwargs)


class Category(models.Model):
    '''Модель категорий.'''

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
    meta_title = models.CharField(
        max_length=255,
        verbose_name='Мета-название категории',
        null=True,
        blank=True,
    )
    meta_description = models.CharField(
        max_length=255,
        verbose_name='Мета-описание категории',
        null=True,
        blank=True
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

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ('name',)

    def __str__(self) -> str:
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)[:200]
        super().save(*args, **kwargs)


class Product(models.Model):
    '''Модель товаров.'''

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
        verbose_name='Бренд'
    )
    category = models.ForeignKey(
        Category, related_name='products', on_delete=models.SET_NULL,
        null=True,
        verbose_name='Категория'
    )
    code = models.IntegerField(verbose_name='Код товара', unique=True)
    wb_urls = models.URLField(verbose_name='Ссылка на WB')
    quantity = models.FloatField(
        verbose_name='Количество',
        default=999999,
    )
    is_deleted = models.BooleanField(
        verbose_name='Удален ли товар',
        default=False,
    )
    meta_title = models.CharField(
        max_length=255,
        verbose_name='Мета-название товара',
        null=True,
        blank=True,
    )
    meta_description = models.CharField(
        max_length=255,
        verbose_name='Мета-описание товара',
        null=True,
        blank=True,
    )

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)[:200]
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
        ordering = ('name',)

    def __str__(self) -> str:
        return self.name


class ProductImage(models.Model):
    product = models.ForeignKey(
        Product, related_name='images', on_delete=models.CASCADE,
        verbose_name='Продукт',
    )
    image = models.ImageField(
        upload_to='products-images',
        verbose_name='Изображение',
    )
    thumbnail = ImageSpecField(
        source='image',
        processors=[ResizeToFit(200, 200)],
        format='JPEG',
        options={'quality': 60}
    )

    class Meta:
        verbose_name = 'Изображение товара'
        verbose_name_plural = 'Изображения товаров'

    def __str__(self) -> str:
        return self.image.name

    def img_preview(self):
        return mark_safe(f"<img src = '{self.image.url}' width = '300'/>")

    def thumb_preview(self):
        return mark_safe(f"<img src = '{self.thumbnail.url}' width = '200'/>")


class Resize(Resize):
    """
    Resizes an image to the specified width and height.

    """

    def process(self, img):
        if self.upscale or (self.width < img.size[0] and self.height < img.size[1]):
            img = img.convert('RGBA')
            img = img.resize((self.width, self.height), Image.LANCZOS)
        return img


@receiver(pre_delete, sender=ProductImage)
def image_model_delete(sender, instance, **kwargs):
    if instance.image.name:
        instance.image.delete(False)
    if instance.thumbnail.name:
        instance.thumbnail.delete(False)
