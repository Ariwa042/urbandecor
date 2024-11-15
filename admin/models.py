from django.db import models
from django.conf import settings
from django.utils import timezone
from core.models import Contact  # Importing the Contact model from core for contact information
from order.models import Order
from product.models import Product
from django_summernote.fields import SummernoteTextField


# Abstract model for shared fields (e.g., author info, timestamps)
class BaseContent(models.Model):
    """
    Base model for content-related models such as Blog and Product,
    to include shared fields like title, content, and timestamps.
    """
    title = models.CharField(max_length=255, unique=True)
    content = SummernoteTextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True, help_text="Is this item active on the site?")

    class Meta:
        abstract = True  # Indicates this model is only used for inheritance
        ordering = ['-created_at']


class Blog(BaseContent):
    """
    Blog model inheriting from BaseContent and linked to a unique Contact entry.
    """
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    contact_info = models.OneToOneField(Contact, on_delete=models.SET_NULL, null=True, blank=True, help_text="Contact information for this blog post")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Blog Post"
        verbose_name_plural = "Blog Posts"


class SiteSettings(models.Model):
    """
    Centralized settings for the site that also includes a link to the core Contact model.
    """
    site_name = models.CharField(max_length=255, default="My Store")
    business_hours = models.CharField(max_length=255, blank=True, null=True)
    contact = models.OneToOneField(Contact, on_delete=models.SET_NULL, null=True, blank=True, help_text="Business contact information")
    social_media_links = models.JSONField(default=dict, blank=True, null=True)

    def __str__(self):
        return f"Settings for {self.site_name}"

    class Meta:
        verbose_name = "Site Setting"
        verbose_name_plural = "Site Settings"


class ProductSettings(models.Model):
    """
    Centralized settings specific to products, linked to Contact for consistent contact details.
    """
    product = models.OneToOneField(Product, on_delete=models.CASCADE, related_name="product_settings")
    contact_info = models.OneToOneField(Contact, on_delete=models.SET_NULL, null=True, blank=True, help_text="Product support contact information")

    def __str__(self):
        return f"Settings for Product {self.product.name}"

    class Meta:
        verbose_name = "Product Setting"
        verbose_name_plural = "Product Settings"


# Sales and Tracking Models
class SalesTracking(models.Model):
    """
    Tracks individual sales and links to orders and payments, with shared settings linked.
    """
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="sales")
    sale_date = models.DateTimeField(default=timezone.now)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Sale for Order #{self.order.id} on {self.sale_date}"

    class Meta:
        verbose_name = "Sales Tracking"
        verbose_name_plural = "Sales Tracking"


class ProductReview(models.Model):
    """
    Product review model with contact info synchronized via Contact.
    """
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="reviews")
    customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    rating = models.PositiveIntegerField(choices=[(i, str(i)) for i in range(1, 6)], default=5)
    review_content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    contact_info = models.OneToOneField(Contact, on_delete=models.SET_NULL, null=True, blank=True, help_text="Contact info for review inquiries")

    def __str__(self):
        return f"Review for {self.product.name} by {self.customer.username if self.customer else 'Guest'}"

    class Meta:
        verbose_name = "Product Review"
        verbose_name_plural = "Product Reviews"
        ordering = ['-created_at']


class SupportTicket(models.Model):
    """
    Support tickets with contact information linked for easy reference and editing.
    """
    customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    issue_description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_resolved = models.BooleanField(default=False)
    contact_info = models.OneToOneField(Contact, on_delete=models.SET_NULL, null=True, blank=True, help_text="Contact information for support")

    def __str__(self):
        return f"Ticket #{self.id} - {self.issue_description[:30]}"

    class Meta:
        verbose_name = "Support Ticket"
        verbose_name_plural = "Support Tickets"
