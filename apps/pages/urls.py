from django.urls import path
from . import views

app_name = 'pages'

urlpatterns = [
    path('404/', views.page_404, name='page_404'),
    path('about-us/', views.AboutView.as_view(), name='about_us'),
    path('contact/', views.ContactView.as_view(), name='contact'),
    path('', views.HomeView.as_view(), name='home3'),
]
