from django.db import models

from maxboom.settings import NEWS_LIMIT


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

    class Meta:
        ordering = ['-pub_date']
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'

    def __str__(self) -> str:
        return self.title[:NEWS_LIMIT]
