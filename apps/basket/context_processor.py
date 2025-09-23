from .cart import Basket
from ..products.models import ProductCategory


def basket(request):
    """
    Make basket available in all templates.
    """
    return {'basket': Basket(request)}

def products_categories(request):
    categories = ProductCategory.objects.filter(sub__isnull=True)
    subcategories = ProductCategory.objects.filter(sub__isnull=False)
    return {'categories': categories, 'subcategories': subcategories}