from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

MIN_AMOUNT = 1
MAX_AMOUNT = 5


class ShopReviews(models.Model):
    text = models.TextField(
        verbose_name='Отзыв',
        help_text='Отзыв о магазине',
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания отзыва',
        help_text='Дата создания отзыва')
    author_name = models.CharField(
        max_length=200,
        verbose_name='Имя',
        help_text='Имя автора отзыва',
    )
    author_email = models.EmailField(
        max_length=200,
        verbose_name='Почта',
        help_text='Почта автора отзыва',
        blank=True,
        null=True,
    )
    delivery_speed_score = models.PositiveIntegerField(
        verbose_name='Скорость доставки',
        help_text='Оценка скорости доставки товаров',
        validators=(
            MinValueValidator(MIN_AMOUNT),
            MaxValueValidator(MAX_AMOUNT)
        )
    )
    quality_score = models.PositiveIntegerField(
        verbose_name='Качество товара',
        help_text='Оценка качества товара в магазине',
        validators=(
            MinValueValidator(MIN_AMOUNT),
            MaxValueValidator(MAX_AMOUNT)
        )
    )
    price_score = models.PositiveIntegerField(
        verbose_name='Цена',
        help_text='Оценка цен в магазине',
        validators=(
            MinValueValidator(MIN_AMOUNT),
            MaxValueValidator(MAX_AMOUNT)
        )
    )
    is_published = models.BooleanField(
        verbose_name='Публикация',
        help_text='Разрешить публикацию отзыва',
        default=False
    )

    @property
    def average_score(obj):
        return round(
            (obj.price_score
             + obj.quality_score
             + obj.delivery_speed_score) / 3, 1)

    average_score.fget.short_description = 'Средняя оценка'

    class Meta:
        verbose_name = 'Отзыв о магазине'
        verbose_name_plural = 'Отзывы о магазине'
        ordering = ('-pub_date',)

    def __str__(self):
        return self.text[:15]


class ReplayToReview(models.Model):
    text = models.TextField(
        verbose_name='Ответ',
        help_text='Ответ на отзыв'
    )
    name = models.CharField(
        max_length=200,
        verbose_name='Имя',
        help_text='Имя автора ответа',
        default='Администратор'
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата',
        help_text='Дата создания ответа')
    review_id = models.OneToOneField(
        ShopReviews,
        on_delete=models.CASCADE,
        related_name='replay',
        verbose_name='Отзыв о магазине',
        help_text='Отзыв о магазине, на который отвечает администратор',
    )

    class Meta:
        verbose_name = 'Ответ на отзыв'
        verbose_name_plural = 'Ответы на отзывы'
        ordering = ('-pub_date',)

    def __str__(self):
        return self.text[:15]
