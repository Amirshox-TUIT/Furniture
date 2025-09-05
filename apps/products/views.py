from django.shortcuts import render
from .models import *

def product_cart(request):
    return render(request, 'products/product-cart.html')

def product_checkout(request):
    return render(request, 'products/product-checkout.html')

def product_detail(request):
    return render(request, 'products/product-detail.html')

def products_view(request):
    products = ProductModel.objects.all()

    for product in products:
        product.rating_percent = product.raiting * 20

    categories = ProductCategory.objects.filter(sub__isnull=True)


    context = {
        "categories": categories,
        "brands": ProductBrand.objects.all(),
        "colors": ProductColor.objects.all(),
        "sizes": ProductSize.objects.all(),
        "tags": ProductTag.objects.all(),
        "products": products,
    }
    return render(request, "products/products.html", context)
