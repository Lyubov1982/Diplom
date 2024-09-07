# from django.db import models
# from django.contrib.auth.models import AbstractUser
#
# class CustomUser(AbstractUser):
#     ROLE_CHOICES = (
#         ('professional', 'Профи'),
#         ('newbie', 'Новичок'),
#         ('startup', 'Стартапер'),
#     )
#     role = models.CharField(max_length=20, choices=ROLE_CHOICES, blank=True, null=True)
#
# class UserProfile(models.Model):
#     user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
#     city = models.CharField(max_length=100, blank=True)
#     social_links = models.JSONField(default=dict)
#     articles = models.ManyToManyField('Article', blank=True)
#     photos = models.ManyToManyField('Photo', blank=True)
#     stories = models.ManyToManyField('Story', blank=True)
#
# class ProfiProfile(UserProfile):
#     diplomas = models.ManyToManyField('Diploma', blank=True)
#     gym = models.CharField(max_length=100, blank=True)
#
# class NoviceProfile(UserProfile):
#     pass
#
# class StartupProfile(UserProfile):
#     online_stores = models.ManyToManyField('OnlineStore', blank=True)
#     city_stores = models.ManyToManyField('CityStore', blank=True)
#
# # Другие модели, связанные с профилями пользователей
# class Article(models.Model):
#     # Поля модели
#     pass
#
# class Photo(models.Model):
#     # Поля модели
#     pass
#
# class Story(models.Model):
#     # Поля модели
#     pass
#
# class Diploma(models.Model):
#     # Поля модели
#     pass
#
# class OnlineStore(models.Model):
#     # Поля модели
#     pass
#
# class CityStore(models.Model):
#     # Поля модели
#     pass
