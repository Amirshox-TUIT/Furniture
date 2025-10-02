from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from apps.users.models import ProfileModel


class RegisterModelForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_active = False
        if commit:
            user.save()
        return user

class LoginForm(forms.Form):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request", None)  # store request if passed
        super().__init__(*args, **kwargs)

    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        credentials = {"username": username, "password": password}
        user = authenticate(request=self.request, **credentials)
        if user is not None:
            self.cleaned_data['user'] = user
        else:
            raise forms.ValidationError("Username or password is incorrect")

        return super().clean()


class ProfileModelForm(forms.ModelForm):
    username = forms.CharField(max_length=150)

    class Meta:
        model = ProfileModel
        exclude = ['user']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['username'].initial = user.username

    def save(self, commit=True):
        profile = super().save(commit=False)
        if commit:
            profile.save()
            user = profile.user
            user.username = self.cleaned_data['username']
            user.save()
        return profile
