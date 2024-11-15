# products/admin.py
from django.contrib import admin
from .models import Product, Category, ProductImages
from .forms import ProductForm, CategoryForm

class ProductImagesAdmin(admin.TabularInline):
    model = ProductImages
    
class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImagesAdmin]
    form = ProductForm
    list_display = ['name', 'category', 'price', 'is_available', 'featured', 'created_at']
    search_fields = ['name', 'category__name', 'featured']
    list_filter = ['category', 'is_available', 'featured']
#    prepopulated_fields = {'slug': ('name',)}

class CategoryAdmin(admin.ModelAdmin):
    form = CategoryForm
    list_display = ['name']
    search_fields = ['name']



admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
