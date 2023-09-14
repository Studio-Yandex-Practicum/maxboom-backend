from django.db import models


class Category(models.Model):
    """Модель категоирий."""

    name = models.CharField(
        verbose_name="название",
        max_length=500,
        unique=True,
    )
    meta_title = models.CharField(
        max_length=255,
        verbose_name="мета-название категории",
        null=True,
        blank=True,
    )
    meta_description = models.CharField(
        max_length=255,
        verbose_name="мета-описание категории",
        null=True,
        blank=True
    )

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self) -> str:
        return self.name


class Product(models.Model):
    """Модель товаров."""

    name = models.CharField(verbose_name="название", max_length=500)
    description = models.TextField(verbose_name="описание")
    price = models.DecimalField(
        verbose_name="цена",
        decimal_places=3,
        max_digits=10,
    )
    brand = models.CharField(verbose_name="производитель", max_length=200)
    category = models.ForeignKey(
        Category, related_name="products", on_delete=models.SET_NULL, null=True
    )
    code = models.IntegerField(verbose_name="код товара", unique=True)
    wb_urls = models.URLField(verbose_name="ссылка на WB")
    quantity = models.FloatField(
        verbose_name="количество",
        default=999999,
    )
    is_deleted = models.BooleanField(
        verbose_name="Удален ли товар",
        default=False,
    )
    meta_title = models.CharField(
        max_length=255,
        verbose_name="Мета-название товара",
        null=True,
        blank=True,
    )
    meta_description = models.CharField(
        max_length=255,
        verbose_name="Мета-описание товара",
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"

    def __str__(self) -> str:
        return self.name


class ProductImage(models.Model):
    product = models.ForeignKey(
        Product, related_name="images", on_delete=models.CASCADE
    )
    image = models.ImageField(upload_to="products_images")

    class Meta:
        verbose_name = "Картинка товара"
        verbose_name_plural = "Картинки товаров"
