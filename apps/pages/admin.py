from django.contrib import admin
from .models import ContactModel


@admin.register(ContactModel)
class ContactAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'subject', 'message']
    list_filter = ['created_at']
    search_fields = ['name', 'email', 'subject']
