from django.db import models
from django.utils import timezone


class Company(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название компании')
    domain = models.CharField(max_length=100, verbose_name='Домейн компании')
    icon = models.URLField(max_length=200, verbose_name='Иконка')

    request = models.IntegerField(default=0, verbose_name='Запросы')

    def __str__(self):
        return f'Company(id={self.id}, name={self.name})'

    class Meta:
        verbose_name_plural = 'Компании'
        verbose_name = 'Компиния'


class Site(models.Model):
    url = models.URLField(max_length=150, verbose_name='Сслыка')
    title = models.CharField(max_length=300, verbose_name='Название')
    description = models.TextField(max_length=500, null=True, blank=True,
                                   verbose_name='Описание')

    og_url = models.CharField(max_length=150, null=True, blank=True,
                               verbose_name='OG сслыка')
    og_title = models.CharField(max_length=300, null=True, blank=True,
                               verbose_name='OG название')
    og_description = models.TextField(max_length=500, null=True, blank=True,
                               verbose_name='OG описание')
    og_type = models.CharField(max_length=50, null=True, blank=True,
                               verbose_name='Тип')
    og_image = models.URLField(max_length=50, null=True, blank=True,
                               verbose_name='Изобращение')

    date = models.DateTimeField(default=timezone.now, verbose_name='Последние обновление')

    company = models.ForeignKey(Company, on_delete=models.CASCADE, verbose_name='Компиния')

    request = models.IntegerField(default=0, verbose_name='Запросы')

    def __str__(self):
        return f'Site(id={self.id})'

    class Meta:
        verbose_name_plural = 'Сайты'
        verbose_name = 'Сайт'


class Keyword(models.Model):
    key = models.CharField(max_length=100, verbose_name='Ключ')
    site = models.ManyToManyField(Site, verbose_name='Сайт')

    request = models.IntegerField(default=0, verbose_name='Запросы')


    def __str__(self):
        return f'Keyword(id={self.id}, key={self.key})'

    class Meta:
        verbose_name_plural = 'Ключивые слова'
        verbose_name = 'Ключиваое слово'
