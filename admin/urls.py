from django.urls import path
from . import views

app_name = 'admin'

urlpatterns = [
    # Site Settings and Contact
    path('site-settings/', views.SiteSettingsView.as_view(), name='site_settings'),
    path('contact-settings/', views.ContactUpdateView.as_view(), name='contact_settings'),

    # Order Management
    path('orders/', views.OrderListView.as_view(), name='order_list'),
    path('orders/<int:pk>/', views.OrderDetailView.as_view(), name='order_detail'),

    # Payment Tracking
    path('payments/', views.PaymentListView.as_view(), name='payment_list'),

    # Sales Tracking
    path('sales-tracking/', views.SalesTrackingListView.as_view(), name='sales_tracking'),

    # Blog Management
    path('blogs/', views.BlogListView.as_view(), name='blog_list'),
    path('blogs/add/', views.BlogCreateView.as_view(), name='blog_add'),
    path('blogs/<int:pk>/edit/', views.BlogUpdateView.as_view(), name='blog_edit'),
    path('blogs/<int:pk>/delete/', views.BlogDeleteView.as_view(), name='blog_delete'),

    # Product Management
    path('products/', views.ProductListView.as_view(), name='product_list'),
    path('products/<int:pk>/edit/', views.ProductUpdateView.as_view(), name='product_edit'),
]
