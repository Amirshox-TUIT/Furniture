import threading

from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse_lazy
from django.utils.http import urlsafe_base64_decode
from django.views import View
from django.views.generic import CreateView, FormView, UpdateView, DetailView

from apps.blogs.models import BlogsModel
from apps.users.forms import RegisterModelForm, LoginForm, ProfileModelForm
from apps.users.models import ProfileModel
from apps.users.tokens import email_verification_token
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
        messages.warning(request=self.request, message=message)
        return super().form_valid(form)

    def form_invalid(self, form):
        for key, value in form.errors.items():
            for error in value:
                messages.error(request=self.request, message=error)
        return super().form_invalid(form)


class LoginFormView(FormView):
    template_name = 'users/user-login.html'
    form_class = LoginForm
    success_url = reverse_lazy('pages:home3')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["request"] = self.request
        return kwargs

    def form_valid(self, form):
        user = form.cleaned_data.get("user")
        if user:
            if not user.is_active:
                messages.error(self.request, "Please verify your email first!")
                return redirect('users:user_login')
            login(self.request, user)
        return super().form_valid(form)

    def form_invalid(self, form):
        for key, value in form.errors.items():
            for error in value:
                messages.error(self.request, error)
        return super().form_invalid(form)


class ConfirmEmailView(View):
    def get(self, request, uidb64, token):
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(pk=uid)
            print(f"User found: {user.username}, is_active: {user.is_active}")
            print(f"Token received: {token}")
        except (User.DoesNotExist, ValueError, TypeError, OverflowError) as e:
            print(f"Error decoding: {e}")
            messages.error(request, "User not found")
            return redirect('users:user_login')

        if user.is_active:
            messages.info(request, "Your email is already verified!")
            return redirect('users:user_login')

        is_valid = email_verification_token.check_token(user, token)

        if is_valid:
            user.is_active = True
            user.save(update_fields=['is_active'])
            messages.success(request, "Your email address has been verified!")
            return redirect('users:user_login')
        else:
            messages.error(request, "Invalid or expired confirmation link. Please register again.")
            return redirect('users:user_register')


class LogoutView(View):
    def get(self, request):
        logout(request)
        messages.success(request, "You have been logged out successfully!")
        return redirect('pages:home3')

    def post(self, request):
        logout(request)
        messages.success(request, "You have been logged out successfully!")
        return redirect('pages:home3')

def user_wishlist(request):
    context = {
        'blogs':BlogsModel.objects.all(),
    }
    return render(request, 'users/user-wishlist.html', context=context)

def user_reset_password(request):
    return render(request, 'users/user-reset-password.html')

class ProfileView(LoginRequiredMixin, UpdateView):
    template_name = 'users/user-acount.html'
    form_class = ProfileModelForm
    context_object_name = 'profile'
    login_url = reverse_lazy('users:user_login')

    def get_object(self, queryset=None):
        user = get_object_or_404(User, id=self.kwargs.get('pk'))
        profile, created = ProfileModel.objects.get_or_create(user=user)
        return profile

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.get_object().user
        return kwargs

    def get_success_url(self):
        return reverse_lazy('users:user_account', kwargs={'pk': self.kwargs['pk']})

    def form_valid(self, form):
        messages.success(self.request, "Your profile has been updated!")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Failed to update your profile!")
        return super().form_invalid(form)

