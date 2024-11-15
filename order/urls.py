from django.urls import path
from . import views

app_name = 'order'

urlpatterns = [
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart_detail, name='cart'),
    path('remove-from-cart/<int:cart_item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('purchase-history/', views.purchase_history, name='purchase_history'),
    path('order-detail/<str:order_id>/', views.order_detail, name='order_detail')
]
