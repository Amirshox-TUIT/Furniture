from django import template

from apps.blogs.models import AuthorsModel

register = template.Library()

@register.filter
def is_author(user):
    return hasattr(user, 'author')