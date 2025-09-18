from django.urls import path
from . import views

app_name = 'blogs'

urlpatterns = [
    path('detail/<int:pk>', views.BlogDetailView.as_view(), name='detail'),
    path('', views.BlogListView.as_view(), name='list_sidebar_left'),
]
