from django.db import models


class Story(models.Model):
    name = models.CharField(verbose_name='Заголовок', max_length=255)
    link = models.URLField(null=True, blank=True,)
    pictures = models.ManyToManyField(
        'Picture',
        related_name='stories',
        verbose_name='Картинки к истории',
    )
    pub_date = models.DateField(
        verbose_name='Дата добавления',
        auto_now_add=True
    )
    show = models.BooleanField(verbose_name='Показать', default=False)

    class Meta:
        verbose_name = 'История'
        verbose_name_plural = 'Истории'
        ordering = ['id']

    def __str__(self):
        return self.name


class Picture(models.Model):
    name = models.CharField(verbose_name='Имя картинки', max_length=255)
    image = models.ImageField(upload_to='story_pictures/')
    pub_date = models.DateField(
        verbose_name='Дата добавления',
        auto_now_add=True
    )

    class Meta:
        verbose_name = 'Картинка к истории'
        verbose_name_plural = 'Картинки к историям'
        ordering = ['id']

    def __str__(self):
        return str(self.image)
