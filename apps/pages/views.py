from django.db.models import Max, Q
from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, TemplateView

from apps.pages.forms import ContactForm
from apps.pages.models import AboutModel, BannerModel
from apps.products.models import ProductModel


def page_404(request):
    return render(request, 'pages/404.html')

class AboutView(ListView):
    template_name = 'pages/about-us.html'
    context_object_name = 'about'
    queryset = AboutModel.objects.all()

    def get_queryset(self):
        queryset = AboutModel.objects.all()
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        admins = AboutModel.objects.all()
        context['admins'] = admins
        return context


class ContactView(CreateView):
    template_name = 'pages/contact.html'
    form_class = ContactForm
    success_url = reverse_lazy('pages:contact')

    def form_valid(self, form):
        form.save()
        messages.success(self.request, "Your message has been successfully sent.")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Please correct the errors in the form and try again.')
        return super().form_invalid(form)


class HomeView(TemplateView):
    template_name = 'pages/home3.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        big_sales = ProductModel.objects.order_by('-discount')[:3]

        banners = BannerModel.objects.filter(title__isnull=False)
        sub_banners = BannerModel.objects.filter(title__isnull=True)

        new_living_prs = ProductModel.objects.filter(
            Q(categories__title="Living Room") | Q(categories__sub__title="Living Room")
        ).distinct().order_by('-created_at')[:3]

        new_bathroom_prs = ProductModel.objects.filter(
            Q(categories__title="Bathroom") | Q(categories__sub__title="Bathroom")
        ).distinct().order_by('-created_at')[:3]

        sales_living_prs = ProductModel.objects.filter(
            Q(categories__title="Living Room") | Q(categories__sub__title="Living Room")
        ).distinct().order_by('-discount')[:3]

        sales_bathroom_prs = ProductModel.objects.filter(
            Q(categories__title="Bathroom") | Q(categories__sub__title="Bathroom")
        ).distinct().order_by('-discount')[:3]

        about = AboutModel.objects.all()

        context['new_living_prs'] = new_living_prs
        context['new_bathroom_prs'] = new_bathroom_prs
        context['sales_living_prs'] = sales_living_prs
        context['sales_bathroom_prs'] = sales_bathroom_prs
        context['about'] = about
        context['big_sales'] = big_sales
        context['banners'] = banners
        context['sub_banners'] = sub_banners

        return context

