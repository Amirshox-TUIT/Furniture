from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, TemplateView

from .forms import ProductModelForm
from .models import *


class CartView(LoginRequiredMixin, TemplateView):
    template_name = 'products/product-cart.html'
    login_url = reverse_lazy('users:user_login')



def product_checkout(request):
    return render(request, 'products/product-checkout.html')

class ProductListView(LoginRequiredMixin, ListView):
    template_name = 'products/products.html'
    context_object_name = 'products'
    login_url = reverse_lazy('users:user_login')
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
        if self.request.GET.get('cat'):
            context['cat_id'] = int(self.request.GET.get('cat'))
        if self.request.GET.get('brand'):
            context['brand_id'] = int(self.request.GET.get('brand'))
        if self.request.GET.get('color'):
            context['color_id'] = int(self.request.GET.get('color'))
        if self.request.GET.get('tag'):
            context['tag_id'] = int(self.request.GET.get('tag'))
        return context


class ProductDetailView(LoginRequiredMixin, DetailView):
    template_name = 'products/product-detail.html'
    context_object_name = 'product'
    queryset = ProductModel.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tags = ProductTag.objects.all()
        categories = ProductCategory.objects.filter(sub__isnull=True)
        pk = self.kwargs['pk']
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


class ProductCreateView(LoginRequiredMixin, CreateView):
    template_name = 'products/product-add.html'
    form_class = ProductModelForm

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.sender = self.request.user
        instance.save()
        messages.success(self.request, 'Product Added successfully')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Product Not Added')
        return super().form_invalid(form)

    def get_success_url(self):
        return reverse_lazy('products:products')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        brands = ProductBrand.objects.all()
        categories = ProductCategory.objects.all()
        tags = ProductTag.objects.all()
        if brands:
            context['brands'] = brands
        if categories:
            context['categories'] = categories
        if tags:
            context['tags'] = tags

        return context



