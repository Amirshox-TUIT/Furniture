from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class RegisterModelForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class LoginForm(forms.Form):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request", None)  # store request if passed
        super().__init__(*args, **kwargs)

    username = forms.CharField()
    password = forms.CharField()

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        context = self.get_context()
        credentials = {"username": username, "password": password}
        user = authenticate(request=context.get('request'), **credentials)
        if user is not None:
            self.cleaned_data['user'] = user
        else:
            raise forms.ValidationError("Username or password is incorrect")

        return super().clean()