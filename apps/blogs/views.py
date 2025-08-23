from django.shortcuts import render

def blog_detail(request):
    return render(request, 'blogs/blog-detail.html')

def blog_list_sidebar_left(request):
    return render(request, 'blogs/blog-list-sidebar-left.html')
