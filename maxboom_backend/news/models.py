from django.db import models


class News(models.Model):
    """
    Модель новостей.
    """
    title = models.CharField(
        max_length=250,
        verbose_name='Заголовок')
    text = models.TextField(
        verbose_name='Текст')
    image = models.ImageField(
        verbose_name='Изображение',
        null=True, blank=True, upload_to='news/')
    pub_date = models.DateField(
        auto_now_add=True,
        verbose_name='Дата публикации')
    slug = models.SlugField(
        unique=True,
        max_length=50,
        verbose_name='Слаг')
    meta_title = models.CharField(
        max_length=255,
        verbose_name='Мета-название страницы',
        null=True,
        blank=True)
    meta_description = models.CharField(
        max_length=255,
        verbose_name='Мета-описание страницы',
        null=True,
        blank=True)

    class Meta:
        ordering = ['-pub_date']
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'

    def __str__(self) -> str:
        return self.title[:15]
