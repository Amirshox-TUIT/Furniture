from django.urls import path
from . import views

app_name = 'pages'

urlpatterns = [
    path('404/', views.page_404, name='page_404'),
    path('about-us/', views.about_us, name='about_us'),
    path('contact/', views.contact_view, name='contact'),
    path('', views.home3, name='home3'),
]
