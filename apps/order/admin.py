from django.contrib import admin
from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('product', 'product_name', 'price', 'quantity', 'get_total_display')
    fields = ('product', 'product_name', 'price', 'quantity', 'get_total_display')
    can_delete = False

    def get_total_display(self, obj):
        """Display total price for this item"""
        if obj.id:
            return f"£{obj.get_total_price():.2f}"
        return "—"

    get_total_display.short_description = 'Total'


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'unique_id',
        'customer_name',
        'customer_email',
        'created_at',
        'order_status',
        'payment_method',
        'get_total_display'
    )
    list_filter = ('order_status', 'payment_method', 'created_at', 'shipping_method')
    search_fields = ('unique_id', 'customer_name', 'customer_email', 'customer_phone')
    readonly_fields = (
        'unique_id',
        'created_at',
        'updated_at',
        'get_total_display',
        'get_items_total_display'
    )
    inlines = [OrderItemInline]

    fieldsets = (
        ('Order Information', {
            'fields': ('unique_id', 'user', 'order_status', 'created_at', 'updated_at')
        }),
        ('Customer Information', {
            'fields': ('customer_name', 'customer_email', 'customer_phone')
        }),
        ('Shipping Address', {
            'fields': ('shipping_address', 'shipping_city', 'shipping_postal_code', 'shipping_country')
        }),
        ('Delivery & Payment', {
            'fields': ('shipping_method', 'delivery', 'payment_method')
        }),
        ('Totals', {
            'fields': ('get_items_total_display', 'get_total_display')
        }),
    )

    def get_total_display(self, obj):
        return f"£{obj.get_total_price():.2f}"

    get_total_display.short_description = 'Total Price'

    def get_items_total_display(self, obj):
        return f"£{obj.get_items_total():.2f}"

    get_items_total_display.short_description = 'Items Total'

    def has_add_permission(self, request):
        return False


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'product_name', 'price', 'quantity', 'get_total_display')
    list_filter = ('order__created_at',)
    search_fields = ('product_name', 'order__unique_id')
    readonly_fields = ('order', 'product', 'price', 'quantity', 'product_name', 'get_total_display')

    def get_total_display(self, obj):
        return f"£{obj.get_total_price():.2f}"

    get_total_display.short_description = 'Total'

    def has_add_permission(self, request):
        return False