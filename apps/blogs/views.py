from django.shortcuts import render
from .models import *

def blog_detail(request, pk):
    try:
        blog = BlogsModel.objects.get(id=pk)
    except BlogsModel.DoesNotExist:
        return render(request, 'pages/404.html')

    related_blogs = BlogsModel.objects.filter(
        category__in=blog.category.all()
    ).exclude(id=blog.id).distinct()

    context = {
        "blog": blog,
        "related_blogs": related_blogs,
    }
    return render(request, 'blogs/blog-detail.html', context)

def blog_list_sidebar_left(request):
    blogs = BlogsModel.objects.all()
    context = {
        'blogs': blogs,
    }
    return render(request, 'blogs/blog-list-sidebar-left.html', context)
