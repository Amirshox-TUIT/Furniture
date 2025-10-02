from django.urls import path
from . import views
from .views import blog_delete

app_name = 'blogs'

urlpatterns = [
    path('detail/<int:pk>', views.BlogDetailView.as_view(), name='detail'),
    path('', views.BlogListView.as_view(), name='list_sidebar_left'),
    path('add/', views.BlogCreateView.as_view(), name='add'),
    path('delete/<int:pk>/', blog_delete, name='delete'),

]
