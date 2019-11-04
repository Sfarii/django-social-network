from django import forms
from django.utils.translation import ugettext_lazy as _
from .models import Post, Comment


class PostFrom(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('cover', 'title', 'status', 'body')


class CommentFrom(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('body', )
        labels = {
            'body': _('Add a public comment...')
        }