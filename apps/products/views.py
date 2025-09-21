from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from apps.blogs.utils import get_pk
from .models import *


def product_cart(request):
    return render(request, 'products/product-cart.html')

def product_checkout(request):
    return render(request, 'products/product-checkout.html')

class ProductListView(ListView):
    template_name = 'products/products.html'
    context_object_name = 'products'
    paginate_by = 2

    def get_queryset(self):
        products = ProductModel.objects.all()
        cat_id = self.request.GET.get('cat')
        brand_id = self.request.GET.get('brand')
        color_id = self.request.GET.get('color')
        tag_id = self.request.GET.get('tag')
        s = self.request.GET.get('s')

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

        return products

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tags = ProductTag.objects.all()
        categories = ProductCategory.objects.filter(sub__isnull=True)
        brands = ProductBrand.objects.all()
        colors = ProductColor.objects.all()
        subcategories = ProductCategory.objects.filter(sub__isnull=False)

        context['products'] = context['products']
        context['categories'] = categories
        context['brands'] = brands
        context['colors'] = colors
        context['subcategories'] = subcategories
        context['tags'] = tags
        return context


class ProductDetailView(DetailView):
    template_name = 'products/product-detail.html'
    context_object_name = 'product'
    queryset = ProductModel.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = get_pk(self.request)
        tags = ProductTag.objects.all()
        categories = ProductCategory.objects.filter(sub__isnull=True)
        product = get_object_or_404(ProductModel, id=pk)

        item = ProductQuantity.objects.get(product=pk)
        rproducts = ProductModel.objects.filter(
            categories__in=product.categories.all()
        ).exclude(id=pk).distinct()

        context['rproducts'] = rproducts
        context['product'] = product
        context['tags'] = tags
        context['categories'] = categories
        context['quantity'] = item.quantity
        return context

