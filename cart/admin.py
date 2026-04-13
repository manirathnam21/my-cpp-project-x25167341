# cart/admin.py
from django.contrib import admin
from .models import CartItem, Order, OrderItem

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']
    extra = 0

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'full_name', 'email', 'status', 'created', 'total_price']
    list_filter = ['status', 'created', 'updated']
    search_fields = ['full_name', 'email', 'address']
    inlines = [OrderItemInline]

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'quantity', 'date_added']
    list_filter = ['date_added']
    search_fields = ['user__username', 'product__name']