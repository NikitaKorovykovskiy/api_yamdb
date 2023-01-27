from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    """Расширенная модель пользователя"""
    USER = 'user'
    MODERATOR = 'moderator'
    ADMIN = 'admin'

    ROLE_CHOICES = [
        (USER, 'Пользователь'),
        (MODERATOR, 'Модератор'),
        (ADMIN, 'Администратор'),
    ]

    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(
        'email adress', max_length=254, unique=True
    )
    role = models.CharField(
        'Роль', max_length=150,
        choices=ROLE_CHOICES, default=USER
    )
    bio = models.TextField('Биография', blank=True)

    REQUIRED_FIELDS = ['username']
    USERNAME_FIELD = 'email'

    @property
    def is_user(self):
        return self.role == self.USER

    @property
    def is_admin(self):
        return self.role == self.ADMIN

    @property
    def is_moderator(self):
        return self.role == self.MODERATOR

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
