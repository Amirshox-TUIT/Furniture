from django import forms
from django.forms import inlineformset_factory
from .models import ProductModel, ProductImageModel, ProductQuantity


class ProductForm(forms.ModelForm):
    # Translation fieldlarni qo'lda qo'shamiz
    title_en = forms.CharField(max_length=100, required=False)
    title_uz = forms.CharField(max_length=100, required=False)
    short_description_en = forms.CharField(widget=forms.Textarea, required=False)
    short_description_uz = forms.CharField(widget=forms.Textarea, required=False)
    long_description_en = forms.CharField(widget=forms.Textarea, required=False)
    long_description_uz = forms.CharField(widget=forms.Textarea, required=False)

    class Meta:
        model = ProductModel
        fields = [
            'image',
            'image2',
            'categories',
            'brand',
            'price',
            'discount',
            'tag',
        ]

    def save(self, commit=True):
        instance = super().save(commit=False)

        # Translation fieldlarni qo'lda save qilamiz
        if hasattr(self, 'cleaned_data'):
            instance.title_en = self.cleaned_data.get('title_en', '')
            instance.title_uz = self.cleaned_data.get('title_uz', '')
            instance.short_description_en = self.cleaned_data.get('short_description_en', '')
            instance.short_description_uz = self.cleaned_data.get('short_description_uz', '')
            instance.long_description_en = self.cleaned_data.get('long_description_en', '')
            instance.long_description_uz = self.cleaned_data.get('long_description_uz', '')

        if commit:
            instance.save()
            self.save_m2m()

        return instance


class ProductImageForm(forms.ModelForm):
    class Meta:
        model = ProductImageModel
        fields = ['image']


class ProductQuantityForm(forms.ModelForm):
    class Meta:
        model = ProductQuantity
        fields = ['quantity', 'sizes', 'colors']


# Inline formsets
ProductImageFormSet = inlineformset_factory(
    ProductModel,
    ProductImageModel,
    form=ProductImageForm,
    extra=1,
    can_delete=True
)

ProductQuantityFormSet = inlineformset_factory(
    ProductModel,
    ProductQuantity,
    form=ProductQuantityForm,
    extra=1,
    can_delete=True
)