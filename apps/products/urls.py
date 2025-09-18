from django.urls import path
from .views import *

app_name = 'products'

urlpatterns = [
    path('cart/', product_cart, name='cart'),
    path('detail/<int:pk>', ProductDetailView.as_view(), name='detail'),
    path('checkout/', product_checkout, name='checkout'),
    path('', ProductListView.as_view(), name='products'),
]