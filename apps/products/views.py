from django.shortcuts import render
from .models import *

def product_cart(request):
    return render(request, 'products/product-cart.html')

def product_checkout(request):
    return render(request, 'products/product-checkout.html')

def product_detail(request):
    return render(request, 'products/product-detail.html')

def products_view(request):
    categories = ProductCategory.objects.filter(sub__isnull=True)
    brands = ProductBrand.objects.all()
    colors = ProductColor.objects.all()
    products = ProductModel.objects.all()
    subcategories = ProductCategory.objects.filter(sub__isnull=False)
    cat_id = request.GET.get('cat')
    brand_id = request.GET.get('brand')
    color_id = request.GET.get('color')
    tag_id = request.GET.get('tag')
    s = request.GET.get('s')

    if cat_id:
        products = products.filter(categories=cat_id)

    if brand_id:
        products = products.filter(brand=brand_id)

    if color_id:
        products = products.filter(products_quantity__colors=color_id)

    if tag_id:
        products = products.filter(tag=tag_id)

    if s:
        products = products.filter(title__icontains=s)

    context = {
            "categories": categories,
            "brands": brands,
            "colors": colors,
            "tags": ProductTag.objects.all(),
            "products": products,
            "subcategories": subcategories,
        }

    return render(request, "products/products.html", context)
