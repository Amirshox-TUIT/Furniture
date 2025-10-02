from django import forms

from apps.products.models import ProductModel


class ProductModelForm(forms.ModelForm):
    class Meta:
        model = ProductModel
        exclude = ('sender', 'raiting')
