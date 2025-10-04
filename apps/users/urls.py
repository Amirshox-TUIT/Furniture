from django.urls import path
from . import views
from .views import ConfirmEmailView, UpdateAvatarView

app_name = 'users'

urlpatterns = [
    path('account/<int:pk>', views.ProfileView.as_view(), name='user_account'),
    path('login/', views.LoginFormView.as_view(), name='user_login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('register/', views.RegisterCreateView.as_view(), name='user_register'),
    path('reset-password/', views.user_reset_password, name='user_reset_password'),
    path('wishlist/', views.user_wishlist, name='user_wishlist'),
    path('update-avatar/<int:pk>/', UpdateAvatarView.as_view(), name='update_avatar'),
]
