from django.shortcuts import render, redirect

from .forms import CommentsForm
from .models import *

def blog_detail(request, pk):
    if request.method == "POST":
        form = CommentsForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.blog_id = pk
            instance.save()
            return redirect("blogs:detail", pk=pk)
    else:
        try:
            blog = BlogsModel.objects.get(id=pk)
        except BlogsModel.DoesNotExist:
            return render(request, 'pages/404.html')

        related_blogs = BlogsModel.objects.filter(
            category__in=blog.category.all()
        ).exclude(id=blog.id).distinct()
        comments = CommentsModel.objects.filter(blog=pk)

        context = {
            "blog": blog,
            "related_blogs": related_blogs,
            "comments": comments,
        }
        return render(request, 'blogs/blog-detail.html', context)

def blog_list_sidebar_left(request):
    blogs = BlogsModel.objects.all()
    cat_id = request.GET.get('cat')
    tag_id = request.GET.get('tag')
    s = request.GET.get('s')

    if cat_id:
        blogs = blogs.filter(category=cat_id)

    if tag_id:
        blogs = blogs.filter(tag=tag_id)

    if s:
        blogs = blogs.filter(title__icontains=s)


    context = {
        'blogs': blogs,
    }
    return render(request, 'blogs/blog-list-sidebar-left.html', context)
