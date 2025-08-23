from django.shortcuts import render


def page_404(request):
    return render(request, 'pages/404.html')


def about_us(request):
    return render(request, 'pages/about-us.html')


def contact(request):
    return render(request, 'pages/contact.html')


def home3(request):
    return render(request, 'pages/home3.html')
