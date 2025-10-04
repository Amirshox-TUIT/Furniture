# apps/orders/models.py
import uuid
from django.contrib.auth import get_user_model
from django.db import models
from decimal import Decimal

User = get_user_model()


class Order(models.Model):
    class Status(models.TextChoices):
        CASH = ('cash', 'Cash')
        CARD = ('card', 'Card')

    class OrderStatus(models.TextChoices):
        PENDING = ('pending', 'Pending')
        PROCESSING = ('processing', 'Processing')
        SHIPPED = ('shipped', 'Shipped')
        DELIVERED = ('delivered', 'Delivered')
        CANCELLED = ('cancelled', 'Cancelled')

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='orders')
    unique_id = models.CharField(max_length=10, editable=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    delivery = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    payment_method = models.CharField(default=Status.CARD, max_length=10, choices=Status.choices)
    order_status = models.CharField(max_length=20, choices=OrderStatus.choices, default=OrderStatus.PENDING)

    customer_name = models.CharField(max_length=100, null=True, blank=True)
    customer_email = models.EmailField(null=True, blank=True)
    customer_phone = models.CharField(max_length=128, null=True, blank=True)

    shipping_address = models.CharField(max_length=255, null=True, blank=True)
    shipping_city = models.CharField(max_length=128, null=True, blank=True)
    shipping_postal_code = models.CharField(max_length=15, null=True, blank=True)
    shipping_country = models.CharField(max_length=128, null=True, blank=True)
    shipping_method = models.CharField(max_length=20, default='standard')

    def get_total_price(self):
        items_total = sum(item.get_total_price() for item in self.items.all())
        delivery = Decimal(self.delivery or 0)
        return float(items_total + delivery)

    def get_items_total(self):
        return sum(item.get_total_price() for item in self.items.all())

    def __str__(self):
        return f"Order #{self.unique_id}"

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey('products.ProductModel', on_delete=models.SET_NULL, null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    quantity = models.PositiveIntegerField(default=1)

    product_name = models.CharField(max_length=255, null=True, blank=True)
    product_image = models.ImageField(upload_to='order_items/', null=True, blank=True)

    def get_total_price(self):
        price = Decimal(self.price or 0)
        quantity = Decimal(self.quantity or 0)
        return price * quantity

    def __str__(self):
        return f"{self.quantity}x {self.product_name or self.product or 'Unknown Product'}"

    class Meta:
        verbose_name = 'Order Item'
        verbose_name_plural = 'Order Items'