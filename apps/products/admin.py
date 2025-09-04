from django.contrib import admin

from .models import (
    ProductCategory, ProductSize, ProductColor, ProductBrand,
    ProductModel, ProductQuantity, ProductImageModel, ProductTag
)


class ProductImageInline(admin.TabularInline):
    model = ProductImageModel
    extra = 1  # Number of empty forms to display
    fields = ['image']
    verbose_name = 'Product Image'
    verbose_name_plural = 'Product Images'


class ProductQuantityInline(admin.TabularInline):
    model = ProductQuantity
    extra = 1  # Number of empty forms to display
    fields = ['quantity', 'sizes', 'colors']
    verbose_name = 'Product Quantity'
    verbose_name_plural = 'Product Quantities'


@admin.register(ProductModel)
class ProductModelAdmin(admin.ModelAdmin):
    list_display = ['title', 'brand', 'price', 'discount']
    list_filter = ['brand', 'categories', 'created_at']
    search_fields = ['title', 'short_description']
    filter_horizontal = ['categories']

    inlines = [ProductImageInline, ProductQuantityInline]

    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'short_description', 'long_description', 'image', 'image2')
        }),
        ('Product Details', {
            'fields': ('categories', 'brand', 'price', 'discount', 'tag')
        }),
    )


# Register other models normally
@admin.register(ProductCategory)
class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'created_at']
    search_fields = ['title']


@admin.register(ProductSize)
class ProductSizeAdmin(admin.ModelAdmin):
    list_display = ['title']
    search_fields = ['title']


@admin.register(ProductColor)
class ProductColorAdmin(admin.ModelAdmin):
    list_display = ['title', 'code']
    search_fields = ['title', 'code']


@admin.register(ProductBrand)
class ProductBrandAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']


@admin.register(ProductTag)
class ProductModelAdmin(admin.ModelAdmin):
    list_display = ['title']
    search_fields = ['title']
