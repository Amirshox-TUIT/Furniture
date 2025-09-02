from django.contrib import admin
from apps.blogs.models import *

@admin.register(CategoriesModel)
class CategoriesAdmin(admin.ModelAdmin):
    list_display = ['title']
    search_fields = ['title']
    list_filter = ['title']


@admin.register(TagsModel)
class TagsAdmin(admin.ModelAdmin):
    list_display = ['title']
    search_fields = ['title']
    list_filter = ['title']


@admin.register(BlogsModel)
class BlogsAdmin(admin.ModelAdmin):
    list_display = ['title', 'description', 'author_full_name']
    search_fields = ['title']
    list_filter = ['title']

    def author_full_name(self, obj):
        return obj.author.full_name


@admin.register(AuthorsModel)
class AuthorsAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'email']
    search_fields = ['full_name', 'email']
    list_filter = ['full_name']

@admin.register(CommentsModel)
class CommentsAdmin(admin.ModelAdmin):
    list_display = ['blog_title', 'name', 'text']
    search_fields = ['name', 'email']
    list_filter = ['created_at']

    def blog_title(self, obj):
        return obj.blog.title

