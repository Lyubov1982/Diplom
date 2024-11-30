from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile, Skill
from django.forms import ModelForm
from .models import Photo, Video, Message


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['nickname', '' 'myself', 'myself_short', 'photo', 'social_youtube',
                  'social_site', 'social_website', 'document', 'work']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs.update({'class': 'input'})


class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True, label='Имя')
    last_name = forms.CharField(max_length=30, required=True, label='Фамилия')

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']
        labels = {'username': "Логин"}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs.update({'class': 'input'})


class SkillForm(forms.ModelForm):
    class Meta:
        model = Skill
        fields = ['qualification', 'info']
        labels = {'qualification': "Квалификация", 'info': "Опыт"}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs.update({'class': 'input'})


class PhotoForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = ['image', 'caption']

    def __init__(self, *args, **kwargs):
        super(PhotoForm, self).__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs.update({'class': 'input'})


# class VideoForm(forms.ModelForm):
#     class Meta:
#         model = Video
#         fields = ['video', 'caption']
#
#     def __init__(self, *args, **kwargs):
#         super(VideoForm, self).__init__(*args, **kwargs)
#
#         for field in self.fields.values():
#             field.widget.attrs.update({'class': 'input'})


class VideoForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = ['video_type', 'video', 'video_url', 'caption']
        widgets = {
            'video_type': forms.RadioSelect(attrs={'class': 'input'}),
            'video': forms.FileInput(attrs={'class': 'input'}),
            'video_url': forms.URLInput(attrs={'class': 'input'}),
            'caption': forms.Textarea(attrs={'class': 'input'}),
        }

    def __init__(self, *args, **kwargs):
        super(VideoForm, self).__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs.update({'class': 'input'})

    def clean(self):
        cleaned_data = super().clean()
        video_type = cleaned_data.get('video_type')
        video = cleaned_data.get('video')
        video_url = cleaned_data.get('video_url')

        if video_type == 'local' and not video:
            self.add_error('video', 'Пожалуйста, загрузите видео файл.')
        elif video_type == 'url' and not video_url:
            self.add_error('video_url', 'Пожалуйста, введите ссылку на видео.')

        return cleaned_data



class MessageForm(ModelForm):
    class Meta:
        model = Message
        fields = ['name', 'email', 'subject', 'body']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs.update({'class': 'input'})
