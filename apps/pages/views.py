from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView

from apps.pages.forms import ContactForm
from apps.pages.models import AboutModel
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
        messages.success(self.request, "Ваше сообщение успешно отправлено!")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Исправьте ошибки в форме и попробуйте снова.')
        return super().form_invalid(form)

class HomeView(ListView):
    template_name = 'pages/home3.html'
    context_object_name = 'home'
    queryset = living_prs = ProductModel.objects.filter(categories__sub__title="Living Room").distinct()

    def get_queryset(self):
        living_prs = ProductModel.objects.filter(categories__sub__title="Living Room").distinct()
        return living_prs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        living_prs = ProductModel.objects.filter(categories__sub__title="Living Room").distinct()
        bathroom_prs = ProductModel.objects.filter(categories__sub__title="Bathroom").distinct()
        context['living_prs'] = living_prs
        context['bathroom_prs'] = bathroom_prs
        return context
