from enum import unique
from django.db import models
from django.conf import settings
from django.contrib.sessions.models import Session
from product.models import Product
from shortuuid.django_fields import ShortUUIDField

class ShippingInfo(models.Model):
    email = models.EmailField()
    phone_number = models.CharField(max_length=20)
    address = models.TextField()
    city = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.email} - {self.city}"

    class Meta:
        verbose_name = 'Shipping Info'
        verbose_name_plural = 'Shipping Info'


class Cart(models.Model):
    customer = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL)
    session_key = models.CharField(max_length=40, blank=True, null=True)  # For guest users
    shipping_info = models.OneToOneField(ShippingInfo, null=True, blank=True, on_delete=models.CASCADE)  # Link shipping info
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def total(self):
        """
        Calculate the total value of the cart (product price * quantity).
        """
        return sum(item.total_price() for item in self.cart_items.all())

    def __str__(self):
        return f"Cart for {self.customer or 'Guest'}"

    class Meta:
        verbose_name = 'Cart'
        verbose_name_plural = 'Carts'


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='cart_items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)

    def total_price(self):
        return self.product.price * self.quantity

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"

    class Meta:
        verbose_name = 'Cart Item'
        verbose_name_plural = 'Cart Items'


class Order(models.Model):
    ORDER_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('canceled', 'Canceled'),
    ]

#    SHIPPING_METHOD_CHOICES = [
#        ('standard', 'Standard Shipping'),
#        ('express', 'Express Shipping'),
#    ]
    order_id = ShortUUIDField(
        unique=True, max_length=10, length=6, alphabet="1234567890", primary_key=True  # This makes it the primary key
    ) 
    customer = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL)
    session_key = models.CharField(max_length=40, blank=True, null=True)  # For guest users
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=ORDER_STATUS_CHOICES, default='pending')
#    shipping_method = models.CharField(max_length=20, choices=SHIPPING_METHOD_CHOICES, default='standard')
    shipping_address = models.TextField()  # Customer's shipping address
#    shipping_rate = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)  # Cost of shipping
    cart_value = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def calculate_total(self):
        self.cart_value = self.cart.total()
        self.total_amount = self.cart_value
        self.save()

    def __str__(self):
        return f"Order #{self.order_id} for {self.customer or 'Guest'}"

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='order_items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def save(self, *args, **kwargs):
        if not self.price:
            self.price = self.product.price
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"

    class Meta:
        verbose_name = 'Order Item'
        verbose_name_plural = 'Order Items'


class BankAccount(models.Model):
    bank_name = models.CharField(max_length=100)
    account_number = models.CharField(max_length=20)
    account_name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.bank_name} - {self.account_name}"

    class Meta:
        verbose_name = 'Bank Account'
        verbose_name_plural = 'Bank Accounts'


class Payment(models.Model):
    PAYMENT_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('canceled', 'Canceled'),
    ]

    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='payment')
    payment_status = models.CharField(max_length=10, choices=PAYMENT_STATUS_CHOICES, default='pending')
    payment_date = models.DateTimeField(auto_now_add=True)
    transaction_id = ShortUUIDField(unique=True, max_length=20, length=5, alphabet='1234567890', primary_key=True, prefix='TR')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_details = models.TextField(blank=True, null=True)
    bank_account = models.ForeignKey(BankAccount, on_delete=models.CASCADE, related_name='payments')

    def __str__(self):
        return f"Payment for Order #{self.order.pk} - {self.get_payment_status_display()}"

    class Meta:
        verbose_name = 'Payment'
        verbose_name_plural = 'Payments'
