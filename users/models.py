from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name="Почта")
    phone = models.CharField(max_length=30, verbose_name="Номер телефона", null=True, blank=True)
    avatar = models.ImageField(upload_to='users/', verbose_name="Аватар", blank=True, null=True)
    token = models.CharField(verbose_name="Токен", max_length=100, null=True, blank=True)
    is_active = models.BooleanField(verbose_name="Статус пользователя", default=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        permissions = [
            ('change_user_status', 'Can block/unblock user'),
        ]
