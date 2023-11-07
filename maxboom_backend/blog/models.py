from django.contrib.auth import get_user_model
from django.db import models


User = get_user_model()


class MetaDataModel(models.Model):
    """
    Базовая абстрактная модель с мета-данными.
    """

    meta_title = models.CharField(
        verbose_name='Мета-название страницы',
        help_text='Мета-название страницы для SEO',
        max_length=255,
        blank=True,
        null=True)
    meta_description = models.CharField(
        verbose_name='Мета-описание страницы',
        help_text='Мета-описание страницы для SEO',
        max_length=255,
        blank=True,
        null=True)

    class Meta:
        abstract = True


class Category(MetaDataModel):
    """
    Модель категории постов.
    """

    title = models.CharField(
        max_length=250,
        verbose_name='Название категории',
        help_text='Название категории')
    slug = models.SlugField(
        unique=True,
        max_length=50,
        verbose_name='Слаг',
        help_text='Слаг для категории')

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
        help_text='Название тега',
        max_length=200)

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'
        ordering = ['id']

    def __str__(self) -> str:
        return self.name[:15]


class Post(MetaDataModel):
    """
    Модель для постов.
    """

    title = models.CharField(
        verbose_name='Заголовок',
        help_text='Заголовок поста',
        max_length=255)
    text = models.TextField(
        verbose_name='Текст',
        help_text='Текст поста')
    author = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Автор',
        help_text='Автор поста')
    pub_date = models.DateField(
        verbose_name='Дата публикации',
        help_text='Дата создания поста',
        auto_now_add=True)
    image = models.ImageField(
        verbose_name='Изображение',
        help_text='Изображние для поста',
        upload_to='blog/',
        blank=True,
        null=True)
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        verbose_name='Категория',
        help_text='Категория, к которой относится пост',
        related_name='posts',
        blank=True,
        null=True)
    tags = models.ManyToManyField(
        Tag,
        verbose_name='Теги',
        help_text='Теги для поста.',
        related_name='posts',
        blank=True)
    views = models.PositiveIntegerField(
        verbose_name='Количество просмотров',
        help_text='Количество просмотров пользователями данного поста',
        default=0)
    slug = models.SlugField(
        unique=True,
        max_length=50,
        verbose_name='Слаг',
        help_text='Слаг для поста')

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'
        ordering = ['-pub_date']

    def __str__(self) -> str:
        return self.title[:30]

    def save(self, *args, **kwargs):
        """
        Если указан автор и не суперюзер, то устанавливаем
        автором первого суперюзера для постов.
        """

        if self.author and not self.author.is_superuser:
            super_user = User.objects.filter(is_superuser=True).first()
            self.author = super_user
            self.author.save()
        super().save(*args, **kwargs)


class Comments(models.Model):
    """
    Модель для комментариев.
    """

    author = models.CharField(
        max_length=200,
        verbose_name='Имя',
        help_text='Автор комментария')
    post = models.ForeignKey(
        Post,
        verbose_name='Пост',
        help_text='Комментарий для данного поста',
        on_delete=models.CASCADE,
        related_name='comments')
    text = models.TextField(
        verbose_name='Комментарий',
        help_text='Текст комментария')
    pub_date = models.DateField(
        verbose_name='Дата создания',
        help_text='Дата создания комментария',
        auto_now_add=True)
    is_published = models.BooleanField(
        verbose_name='Опубликован',
        help_text='Статус публикации комментария',
        default=False)

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ['-pub_date']

    def __str__(self):
        return self.text[:30]
