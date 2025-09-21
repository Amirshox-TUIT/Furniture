import threading

from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.utils.http import urlsafe_base64_decode
from django.views import View
from django.views.generic import CreateView, FormView

from apps.users.forms import RegisterModelForm, LoginForm
from apps.users.utils import send_email_confirmation


class RegisterCreateView(CreateView):
    template_name = 'users/user-register.html'
    form_class = RegisterModelForm
    success_url = reverse_lazy('pages:home3')

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False
        user.save()

        email_thread = threading.Thread(target=send_email_confirmation, args=(user, self.request,))
        email_thread.start()

        message = "We sent a mail to your email, please verify it!"
        messages.error(request=self.request, message=message)
        return super().form_valid(form)

    def form_invalid(self, form):
        for key, value in form.errors.items():
            for error in value:
                messages.error(request=self.request, message=error)
        return super().form_invalid(form)


class LoginFormView(FormView):
    template_name = 'users/user-login.html'
    form_class = LoginForm
    success_url = reverse_lazy('pages:home')

    def get_form_kwargs(self):
        """Pass request into the form"""
        kwargs = super().get_form_kwargs()
        kwargs["request"] = self.request
        return kwargs

    def form_valid(self, form):
        """Login the user after validation"""
        user = form.cleaned_data.get("user")
        if user:
            login(self.request, user)
        return super().form_valid(form)

    def form_invalid(self, form):
        for key, value in form.errors.items():
            for error in value:
                messages.error(request=self.request, message=error)
        return super().form_invalid(form)


class ConfirmEmailView(View):
    @staticmethod
    def get(request, uidb64, token):
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(pk=uid)
        except (User.DoesNotExist, ValueError, TypeError, OverflowError):
            messages.error(request, "User not found")
            return redirect('users:user_login')

        if default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            messages.success(request, "Your email address is verified!")
            return redirect('users:user_login')
        else:
            messages.error(request, "Link is not correct")
            return redirect('users:user_register')

def user_wishlist(request):
    return render(request, 'users/user-wishlist.html')

def user_reset_password(request):
    return render(request, 'users/user-reset-password.html')

def user_account(request):
    return render(request, 'users/user-acount.html')