from decimal import Decimal

from django.conf import settings

from apps.products.models import ProductModel


class Basket:
    def __init__(self, request):
        """
        Initialize the basket.
        """
        self.session = request.session
        basket = self.session.get(settings.BASKET_SESSION_ID)
        if not basket:
            # Save an empty basket in the session
            basket = self.session[settings.BASKET_SESSION_ID] = dict()
        self.basket = basket

    def add(self, product, quantity=1, color=None, size=None, override_quantity=False):
        """
        Add a product to the basket or update its quantity.
        """
        product_id = str(product.id)
        if product_id not in self.basket:
            self.basket[product_id] = {
                'quantity': 0,
                'price': str(product.price),
                'color': color.title if color else None,
                'size': size.title if size else None,
            }
        if override_quantity:
            self.basket[product_id]['quantity'] = quantity
        else:
            self.basket[product_id]['quantity'] += quantity
        self.save()

    def save(self):
        """
        Mark the session as "modified" to make sure it gets saved.
        """
        self.session.modified = True

    def remove(self, product):
        """
        Remove a product from the basket.
        """
        product_id = str(product.id)
        if product_id in self.basket:
            del self.basket[product_id]
            self.save()

    def __iter__(self):
        """
        Iterate over the items in the basket and get the products
        from the database.
        """
        product_ids = self.basket.keys()
        # Get the product objects
        products = ProductModel.objects.filter(id__in=product_ids)

        for product in products:
            product_id = str(product.id)
            if product_id in self.basket:
                item = self.basket[product_id].copy()
                item['price'] = Decimal(item['price'])
                item['total_price'] = item['price'] * item['quantity']
                item['product'] = product  # Add product object to the yielded item
                yield item

    def __len__(self):
        """
        Count all items in the basket.
        """
        return sum(item['quantity'] for item in self.basket.values())

    def get_total_price(self):
        """
        Calculate the total cost of items in the basket.
        """
        return sum(Decimal(item['price']) * item['quantity']
                   for item in self.basket.values())

    def clear(self):
        """
        Remove basket from session
        """
        del self.session[settings.BASKET_SESSION_ID]
        self.save()

    def in_basket(self, product_id):
        return str(product_id) in self.basket.keys()