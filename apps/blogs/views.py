from django.contrib import messages
from django.http import Http404
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import DetailView, CreateView, ListView
from .forms import CommentsForm
from .models import *
from .utils import get_pk

class BlogDetailView(DetailView, CreateView):
    queryset = BlogsModel.objects.all()
    template_name = 'blogs/blog-detail.html'
    context_object_name = 'blog'
    success_url = reverse_lazy('blogs:detail')
    form_class = CommentsForm

    def get_success_url(self):
        pk = get_pk(self.request)
        return reverse_lazy('blogs:detail', kwargs={'pk': pk})

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.blog_id = get_pk(self.request)
        instance.save()
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Comment is error!')
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            pk = get_pk(self.request)
            blog = BlogsModel.objects.get(id=pk)
        except BlogsModel.DoesNotExist:
            raise Http404(render(self.request, 'pages/404.html'))

        related_blogs = BlogsModel.objects.filter(
            category__in=blog.category.all()
        ).exclude(id=blog.id).distinct()
        comments = CommentsModel.objects.filter(blog=pk)

        context['comments'] = comments
        context['blog'] = blog
        context['related_blogs'] = related_blogs
        return context


class BlogListView(ListView):
    queryset = BlogsModel.objects.all()
    template_name = 'blogs/blog-list-sidebar-left.html'
    context_object_name = 'blogs'
    paginate_by = 3

    def get_queryset(self):
        queryset = BlogsModel.objects.all()
        return queryset

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        blogs = BlogsModel.objects.all()
        cat_id = self.request.GET.get('cat')
        tag_id = self.request.GET.get('tag')
        s = self.request.GET.get('s')

        if cat_id:
            blogs = blogs.filter(category=cat_id)

        if tag_id:
            blogs = blogs.filter(tag=tag_id)

        if s:
            blogs = blogs.filter(title__icontains=s)

        context['blogs'] = blogs
        return context

