from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, verbose_name='Пользователь')
    name = models.CharField(max_length=200, blank=True, verbose_name='Имя')
    email = models.EmailField(max_length=200, blank=True, verbose_name='Эл.адрес')
    nickname = models.CharField(max_length=200, blank=True, verbose_name='Псевдоним')
    myself_short = models.CharField(max_length=200, blank=True, verbose_name='О себе коротко')
    myself = models.TextField(blank=True, verbose_name='О себе')
    photo = models.ImageField(upload_to='profiles/', default='profiles/coach.jpg', verbose_name='Фото')
    video = models.FileField(upload_to='videos/', blank=True, null=True, verbose_name='Видео')
    note = models.TextField(blank=True, null=True, verbose_name='Заметка')
    social_youtube = models.CharField(max_length=200, blank=True, verbose_name='Youtube')
    social_site = models.CharField(max_length=200, blank=True, verbose_name='Социальная сеть')
    social_website = models.CharField(max_length=200, blank=True, verbose_name='Сайт')
    document = models.FileField(upload_to='documents/', verbose_name='Документ об образовании', null=True, blank=False)
    work = models.CharField(max_length=200, blank=True, verbose_name='Место работы')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Дата')

    def __str__(self):
        return self.nickname

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'профили'


class Skill(models.Model):
    expert = models.ForeignKey(Profile, on_delete=models.CASCADE, blank=True, verbose_name='Эксперт')
    qualification = models.CharField(max_length=200, blank=True, verbose_name='Квалификация')
    info = models.TextField(blank=True, verbose_name='Описание')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Дата')

    def __str__(self):
        return self.qualification

    class Meta:
        verbose_name = 'Квалификация'
        verbose_name_plural = 'квалификации'


class Photo(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='photos')
    image = models.ImageField(upload_to='photos/', verbose_name='Фото')
    caption = models.TextField(blank=True, null=True, verbose_name='Подпись')
    likes = models.ManyToManyField(User, related_name='photo_likes', blank=True)
    created = models.DateTimeField(auto_now_add=True, verbose_name='Дата')

    def __str__(self):
        return f"{self.profile.nickname} - {self.created}"

    class Meta:
        verbose_name = 'Фото'
        verbose_name_plural = 'фотографии'


# class Video(models.Model):
#     profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='videos')
#     video = models.FileField(upload_to='videos/', verbose_name='Видео')
#     caption = models.TextField(blank=True, null=True, verbose_name='Подпись')
#     likes = models.ManyToManyField(User, related_name='video_likes', blank=True)
#     created = models.DateTimeField(auto_now_add=True, verbose_name='Дата')
#
#     def __str__(self):
#         return f"{self.profile.nickname} - {self.created}"
#
#     class Meta:
#         verbose_name = 'Видео'
#         verbose_name_plural = 'видео'


class Video(models.Model):
    VIDEO_TYPE_CHOICES = (
        ('local', 'Локальное видео'),
        ('url', 'Ссылка на видео'),
    )

    profile = models.ForeignKey('Profile', on_delete=models.CASCADE, related_name='videos')
    video_type = models.CharField(max_length=10, choices=VIDEO_TYPE_CHOICES, default='local', verbose_name='Тип видео')
    video = models.FileField(upload_to='videos/', verbose_name='Видео', blank=True, null=True)
    video_url = models.URLField(blank=True, null=True, verbose_name='Ссылка на видео')
    caption = models.TextField(blank=True, null=True, verbose_name='Подпись')
    likes = models.ManyToManyField(User, related_name='video_likes', blank=True)
    created = models.DateTimeField(auto_now_add=True, verbose_name='Дата')

    def __str__(self):
        return f"{self.profile.nickname} - {self.created}"

    class Meta:
        verbose_name = 'Видео'
        verbose_name_plural = 'видео'



class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, related_name='sent_messages')
    recipient = models.ForeignKey(Profile, on_delete=models.SET_NULL, blank=True, null=True,
                                  related_name='received_messages')
    name = models.CharField(max_length=200, blank=True, verbose_name='Имя')
    email = models.EmailField(max_length=200, blank=True, verbose_name='email')
    subject = models.CharField(max_length=200, blank=True, verbose_name='Тема')
    body = models.TextField(verbose_name='Сообщение')
    is_read = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.subject

    class Meta:
        ordering = ['is_read', '-created']
        verbose_name = 'Сообщения'
        verbose_name_plural = 'Сообщение'
