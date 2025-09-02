from django.urls import path
from . import views

app_name = 'blogs'

urlpatterns = [
    path('detail/<int:pk>', views.blog_detail, name='detail'),
    path('list-sidebar-left/', views.blog_list_sidebar_left, name='list_sidebar_left'),
]
