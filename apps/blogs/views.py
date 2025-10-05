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

        context['categories'] = CategoriesModel.objects.filter(sub__isnull=True)
        context['recent_blogs'] = BlogsModel.objects.exclude(id=self.kwargs['pk']).order_by("-created_at")[:2]
        context['tags'] = TagsModel.objects.all()
        return context


class BlogListView(LoginRequiredMixin, ListView):
    queryset = BlogsModel.objects.all()
    template_name = 'blogs/blog-list-sidebar-left.html'
    context_object_name = 'blogs'
    paginate_by = 2
    login_url = reverse_lazy('users:user_login')

    def get_queryset(self):
        blogs = BlogsModel.objects.all()
        tag_id = self.request.GET.get('tag')
        author_id = self.request.GET.get('author')
        s = self.request.GET.get('s')
        cat_id = self.request.GET.get('cat')
        if cat_id:
            blogs = blogs.filter(category=cat_id)

        if tag_id:
            blogs = blogs.filter(tag=tag_id)

        if author_id:
            blogs = blogs.filter(author_id=int(author_id))
        if s:
            blogs = blogs.filter(title__icontains=s)

        return blogs

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        tag_id = self.request.GET.get('tag')
        context['categories'] = CategoriesModel.objects.filter(sub__isnull=True)
        context['recent_blogs'] = BlogsModel.objects.order_by("-created_at")[:2]
        context['tags'] = TagsModel.objects.all()
        context['tag_id'] = tag_id
        return context


from .forms import BlogForm

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.shortcuts import redirect


class BlogCreateView(LoginRequiredMixin, CreateView):
    template_name = 'blogs/blog_add.html'
    login_url = reverse_lazy('users:user_login')
    model = BlogsModel
    fields = []

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = CategoriesModel.objects.all()
        context['tags'] = TagsModel.objects.all()
        return context

    def post(self, request, *args, **kwargs):
        try:
            author = AuthorsModel.objects.get(user=request.user)

            blog = BlogsModel.objects.create(
                title_en=request.POST.get('title_en'),
                title_uz=request.POST.get('title_uz'),
                description_en=request.POST.get('description_en'),
                description_uz=request.POST.get('description_uz'),
                image=request.FILES.get('image'),
                author=author
            )

            category_ids = request.POST.getlist('category')
            tag_ids = request.POST.getlist('tag')

            blog.category.set(category_ids)
            blog.tag.set(tag_ids)

            messages.success(request, 'Blog created successfully!')
            return redirect('blogs:detail', pk=blog.pk)

        except AuthorsModel.DoesNotExist:
            messages.error(request, 'You must have an author profile to create blogs!')
            return redirect('blogs:list_sidebar_left')

        except Exception as e:
            messages.error(request, f'Error creating blog: {str(e)}')
            return redirect('blogs:add')

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
