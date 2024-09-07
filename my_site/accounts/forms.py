# from django import forms
# from django.contrib.auth.forms import UserCreationForm
# from .models import CustomUser
# from .models import ProfiProfile, NoviceProfile, StartupProfile
#
# class RegistrationForm(UserCreationForm):
#     email = forms.EmailField(required=True)
#
#     class Meta:
#         model = CustomUser
#         fields = ('username', 'email', 'password1', 'password2', 'role')
#
# class ProfiProfileForm(forms.ModelForm):
#     class Meta:
#         model = ProfiProfile
#         fields = ['city', 'social_links', 'articles', 'photos', 'stories', 'diplomas', 'gym']
#
# class NoviceProfileForm(forms.ModelForm):
#     class Meta:
#         model = NoviceProfile
#         fields = ['city', 'social_links', 'articles', 'photos', 'stories']
#
# class StartupProfileForm(forms.ModelForm):
#     class Meta:
#         model = StartupProfile
#         fields = ['city', 'social_links', 'articles', 'photos', 'stories', 'online_stores', 'city_stores']