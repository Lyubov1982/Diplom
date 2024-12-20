# Generated by Django 5.0.6 on 2024-11-28 12:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_message'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='body',
            field=models.TextField(verbose_name='Сообщение'),
        ),
        migrations.AlterField(
            model_name='message',
            name='email',
            field=models.EmailField(blank=True, max_length=200, verbose_name='email'),
        ),
        migrations.AlterField(
            model_name='message',
            name='name',
            field=models.CharField(blank=True, max_length=200, verbose_name='Имя'),
        ),
        migrations.AlterField(
            model_name='message',
            name='subject',
            field=models.CharField(blank=True, max_length=200, verbose_name='Тема'),
        ),
    ]
