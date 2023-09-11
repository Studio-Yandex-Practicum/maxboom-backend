from django.db import models


class Category(models.Model):
    name = models.CharField(verbose_name='название', max_length=500)


class Product(models.Model):
    name = models.CharField(verbose_name='название', max_length=500)
    description = models.TextField(verbose_name='описание')
    price = models.DecimalField(
        verbose_name='цена',
        decimal_places=3,
        max_digits=10,
    )
    brand = models.CharField(verbose_name='производитель', max_length=200)
    category = models.ForeignKey(Category, related_name='images', on_delete=models.SET_NULL, null=True)
    code = models.IntegerField(verbose_name='код товара')
    wb_urls = models.URLField(verbose_name='ссылка на WB')
    is_deleted = models.BooleanField(
        verbose_name='Удален ли товар', default=False)


class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='products_images')


class ProductQuantity(models.Model):
    product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE)
    quantity = models.FloatField(
        verbose_name='количество',
        default=999999,
    )


# class Order(models.Model):
#     total_price = models.DecimalField(
#         verbose_name='цена',
#         decimal_places=3,
#         max_digits=10,
#     )
#     products = models.ManyToManyField(
#         'OrderProductQuantity', 
#         verbose_name='Категория',
#         related_name='products',
# )
#     status = models.CharField(verbose_name='статус')


# class OrderProductQuantity(models.Model):

#     product = models.ForeignKey(Product, on_delete=models.CASCADE)
#     order = models.ForeignKey(Order, on_delete=models.CASCADE)
#     product_quantity = models.FloatField(verbose_name='количество товара')

#     class Meta:
#         verbose_name = 'Товар в заказе'
#         verbose_name_plural = 'Товары в заказе'
#         constraints = (
#             models.UniqueConstraint(
#                 fields=('product', 'order'), name='unique_order_product'
#             ),
#         )


# class ShoppingCart(models.Model):
#     pass