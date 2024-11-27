from django.db import models
from users.models import Profile
from django.contrib.auth.models import User


class Project(models.Model):
    owner = models.ForeignKey(Profile, on_delete=models.SET_NULL, blank=True, null=True, verbose_name='Автор')
    sections = models.ManyToManyField('Section', blank=True, verbose_name='Категории')
    title = models.CharField(max_length=200, verbose_name='Название')
    description = models.TextField(blank=True, verbose_name='Описание')
    featured_image = models.ImageField(default='default.jpg', upload_to='projects/%Y/%m/%d', verbose_name='Изображение')
    demo_link = models.CharField(max_length=200, blank=True, verbose_name='Ссылка на демонстрацию')
    source_link = models.CharField(max_length=200, blank=True, verbose_name='Ссылка на источник')
    tags = models.ManyToManyField('Tag', blank=True, verbose_name='Тег')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    likes = models.ManyToManyField(User, related_name='project_likes', blank=True, verbose_name='Лайки')

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created']
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


class Section(models.Model):
    name = models.CharField(max_length=200, verbose_name='Название раздела')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Раздел'
        verbose_name_plural = 'разделы'


class UsefulLink(models.Model):
    title = models.CharField(max_length=255, verbose_name='Наименование')
    url = models.URLField()
    icon_url = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Сайт'
        verbose_name_plural = 'сайты'


class Comment(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, blank=True)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.author.name} - {self.content[:50]}'

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'комментарии'
