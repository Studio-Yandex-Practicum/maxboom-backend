import uuid

from django.db import models

from accounts.models import User
from catalogue.models import Product


class Cart(models.Model):
    user = models.OneToOneField(
        User, null=True, related_name='cart', on_delete=models.CASCADE
    )
    cart_id = models.UUIDField(default=uuid.uuid4, editable=False)
    products = models.ManyToManyField(
        Product,
        through='ProductCart',
    )

    @property
    def cart_full_price(self):
        products = self.products.through.objects.all()
        prices = [
            round(product.full_price, 2) for product in products
        ]
        return sum(prices)

    class Meta:
        ordering = ['id']
        verbose_name = "Корзина"
        verbose_name_plural = "Корзины"

    def __str__(self):
        return f"Корзина пользователя: {self.user}"


class ProductCart(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    amount = models.PositiveIntegerField()

    class Meta:
        ordering = ['id']
        verbose_name = "Продукт в корзине"
        verbose_name_plural = "Продукты в корзине"
        constraints = [
            models.UniqueConstraint(
                fields=('cart', 'product'),
                name='unique_cart_product'
            )
        ]

    @property
    def full_price(self):
        price = self.product.price
        return price * self.amount

    def __str__(self):
        return (f"Продукт {self.product.name} "
                f" в корзине пользователя {self.cart.user}")
