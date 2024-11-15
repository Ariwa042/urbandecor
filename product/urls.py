# product/urls.py
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'product'

urlpatterns = [
    path('', views.product_list, name='shop'),  # List all products
    path('<int:pk>/', views.product_detail, name='product_detail'),  # View product details
    path('create/', views.product_create, name='product_create'),  # Create a new product (staff only)
    path('<int:pk>/update/', views.product_update, name='product_update'),  # Update a product (staff only)
    path('<int:pk>/delete/', views.product_delete, name='product_delete'),  # Delete a product (staff only)
]

