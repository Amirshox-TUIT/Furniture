from datetime import datetime
from decimal import Decimal, ROUND_HALF_UP

import pytz
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from apps.blogs.models import BaseModel


class ProductCategory(BaseModel):
    title = models.CharField(max_length=128)
    sub = models.ForeignKey(
        'self',
            null=True, blank=True,
            related_name='sub_category',
            on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'product category'
        verbose_name_plural = 'product categories'


class ProductTag(BaseModel):
    title = models.CharField(max_length=128)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'product tag'
        verbose_name_plural = 'product tags'


class ProductSize(models.Model):
    title = models.CharField(max_length=128)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'product size'
        verbose_name_plural = 'product sizes'


class ProductColor(models.Model):
    title = models.CharField(max_length=128)
    code = models.CharField(max_length=6)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'product color'
        verbose_name_plural = 'product colors'


class ProductBrand(models.Model):
    name = models.CharField(max_length=128)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'product brand'
        verbose_name_plural = 'product brands'


class ProductModel(BaseModel):
    title = models.CharField(max_length=100)
    short_description = models.TextField()
    long_description = models.TextField()

    image = models.ImageField(upload_to='products/', null=True, blank=True)
    image2 = models.ImageField(upload_to='products/', null=True, blank=True)
    categories = models.ManyToManyField(ProductCategory, related_name='products')
    brand = models.ForeignKey(ProductBrand, on_delete=models.CASCADE, related_name='products')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    tag = models.ManyToManyField(ProductTag, related_name='products')
    discount = models.PositiveSmallIntegerField(
        null=True, blank=True,
        validators=[MaxValueValidator(100), MinValueValidator(1)]
    )
    raiting = models.PositiveSmallIntegerField(default=0)

    def is_new(self):
        tashkent_tz = pytz.timezone('Asia/Tashkent')
        now = datetime.now(tashkent_tz)

        # Ensure created_at is timezone-aware
        if self.created_at.tzinfo is None:
            created_at = tashkent_tz.localize(self.created_at)
        else:
            created_at = self.created_at.astimezone(tashkent_tz)

        diff = now - created_at
        return diff.days <= 3

    def is_discount(self):
        if self.discount:
            return self.discount > 0
        return False

    def discount_price(self):
        if self.discount:
            discounted = self.price * (Decimal(1) - Decimal(self.discount) / Decimal(100))
            return discounted.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)  # 2 ta xonagacha
        return self.price.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'product'
        verbose_name_plural = 'products'



class ProductQuantity(BaseModel):
    product = models.ForeignKey(ProductModel, on_delete=models.CASCADE, related_name='products_quantity')
    quantity = models.PositiveSmallIntegerField()

    sizes = models.ForeignKey(ProductSize, on_delete=models.CASCADE, related_name='products_quantity')
    colors = models.ForeignKey(ProductColor, on_delete=models.CASCADE, related_name='products_quantity')


class ProductImageModel(BaseModel):
    product = models.ForeignKey(ProductModel, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='products/')

    def __str__(self):
        return self.product.title

    class Meta:
        verbose_name = 'product image'
        verbose_name_plural = 'product images'
