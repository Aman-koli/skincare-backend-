from django.contrib import admin
from .models import Order, OrderItem, ReturnRequest

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ['product', 'product_name', 'price', 'quantity']

class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'full_name', 'total_amount', 'status', 'is_paid', 'created_at']
    list_filter = ['status', 'is_paid']
    inlines = [OrderItemInline]

class ReturnRequestAdmin(admin.ModelAdmin):
    list_display = ['id', 'order', 'reason', 'status', 'created_at']
    list_filter = ['status', 'reason']

admin.site.register(Order, OrderAdmin)
admin.site.register(ReturnRequest, ReturnRequestAdmin)