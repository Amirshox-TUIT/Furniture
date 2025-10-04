from django.urls import path
from .views import *

app_name = 'products'

urlpatterns = [
    path('cart/', CartView.as_view(), name='cart'),
    path('detail/<int:pk>', ProductDetailView.as_view(), name='detail'),
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('', ProductListView.as_view(), name='products'),
    path('add/', ProductCreateView.as_view(), name='add'),
    path('delete/<int:pk>', product_delete, name='delete'),
]