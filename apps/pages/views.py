from django.shortcuts import render, redirect
from django.contrib import messages
from apps.pages.forms import ContactForm
from apps.pages.models import AboutModel


def page_404(request):
    return render(request, 'pages/404.html')


def about_us(request):
    admins = AboutModel.objects.all()
    return render(request, 'pages/about-us.html', {'admins': admins})


def contact_view(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Ваше сообщение успешно отправлено!")
            return redirect("pages:contact")
        else:
            messages.error(request, "Исправьте ошибки в форме и попробуйте снова.")
    else:
        form = ContactForm()
    return render(request, "pages/contact.html", {"form": form})

def home3(request):
    return render(request, 'pages/home3.html')
