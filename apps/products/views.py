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
    sizes = ProductSize.objects.all()
    products = ProductModel.objects.all()
    subcategories = ProductCategory.objects.filter(sub__isnull=False)
    cat_id = request.GET.get('cat')
    brand_id = request.GET.get('brand_id')
    color_id = request.GET.get('color_id')
    size_id = request.GET.get('size_id')
    tag_id = request.GET.get('tag_id')
    q = request.GET.get('q')

    if cat_id:
        products = products.filter(categories=cat_id)

    if brand_id:
        products = products.filter(brand=brand_id)

    if color_id:
        products = products.filter(products_quantity__color=color_id)

    if size_id:
        products = products.filter(products_quantity__size=size_id)

    if tag_id:
        products = products.filter(products_quantity__size=tag_id)

    if q:
        products = products.filter(title__icontains=q)

    context = {
            "categories": categories,
            "brands": brands,
            "colors": colors,
            "sizes": sizes,
            "tags": ProductTag.objects.all(),
            "products": products,
            "subcategories": subcategories,
        }

    return render(request, "products/products.html", context)
