from django import template

from apps.basket.cart import Basket

register = template.Library()

@register.filter
def nospace(value):
    return value.replace(' ','')

@register.simple_tag
def get_full_url(request, lang):
    path = request.path.split('/')
    path[1] = lang
    return '/'.join(path)

@register.simple_tag
def in_basket(request, product_id):
    basket = Basket(request)
    return basket.in_basket(product_id)