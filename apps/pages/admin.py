from django.contrib import admin
from django.core.paginator import Page
from modeltranslation.admin import TranslationAdmin

from .models import ContactModel, AboutModel, BannerModel


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

@admin.register(ContactModel)
class ContactAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'subject', 'message']
    list_filter = ['created_at']
    search_fields = ['name', 'email', 'subject']


@admin.register(AboutModel)
class AboutAdmin(MyTranslationAdmin):
    list_display = ['name', 'profession']
    search_fields = ['name', 'profession']
    list_filter = ['name']


@admin.register(BannerModel)
class BannerAdmin(MyTranslationAdmin):
    list_display = ['title']
    search_fields = ['title']
    list_filter = ['title']
