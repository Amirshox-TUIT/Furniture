from django.urls import path
from .views import *

app_name = 'products'

urlpatterns = [
    path('cart/', product_cart, name='cart'),
    path('detail/', product_detail, name='detail'),
    path('checkout/', product_checkout, name='checkout'),
    path('', products_view, name='products'),

]