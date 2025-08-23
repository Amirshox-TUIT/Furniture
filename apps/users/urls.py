from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('account/', views.user_account, name='user_account'),
    path('login/', views.user_login, name='user_login'),
    path('register/', views.user_register, name='user_register'),
    path('reset-password/', views.user_reset_password, name='user_reset_password'),
    path('wishlist/', views.user_wishlist, name='user_wishlist'),
]
