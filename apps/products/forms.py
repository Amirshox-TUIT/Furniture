from django import forms
from django.forms import inlineformset_factory
from .models import ProductModel, ProductImageModel, ProductQuantity


class ProductForm(forms.ModelForm):
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


class CheckoutForm(forms.Form):
    firstname = forms.CharField(max_length=100, required=True)
    email = forms.EmailField(required=True)
    phone = forms.CharField(max_length=128, required=True)
    address = forms.CharField(max_length=255, required=True)
    city = forms.CharField(max_length=128, required=True)
    postal_code = forms.CharField(max_length=15, required=True)
    country = forms.CharField(max_length=128, required=True)
    shipping_method = forms.ChoiceField(
        choices=[
            ('standard', 'Standard Delivery'),
            ('express', 'Express Delivery')
        ],
        required=True
    )
    payment_method = forms.ChoiceField(
        choices=[
            ('card', 'Pay by Card'),
            ('cash', 'Cash on Delivery')
        ],
        required=True
    )
    terms = forms.BooleanField(required=True)
    optin = forms.BooleanField(required=False)
    newsletter = forms.BooleanField(required=False)
