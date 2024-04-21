from django.db import models
from django.contrib.auth import get_user_model

from catalogue.models import Product
from maxboom.settings import DISCOUNT_ANONYM, DISCOUNT_USER

User = get_user_model()


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

    @property
    def cart_full_weight(self):
        """Высчитывает полный вес корзины."""
        products = self.products.through.objects.filter(cart=self)
        weights = [
            round(product.full_weight, 2) for product in products
        ]
        return sum(weights)

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
    def price_with_discount(self):
        if self.cart.is_active and self.cart.user.userprofile.is_vendor:
            discount = DISCOUNT_USER
        else:
            discount = DISCOUNT_ANONYM
        return round(self.product.price * discount, 2)

    @property
    def full_price(self):
        """Высчитывает полную стоимость продукта в корзине."""
        price = self.price_with_discount
        return round(price * self.amount, 2)

    @property
    def full_weight(self):
        """Высчитывает полный вес продукта в корзине."""
        return self.product.weight * self.amount

    def __str__(self):
        return (f"Продукт {self.product.name} "
                f"в корзине пользователя: {self.cart.user}")
