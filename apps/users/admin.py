from django.contrib import admin
from .models import ProfileModel


@admin.register(ProfileModel)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'company', 'city', 'country', 'phone')
    search_fields = ('user__username', 'company', 'city', 'country', 'phone')
    list_filter = ('city', 'country')

