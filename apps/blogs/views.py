from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import DetailView, CreateView, ListView
from .forms import CommentsForm
from .models import *

class BlogDetailView(LoginRequiredMixin, DetailView, CreateView):
    queryset = BlogsModel.objects.all()
    template_name = 'blogs/blog-detail.html'
    context_object_name = 'blog'
    success_url = reverse_lazy('blogs:detail')
    form_class = CommentsForm
    login_url = reverse_lazy('users:user_login')

    def get_success_url(self):
        return reverse_lazy('blogs:detail', kwargs={'pk':self.kwargs['pk']})

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.blog = BlogsModel.objects.get(id=self.kwargs['pk'])
        instance.email = self.request.user.email
        instance.name = self.request.user.username
        instance.save()
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Comment is error!')
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        blog = BlogsModel.objects.get(id=self.kwargs['pk'])
        related_blogs = BlogsModel.objects.filter(
            category__in=blog.category.all()
        ).exclude(id=blog.id).distinct()
        comments = CommentsModel.objects.filter(blog=blog.id)

        context['comments'] = comments
        context['related_blogs'] = related_blogs
        return context


class BlogListView(LoginRequiredMixin, ListView):
    queryset = BlogsModel.objects.all()
    template_name = 'blogs/blog-list-sidebar-left.html'
    context_object_name = 'blogs'
    paginate_by = 2
    login_url = reverse_lazy('users:user_login')

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


from .forms import BlogForm


class BlogCreateView(LoginRequiredMixin, CreateView):
    form_class = BlogForm
    template_name = 'blogs/blog_add.html'
    login_url = reverse_lazy('users:user_login')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['authors'] = AuthorsModel.objects.all()
        context['categories'] = CategoriesModel.objects.all()
        context['tags'] = TagsModel.objects.all()
        return context

    def form_valid(self, form):
        messages.success(self.request, 'Blog created successfully!')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Please check your spelling and try again!')
        return super().form_invalid(form)

    def get_success_url(self):
        return reverse_lazy('blogs:detail', kwargs={'pk': self.object.pk})

@login_required
def blog_delete(request, pk):
    blog = get_object_or_404(BlogsModel, pk=pk)
    if blog.author == request.user:
        blog.status = BlogsModel.Status.DELETED
        blog.save()
        messages.success(request, "Blog muvaffaqiyatli o‘chirildi.")
    else:
        return redirect('pages:page_404')
    return redirect(reverse('blogs:list_sidebar_left'))
