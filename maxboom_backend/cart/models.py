from django.db import models

from accounts.models import User
from catalogue.models import Product


class Cart(models.Model):
    user = models.OneToOneField(
        User,
        null=True,
        blank=True,
        related_name='cart',
        on_delete=models.CASCADE,
    )
    products = models.ManyToManyField(
        Product,
        through='ProductCart',
    )
    session_id = models.CharField(
        max_length=100,
        null=True,
        blank=True,
    )
    is_active = models.BooleanField(default=False)

    class Meta:
        ordering = ['id']
        verbose_name = "Корзина"
        verbose_name_plural = "Корзины"

    @property
    def cart_full_price(self):
        """Высчитывает полную стоимость корзины."""
        products = self.products.through.objects.filter(cart=self)
        prices = [
            round(product.full_price, 2) for product in products
        ]
        return round(sum(prices), 2)

    def __str__(self):
        return f"Корзина пользователя: {self.user}"


class ProductCart(models.Model):
    cart = models.ForeignKey(
        Cart,
        on_delete=models.CASCADE,
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
    )
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
        """Высчитывает полную стоимость продукта в корзине."""
        price = self.product.price
        return round(price * self.amount, 2)

    def __str__(self):
        return (f"Продукт {self.product.name} "
                f"в корзине пользователя: {self.cart.user}")
