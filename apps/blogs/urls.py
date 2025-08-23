from django.urls import path
from . import views

app_name = 'blogs'

urlpatterns = [
    path('detail/', views.blog_detail, name='blog_detail'),
    path('list-sidebar-left/', views.blog_list_sidebar_left, name='blog_list_sidebar_left'),
]
