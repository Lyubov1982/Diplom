# Generated by Django 5.0.6 on 2024-11-24 06:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0006_project_likes'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='project',
            name='vote_ratio',
        ),
        migrations.RemoveField(
            model_name='project',
            name='vote_total',
        ),
    ]
