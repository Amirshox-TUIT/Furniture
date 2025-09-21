from django.urls import path

from apps.basket.views import basket_detail, basket_add, basket_remove, basket_update

app_name = 'basket'

urlpatterns = [
    path('', basket_detail, name='detail'),
    path('add/<int:product_id>/', basket_add, name='basket_add'),
    path('remove/<int:product_id>/', basket_remove, name='basket_remove'),
    path('update/<int:product_id>/', basket_update, name='basket_update'),
]