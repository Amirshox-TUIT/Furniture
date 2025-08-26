from django.urls import path
from .views import *

app_name = 'products'

urlpatterns = [
    path('cart/', product_cart, name='product_cart'),
    path('detail/', product_detail, name='product_detail'),
    path('checkout/', product_checkout, name='product_checkout'),
    path('grid_sidebar_left', product_grid_sidebar_left, name='product_grid_sidebar_left'),

]