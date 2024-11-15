from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.sessions.models import Session
from django.http import HttpResponseForbidden
from .models import Cart, CartItem, Order, OrderItem, ShippingInfo
from .forms import CheckoutForm
from product.models import Product
import random
import string
from django.conf import settings

User = settings.AUTH_USER_MODEL

#def create_order_id():
#    """Generate a unique order ID."""
#    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=12))


def create_order_id():
    """Generate a unique order ID using only numbers."""
    return ''.join(random.choices(string.digits, k=12))


def get_cart(request):
    """Get the current cart, either from session for guests or user for logged-in users."""
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(customer=request.user)
    else:
        session_key = request.session.session_key
        if not session_key:
            request.session.create()
        cart, created = Cart.objects.get_or_create(session_key=session_key)

    return cart


def add_to_cart(request, product_id):
    """Add a product to the cart."""
    product = get_object_or_404(Product, pk=product_id)
    cart = get_cart(request)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    cart_item.quantity += 1  # Increment quantity if the item already exists
    cart_item.save()

    return redirect('order:cart_detail')


def cart_detail(request):
    """View to display the cart details."""
    cart = get_cart(request)
    total_amount = cart.total()
    context = {
        'cart': cart,
        'total_amount': total_amount,
    }
    return render(request, 'order/cart_detail.html', context)


def remove_from_cart(request, cart_item_id):
    """Remove a product from the cart."""
    cart_item = get_object_or_404(CartItem, pk=cart_item_id)
    cart_item.delete()
    return redirect('order:cart_detail')


def checkout(request):
    """Handle the checkout process for both authenticated and guest users."""
    cart = get_cart(request)
    if cart.cart_items.count() == 0:
        return redirect('order:cart_detail')

    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            # For authenticated users, use their account info
            if request.user.is_authenticated:
                shipping_info = ShippingInfo.objects.create(
                    email=form.cleaned_data['email'],
                    phone_number=form.cleaned_data['phone_number'],
                    address=form.cleaned_data['address'],
                    city=form.cleaned_data['city'],
                )
                order = Order.objects.create(
                    customer=request.user,
                    cart=cart,
                    shipping_address=shipping_info.address,
                   # shipping_method=form.cleaned_data['shipping_method'],
                  #  shipping_rate=form.cleaned_data['shipping_rate'],
                    order_id=create_order_id(),  # Generate unique order ID
                )
            else:  # For guest users, use session key
                shipping_info = ShippingInfo.objects.create(
                    email=form.cleaned_data['email'],
                    phone_number=form.cleaned_data['phone_number'],
                    address=form.cleaned_data['address'],
                    city=form.cleaned_data['city'],
                )
                order = Order.objects.create(
                    session_key=request.session.session_key,
                    cart=cart,
                    shipping_address=shipping_info.address,
                    #shipping_method=form.cleaned_data['shipping_method'],
                   # shipping_rate=form.cleaned_data['shipping_rate'],
                    order_id=create_order_id(),  # Generate unique order ID
                )

            order.calculate_total()  # Calculate total amount (cart value + shipping)
            for item in cart.cart_items.all():
                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    quantity=item.quantity,
                    price=item.product.price,
                )
            cart.cart_items.all().delete()  # Clear cart after order
            return redirect('order:purchase_history')

    else:
        form = CheckoutForm()

    return render(request, 'order/checkout.html', {'form': form})


def purchase_history(request):
    """View to show the purchase history for both authenticated and guest users."""
    if request.user.is_authenticated:
        orders = Order.objects.filter(customer=request.user).order_by('-created_at')
    else:
        session_key = request.session.session_key
        orders = Order.objects.filter(session_key=session_key).order_by('-created_at')

    context = {
        'orders': orders,
    }
    return render(request, 'order/purchase_history.html', context)

def order_detail(request, order_id):
    """
    View for displaying the details of a single order.
    Supports both guest and authenticated users.
    """
    # Check if the user is authenticated
    if request.user.is_authenticated:
        # For authenticated users, we use their user_id to fetch the order
        order = get_object_or_404(Order, pk=order_id, customer=request.user)
    else:
        # For guest users, we use the session key to fetch the order
        session_key = request.session.session_key
        if not session_key:
            # If there's no session key, we return an error or redirect
            return HttpResponseForbidden("Session key not found. Please add items to the cart before proceeding.")

        order = get_object_or_404(Order, pk=order_id, session_key=session_key)

    # Get the order items and calculate totals
    order_items = order.order_items.all()
    for item in order_items:
        item.item_total = item.price * item.quantity

    # Pass the order details to the template
    context = {
        'order': order,
        'order_items': order_items,
    }
    return render(request, 'order/order_detail.html', context)