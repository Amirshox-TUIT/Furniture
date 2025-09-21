from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404

from apps.basket.cart import Basket
from apps.products.models import ProductModel, ProductColor, ProductSize


def basket_detail(request):
    """
    Display the basket contents.
    """
    basket = Basket(request)
    return render(request, 'products/product-cart.html', {'basket': basket})


def basket_add(request, product_id):
    """
    Add a product to the basket.
    """
    basket = Basket(request)
    product = get_object_or_404(ProductModel, id=product_id)

    color = ProductColor.objects.filter(products_quantity__product=product).first()
    size = ProductSize.objects.filter(products_quantity__product=product).first()
    basket.add(product=product, quantity=1, color=color, size=size)
    messages.success(request, f'{product.title} added to your basket!')
    return redirect('products:products')


def basket_remove(request, product_id):
    """
    Remove a product from the basket.
    """
    basket = Basket(request)
    product = get_object_or_404(ProductModel, id=product_id)
    basket.remove(product)
    messages.success(request, f'{product.title} removed from your basket!')
    return redirect('products:products')

def basket_update(request, product_id):
    basket = Basket(request)
    product = get_object_or_404(ProductModel, id=product_id)
    quantity = int(request.POST.get('qty'))
    color = ProductColor.objects.filter(products_quantity__product=product).first()
    size = ProductSize.objects.filter(products_quantity__product=product).first()
    basket.add(product=product, quantity=quantity, color=color, size=size, override_quantity=True)
    messages.success(request, f'{product.title} updated from your basket!')
    return redirect('products:cart')