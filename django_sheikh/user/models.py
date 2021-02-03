from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone


class User(AbstractUser):
    pass


class Position(models.Model):
    """
    User position
    """
    latitude = models.CharField(max_length=50, verbose_name='Ширина')
    longitude = models.CharField(max_length=50, verbose_name='Долгота')
    date = models.DateTimeField(default=timezone.now, verbose_name='Время')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')

    def __str__(self):
        return f'Position(id={self.id})'

    class Meta:
        verbose_name_plural = 'Позиции'
        verbose_name = 'Позиция'
