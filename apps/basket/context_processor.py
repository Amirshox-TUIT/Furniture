from .cart import Basket


def basket(request):
    """
    Make basket available in all templates.
    """
    return {'basket': Basket(request)}