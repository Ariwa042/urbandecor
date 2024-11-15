from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.utils.decorators import method_decorator
from django.utils import timezone
from .models import SiteSettings, SalesTracking, Blog, ProductSettings
from order.models import Order, OrderItem, Payment
from product.models import Product
from core.models import Contact
from .forms import BlogForm, ProductForm, SiteSettingsForm, ContactForm

# Utility function for admin-only access
def admin_required(user):
    return user.is_staff and user.is_superuser


# Site Settings Views
@method_decorator([login_required, user_passes_test(admin_required)], name='dispatch')
class SiteSettingsView(UpdateView):
    model = SiteSettings
    form_class = SiteSettingsForm
    template_name = "admin/site_settings.html"
    success_url = reverse_lazy("admin:site_settings")

    def form_valid(self, form):
        messages.success(self.request, "Site settings updated successfully.")
        return super().form_valid(form)


# Order Management Views
@method_decorator([login_required, user_passes_test(admin_required)], name='dispatch')
class OrderListView(ListView):
    model = Order
    template_name = "admin/order_list.html"
    context_object_name = "orders"
    paginate_by = 10  # Pagination for better management

    def get_queryset(self):
        return Order.objects.all().order_by('-created_at')


@method_decorator([login_required, user_passes_test(admin_required)], name='dispatch')
class OrderDetailView(DetailView):
    model = Order
    template_name = "admin/order_detail.html"
    context_object_name = "order"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["order_items"] = self.object.order_items.all()  # Detailed view of order items
        return context


# Payment Tracking Views
@method_decorator([login_required, user_passes_test(admin_required)], name='dispatch')
class PaymentListView(ListView):
    model = Payment
    template_name = "admin/payment_list.html"
    context_object_name = "payments"
    paginate_by = 10

    def get_queryset(self):
        return Payment.objects.all().order_by('-payment_date')


# Sales Tracking Views
@method_decorator([login_required, user_passes_test(admin_required)], name='dispatch')
class SalesTrackingListView(ListView):
    model = SalesTracking
    template_name = "admin/sales_tracking.html"
    context_object_name = "sales_records"
    paginate_by = 10

    def get_queryset(self):
        return SalesTracking.objects.all().order_by('-sale_date')


# Blog Management Views
@method_decorator([login_required, user_passes_test(admin_required)], name='dispatch')
class BlogListView(ListView):
    model = Blog
    template_name = "admin/blog_list.html"
    context_object_name = "blogs"
    paginate_by = 10

@method_decorator([login_required, user_passes_test(admin_required)], name='dispatch')
class BlogCreateView(CreateView):
    model = Blog
    form_class = BlogForm
    template_name = "admin/blog_form.html"
    success_url = reverse_lazy("admin:blog_list")

    def form_valid(self, form):
        form.instance.author = self.request.user  # Set the author as the logged-in admin
        messages.success(self.request, "Blog post created successfully.")
        return super().form_valid(form)


@method_decorator([login_required, user_passes_test(admin_required)], name='dispatch')
class BlogUpdateView(UpdateView):
    model = Blog
    form_class = BlogForm
    template_name = "admin/blog_form.html"
    success_url = reverse_lazy("admin:blog_list")

    def form_valid(self, form):
        messages.success(self.request, "Blog post updated successfully.")
        return super().form_valid(form)


@method_decorator([login_required, user_passes_test(admin_required)], name='dispatch')
class BlogDeleteView(DeleteView):
    model = Blog
    template_name = "admin/blog_confirm_delete.html"
    success_url = reverse_lazy("admin:blog_list")

    def delete(self, request, *args, **kwargs):
        messages.success(request, "Blog post deleted successfully.")
        return super().delete(request, *args, **kwargs)


# Product Management Views
@method_decorator([login_required, user_passes_test(admin_required)], name='dispatch')
class ProductListView(ListView):
    model = Product
    template_name = "admin/product_list.html"
    context_object_name = "products"
    paginate_by = 10

@method_decorator([login_required, user_passes_test(admin_required)], name='dispatch')
class ProductUpdateView(UpdateView):
    model = Product
    form_class = ProductForm
    template_name = "admin/product_form.html"
    success_url = reverse_lazy("admin:product_list")

    def form_valid(self, form):
        messages.success(self.request, "Product updated successfully.")
        return super().form_valid(form)


# Contact Management (Synced with core Contact model)
@method_decorator([login_required, user_passes_test(admin_required)], name='dispatch')
class ContactUpdateView(UpdateView):
    model = Contact
    form_class = ContactForm
    template_name = "admin/contact_form.html"
    success_url = reverse_lazy("admin:site_settings")  # Redirect to settings page where contact is displayed

    def form_valid(self, form):
        messages.success(self.request, "Contact information updated successfully.")
        return super().form_valid(form)
