from django.db import models


class News(models.Model):
    """
    Модель новостей.
    """

    title = models.CharField(
        max_length=250,
        verbose_name='Заголовок',
        help_text='Название новости')
    text = models.TextField(
        verbose_name='Текст',
        help_text='Тест для новости')
    image = models.ImageField(
        verbose_name='Изображение',
        help_text='Изображение для новости',
        null=True,
        blank=True,
        upload_to='news/')
    pub_date = models.DateField(
        auto_now_add=True,
        verbose_name='Дата публикации',
        help_text='Дата создания новости')
    slug = models.SlugField(
        unique=True,
        max_length=50,
        verbose_name='Слаг',
        help_text='Слаг для новости')
    meta_title = models.CharField(
        max_length=255,
        verbose_name='Мета-название страницы',
        help_text='Мета-название новости для SEO',
        null=True,
        blank=True)
    meta_description = models.CharField(
        max_length=255,
        verbose_name='Мета-описание страницы',
        help_text='Мета-описание новости для SEO',
        null=True,
        blank=True)

    class Meta:
        ordering = ['-pub_date']
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'

    def __str__(self) -> str:
        return self.title[:30]
