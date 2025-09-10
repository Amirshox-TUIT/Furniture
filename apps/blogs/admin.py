from django.contrib import admin
from modeltranslation.admin import TranslationAdmin

from apps.blogs.models import *


class MyTranslationAdmin(TranslationAdmin):
    class Media:
        js = (
            'http://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js',
            'http://ajax.googleapis.com/ajax/libs/jqueryui/1.10.2/jquery-ui.min.js',
            'modeltranslation/js/tabbed_translation_fields.js',
        )
        css = {
            'screen': ('modeltranslation/css/tabbed_translation_fields.css',),
        }

@admin.register(CategoriesModel)
class CategoriesAdmin(MyTranslationAdmin):
    list_display = ['title']
    search_fields = ['title']
    list_filter = ['title']


@admin.register(TagsModel)
class TagsAdmin(MyTranslationAdmin):
    list_display = ['title']
    search_fields = ['title']
    list_filter = ['title']


@admin.register(BlogsModel)
class BlogsAdmin(MyTranslationAdmin):
    list_display = ['title', 'description', 'author_full_name']
    search_fields = ['title']
    list_filter = ['title']

    def author_full_name(self, obj):
        return obj.author.full_name


@admin.register(AuthorsModel)
class AuthorsAdmin(MyTranslationAdmin):
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

