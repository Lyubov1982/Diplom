# Generated by Django 5.0.6 on 2024-11-03 12:40

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=200, verbose_name='Имя')),
                ('email', models.EmailField(blank=True, max_length=200, verbose_name='Эл.адрес')),
                ('nickname', models.CharField(blank=True, max_length=200, verbose_name='Псевдоним')),
                ('myself', models.TextField(blank=True, verbose_name='О себе')),
                ('photo', models.ImageField(default='profiles/coach.jpg', upload_to='profiles/', verbose_name='Фото')),
                ('social_youtube', models.CharField(blank=True, max_length=200, verbose_name='Youtube')),
                ('social_site', models.CharField(blank=True, max_length=200, verbose_name='Социальная сеть')),
                ('social_website', models.CharField(blank=True, max_length=200, verbose_name='Сайт')),
                ('document', models.FileField(null=True, upload_to='documents/', verbose_name='Документ об образовании')),
                ('work', models.CharField(blank=True, max_length=200, verbose_name='Место работы')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Дата')),
                ('user', models.OneToOneField(blank=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Профиль',
                'verbose_name_plural': 'профили',
            },
        ),
        migrations.CreateModel(
            name='Skill',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('qualification', models.CharField(blank=True, max_length=200, verbose_name='Квалификация')),
                ('info', models.TextField(blank=True, verbose_name='Описание')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Дата')),
                ('expert', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='users.profile', verbose_name='Эксперт')),
            ],
            options={
                'verbose_name': 'Квалификация',
                'verbose_name_plural': 'квалификации',
            },
        ),
    ]