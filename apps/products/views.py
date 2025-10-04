from django.views.generic import ListView, DetailView, CreateView, TemplateView, UpdateView
from .forms import ProductForm, ProductImageFormSet, ProductQuantityFormSet
from .models import *
from django.db import transaction
from apps.basket.cart import Basket
from apps.order.models import Order, OrderItem
from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.views.generic import DetailView
from django.db.models import Sum

from .models import ProductModel, ProductTag, ProductCategory, ProductQuantity

import uuid


class CartView(LoginRequiredMixin, TemplateView):
    template_name = 'products/product-cart.html'
    login_url = reverse_lazy('users:user_login')


class CheckoutView(LoginRequiredMixin, TemplateView):
    template_name = 'products/product-checkout.html'
    login_url = reverse_lazy('users:user_login')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['basket'] = Basket(self.request)
        return context

    def dispatch(self, request, *args, **kwargs):
        basket = Basket(request)
        if len(basket) == 0:
            messages.warning(request, 'Your basket is empty!')
            return redirect('products:cart')
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        basket = Basket(request)

        try:
            with transaction.atomic():
                shipping = request.POST.get('shipping_method')
                delivery_cost = 10 if shipping == 'express' else 0
                order = Order.objects.create(
                    user=request.user if request.user.is_authenticated else None,
                    unique_id=str(uuid.uuid4())[:10].upper(),
                    delivery=delivery_cost,
                    payment_method=request.POST.get('payment_method'),
                    shipping_method=shipping,
                    customer_name=request.POST.get('firstname'),
                    customer_email=request.POST.get('email'),
                    customer_phone=request.POST.get('phone'),
                    shipping_address=request.POST.get('address'),
                    shipping_city=request.POST.get('city'),
                    shipping_postal_code=request.POST.get('postal_code'),
                    shipping_country=request.POST.get('country'),
                )

                for item in basket:
                    OrderItem.objects.create(
                        order=order,
                        product=item['product'],
                        price=item['price'],

                        quantity=item['quantity'],
                        product_name=item['product'].title,
                        product_image=item['product'].image
                    )

                profile = request.user.profile
                profile.phone = request.POST.get('phone')
                profile.address = request.POST.get('address')
                profile.city = request.POST.get('city')
                profile.postal_code = request.POST.get('postal_code')
                profile.country = request.POST.get('country')
                profile.save()

                request.user.first_name = request.POST.get('firstname')
                request.user.email = request.POST.get('email')
                request.user.save()

                basket.clear()

                messages.success(request, f'Order #{order.unique_id} placed successfully!')
                return redirect('orders:success', order_id=order.unique_id)

        except Exception as e:
            messages.error(request, f'Error: {str(e)}')
            return redirect('products:checkout')


class OrderSuccessView(DetailView):
    model = Order
    template_name = 'order_success.html'
    context_object_name = 'order'
    slug_field = 'unique_id'
    slug_url_kwarg = 'order_id'

    def get_queryset(self):
        return Order.objects.prefetch_related('items__product')


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
        product = self.object
        context['tags'] = ProductTag.objects.all()
        context['categories'] = ProductCategory.objects.filter(sub__isnull=True)
        product_quantities = ProductQuantity.objects.filter(product=product)
        total_quantity = product_quantities.aggregate(
            total=Sum('quantity')
        )['total'] or 0

        available_sizes = set()
        available_colors = set()

        for pq in product_quantities:
            if pq.quantity > 0:
                available_sizes.update(pq.sizes.all())
                available_colors.update(pq.colors.all())

        context['total_quantity'] = total_quantity
        context['available_sizes'] = list(available_sizes)
        context['available_colors'] = list(available_colors)
        context['rproducts'] = ProductModel.objects.filter(
            categories__in=product.categories.all()
        ).exclude(id=product.id).distinct()[:6]

        context['bestsellers'] = ProductModel.objects.all().order_by('-discount')[:3]
        context['reviews'] = []
        context['reviews_count'] = 0

        return context




class ProductCreateView(CreateView):
    model = ProductModel
    form_class = ProductForm
    template_name = "products/product-add.html"
    success_url = reverse_lazy("products:products")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['brands'] = ProductBrand.objects.all()
        context['categories'] = ProductCategory.objects.all()
        context['tags'] = ProductTag.objects.all()
        context['sizes'] = ProductSize.objects.all()
        context['colors'] = ProductColor.objects.all()

        if self.request.POST:
            context["image_formset"] = ProductImageFormSet(
                self.request.POST,
                self.request.FILES,
                prefix="images"
            )
            context["quantity_formset"] = ProductQuantityFormSet(
                self.request.POST,
                prefix="quantities"
            )
        else:
            context["image_formset"] = ProductImageFormSet(prefix="images")
            context["quantity_formset"] = ProductQuantityFormSet(prefix="quantities")

        return context

    def post(self, request, *args, **kwargs):
        self.object = None

        form = self.get_form()

        mutable_post = request.POST.copy()
        mutable_post['title_en'] = request.POST.get('title_en', '')
        mutable_post['title_uz'] = request.POST.get('title_uz', '')
        mutable_post['short_description_en'] = request.POST.get('short_description_en', '')
        mutable_post['short_description_uz'] = request.POST.get('short_description_uz', '')
        mutable_post['long_description_en'] = request.POST.get('long_description_en', '')
        mutable_post['long_description_uz'] = request.POST.get('long_description_uz', '')

        # Update form data
        form.data = mutable_post

        # Get formsets
        image_formset = ProductImageFormSet(
            request.POST,
            request.FILES,
            prefix="images"
        )
        quantity_formset = ProductQuantityFormSet(
            request.POST,
            prefix="quantities"
        )

        # Validate
        if form.is_valid() and image_formset.is_valid() and quantity_formset.is_valid():
            self.object = form.save(commit=False)
            self.object.title_en = request.POST.get('title_en', '')
            self.object.title_uz = request.POST.get('title_uz', '')
            self.object.short_description_en = request.POST.get('short_description_en', '')
            self.object.short_description_uz = request.POST.get('short_description_uz', '')
            self.object.long_description_en = request.POST.get('long_description_en', '')
            self.object.long_description_uz = request.POST.get('long_description_uz', '')

            if request.user.is_authenticated:
                self.object.sender = request.user

            self.object.save()

            categories = request.POST.getlist('categories')
            self.object.categories.set(categories)

            tags = request.POST.getlist('tag')
            self.object.tag.set(tags)

            image_formset.instance = self.object
            image_formset.save()

            quantity_formset.instance = self.object
            quantity_formset.save()

            messages.success(request, 'Product created successfully!')
            return redirect(self.success_url)
        else:

            messages.error(request, 'Please correct the errors below.')
            return self.render_to_response(
                self.get_context_data(
                    form=form,
                    image_formset=image_formset,
                    quantity_formset=quantity_formset
                )
            )


def product_delete(request, pk):
    product = get_object_or_404(ProductModel, id=pk)
    if product.sender == request.user:
        product.status = ProductModel.Status.DELETED
        product.save()
        messages.success(request, 'Product deleted successfully!')
        return redirect('products:products')
    else:
        return redirect('pages:page_404')


