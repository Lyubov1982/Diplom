from django.forms import ModelForm
from django import forms
from .models import Project, Tag, UsefulLink, Comment, Section
from .widgets import ScrollableCheckboxSelectMultiple


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = [
            'sections', 'tags', 'title', 'description', 'demo_link',
            'source_link', 'featured_image',
        ]
        widgets = {
            'sections': ScrollableCheckboxSelectMultiple(),
            'tags': ScrollableCheckboxSelectMultiple(),
        }

    def __init__(self, *args, **kwargs):
        super(ProjectForm, self).__init__(*args, **kwargs)
        self.fields['tags'].queryset = Tag.objects.all()
        self.fields['sections'].queryset = Section.objects.all()

        for field in self.fields.values():
            field.widget.attrs.update({'class': 'input'})

class TagForm(ModelForm):
    class Meta:
        model = Tag
        fields = ['name']

    def __init__(self, *args, **kwargs):
        super(TagForm, self).__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs.update({'class': 'input'})


class UsefulLinkForm(forms.ModelForm):
    class Meta:
        model = UsefulLink
        fields = ['title', 'url']

    def __init__(self, *args, **kwargs):
        super(UsefulLinkForm, self).__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs.update({'class': 'input'})


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(
                attrs={'class': 'input input--textarea',
                       'placeholder': 'Вы можете здесь оставить свой комментарий ...'}),
        }

    def __init__(self, *args, **kwargs):
        super(CommentForm, self).__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs.update({'class': 'input'})
