from django.urls import path
from . import views
from .views import ConfirmEmailView

app_name = 'users'

urlpatterns = [
    # path('account/', views.user_account, name='user_account'),
    path('login/', views.LoginFormView.as_view(), name='user_login'),
    path('register/', views.RegisterCreateView.as_view(), name='user_register'),
    path('confirmation/<uidb64>/<token>/', ConfirmEmailView.as_view(), name='confirmation'),
    path('reset-password/', views.user_reset_password, name='user_reset_password'),
    path('wishlist/', views.user_wishlist, name='user_wishlist'),
    path('account/', views.user_account, name='user_account'),
]
