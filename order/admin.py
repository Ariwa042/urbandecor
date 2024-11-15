# order/admin.py

from django.contrib import admin
from .models import Cart, CartItem, Order, OrderItem, Payment, BankAccount

class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 1

class CartAdmin(admin.ModelAdmin):
    list_display = ('customer', 'created_at', 'updated_at')
    inlines = [CartItemInline]

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1

class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_id', 'customer', 'status', 'total_amount', 'created_at')
    inlines = [OrderItemInline]
    search_fields = ('customer__username', 'order_id')

class PaymentAdmin(admin.ModelAdmin):
    list_display = ('order', 'payment_status', 'payment_date', 'amount', 'bank_account')
    list_filter = ('payment_status',)
    search_fields = ('order__id',)

class BankAccountAdmin(admin.ModelAdmin):
    list_display = ('bank_name', 'account_number', 'account_name')

admin.site.register(Cart, CartAdmin)
admin.site.register(CartItem)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem)
admin.site.register(Payment, PaymentAdmin)
admin.site.register(BankAccount, BankAccountAdmin)
