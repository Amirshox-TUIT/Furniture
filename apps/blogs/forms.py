from django import forms
from apps.blogs.models import CommentsModel


class CommentsForm(forms.ModelForm):
    class Meta:
        model = CommentsModel
        exclude = ['created_at', 'updated_at', 'blog']
