# from django.db.models.signals import post_save
# from django.dispatch import receiver
# # from .models import CustomUser, UserProfile, ProfiProfile, NoviceProfile, StartupProfile
#
# @receiver(post_save, sender=CustomUser)
# def create_user_profile(sender, instance, created, **kwargs):
#     if created:
#         if instance.role == 'professional':
#             ProfiProfile.objects.create(user=instance)
#         elif instance.role == 'newbie':
#             NoviceProfile.objects.create(user=instance)
#         elif instance.role == 'startup':
#             StartupProfile.objects.create(user=instance)
#         else:
#             UserProfile.objects.create(user=instance)
#
# @receiver(post_save, sender=CustomUser)
# def save_user_profile(sender, instance, **kwargs):
#     if hasattr(instance, 'profiprofile') and instance.role == 'professional':
#         instance.profiprofile.save()
#     elif hasattr(instance, 'noviceprofile') and instance.role == 'newbie':
#         instance.noviceprofile.save()
#     elif hasattr(instance, 'startupprofile') and instance.role == 'startup':
#         instance.startupprofile.save()
#     elif hasattr(instance, 'userprofile'):
#         instance.userprofile.save()