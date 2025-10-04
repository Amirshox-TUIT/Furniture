from django.urls import path

from apps.products.views import OrderSuccessView

app_name = 'orders'

urlpatterns = [
    path('success/<str:order_id>/', OrderSuccessView.as_view(), name='success'),
]