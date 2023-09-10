from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class Category(models.Model):
    """
    Модель категории постов.
    """
    title = models.CharField(
        max_length=250)
    slug = models.SlugField(
        unique=True,
        max_length=50,
        verbose_name='Слаг')
    meta_title = models.CharField(
        verbose_name='Мета-название страницы',
        max_length=255,
        blank=True,
        null=True)
    meta_description = models.CharField(
        verbose_name='Мета-описание страницы',
        max_length=255,
        blank=True,
        null=True)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['id']

    def __str__(self) -> str:
        return self.title[:15]


class Tag(models.Model):
    """
    Модель тегов.
    """
    name = models.CharField(
        verbose_name='Название',
        max_length=200)

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'
        ordering = ['id']

    def __str__(self) -> str:
        return self.name[:15]


class Post(models.Model):
    """
    Модель для постов.
    """
    title = models.CharField(
        verbose_name='Заголовок',
        max_length=255)
    text = models.TextField(
        verbose_name='Текст')
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор')
    pub_date = models.DateField(
        verbose_name='Дата публикации',
        auto_now_add=True)
    image = models.ImageField(
        verbose_name='Изображение',
        upload_to='blog/',
        blank=True,
        null=True)
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        verbose_name='Категория',
        blank=True,
        null=True)
    tags = models.ManyToManyField(
        Tag,
        through='PostTag',
        verbose_name='Тег')
    slug = models.SlugField(
        unique=True,
        max_length=50,
        verbose_name='Слаг')
    meta_title = models.CharField(
        verbose_name='Мета-название страницы',
        max_length=255,
        blank=True,
        null=True)
    meta_description = models.CharField(
        verbose_name='Мета-описание страницы',
        max_length=255,
        blank=True,
        null=True)

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'
        ordering = ['id']

    def __str__(self) -> str:
        return self.title[:30]


class PostTag(models.Model):
    """
    Промежуточная модель тегов и постов.
    """
    post = models.ForeignKey(
        Post,
        verbose_name='Пост',
        on_delete=models.CASCADE)
    tag = models.ForeignKey(
        Tag,
        verbose_name='Тег',
        on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Пост и тег'
        verbose_name_plural = 'Посты и теги'
        ordering = ['id']

    def __str__(self) -> str:
        return f'{self.post} с тегом {self.tag}'
