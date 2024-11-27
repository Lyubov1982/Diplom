from django.db.models.signals import post_save, post_delete
from .models import Profile
from django.contrib.auth.models import User
from django.dispatch import receiver



@receiver(post_delete, sender=Profile)
def delete_user(sender, instance, **kwargs):
    user = instance.user
    user.delete()


def update_user(sender, instance, created, **kwargs):
    profile = instance
    user = profile.user

    if created is False:
        user.first_name = profile.name.split()[0]  # Предполагаем, что имя и фамилия разделены пробелом
        user.last_name = profile.name.split()[1] if len(profile.name.split()) > 1 else ''
        user.email = profile.email
        user.username = profile.nickname
        user.save()


# post_save.connect(create_profile, sender=User)
post_delete.connect(delete_user, sender=Profile)
post_save.connect(update_user, sender=Profile)
