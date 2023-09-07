"""
Модели для пользователей.
"""
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.db import models
from django.utils import timezone


class UserManager(BaseUserManager):
    """Менеджер для пользователей."""

    def create_user(self, email, password=None, **extra_fields):
        """Создает в возвращает пользователя."""
        if not email:
            raise ValueError('У пользователя должен быть email адрес.')
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        UserProfile.objects.create(user=user)

        return user

    def create_superuser(self, email, password):
        """Создает и возвращает суперпользователя."""
        user = self.create_user(email, password)
        user.is_active = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """Пользователь в системе. Облегченная модель."""
    email = models.EmailField('Почта', max_length=255, unique=True)
    is_active = models.BooleanField('Активен', default=False)
    is_staff = models.BooleanField('Персонал', default=False)
    date_joined = models.DateTimeField('Дата создания', default=timezone.now)

    objects = UserManager()

    USERNAME_FIELD = 'email'

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('-id',)

    def __str__(self):
        return self.email


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=255, blank=True)
    last_name = models.CharField(max_length=255, blank=True)
    about = models.TextField(blank=True)
    company = models.CharField(max_length=255, blank=True)
    is_vendor = models.BooleanField('Оптовик', default=False)

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'
        ordering = ('-id',)

    def __str__(self):
        return self.user.email
