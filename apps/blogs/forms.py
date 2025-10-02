from django import forms
from apps.blogs.models import CommentsModel


class CommentsForm(forms.ModelForm):
    class Meta:
        model = CommentsModel
        fields = ['text']

from .models import BlogsModel


class BlogForm(forms.ModelForm):
    class Meta:
        model = BlogsModel
        fields = ['title', 'description', 'author', 'image', 'category', 'tag']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter blog title'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control ckeditor-textarea',
                'id': 'id_description'
            }),
            'author': forms.Select(attrs={
                'class': 'form-control'
            }),
            'image': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            }),
            'category': forms.SelectMultiple(attrs={
                'class': 'form-control',
                'style': 'min-height: 100px;'
            }),
            'tag': forms.SelectMultiple(attrs={
                'class': 'form-control',
                'style': 'min-height: 100px;'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Category va Tag ni optional qilish
        self.fields['category'].required = False
        self.fields['tag'].required = False

    def clean_image(self):
        image = self.cleaned_data.get('image')
        if image:
            # Rasm hajmini tekshirish
            if image.size > 5 * 1024 * 1024:  # 5MB
                raise forms.ValidationError('Rasm hajmi 5MB dan kichik bo\'lishi kerak!')
        return image