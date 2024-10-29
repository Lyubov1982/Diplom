from django.db import models


class Project(models.Model):
    title = models.CharField(max_length=200, verbose_name='Название')
    description = models.TextField(blank=True, verbose_name='Описание')
    featured_image = models.ImageField(default='default.jpg', upload_to='projects/%Y/%m/%d', verbose_name='Изображение')
    demo_link = models.CharField(max_length=200, blank=True, verbose_name='Ссылка')
    source_link = models.CharField(max_length=200, blank=True, verbose_name='Ссылка')
    tags = models.ManyToManyField('Tag', blank=True, verbose_name='Тэг')
    vote_total = models.IntegerField(default=0, blank=True, verbose_name='Кол-во отзывов')
    vote_ratio = models.IntegerField(default=0, blank=True, verbose_name='Кол-во отзывов')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'статьи'


class Tag(models.Model):
    name = models.CharField(max_length=200, verbose_name='Наименование')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Дата')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Тэг'
        verbose_name_plural = 'тэги'

class UsefulLink(models.Model):
    title = models.CharField(max_length=255, verbose_name='Наименование')
    url = models.URLField()
    icon_url = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Сайт'
        verbose_name_plural = 'сайты'