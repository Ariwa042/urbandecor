# core/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django_summernote.admin import SummernoteModelAdmin
from .models import User, ContactMessage, Contact, BlogPost

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    # Customize User model admin
    model = User
    list_display = ('email', 'username', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_active')
    search_fields = ('email', 'username')
    ordering = ('email',)
    fieldsets = (
        (None, {'fields': ('email', 'username', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password1', 'password2', 'is_staff', 'is_active')}
        ),
    )

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    # Customize ContactMessage admin
    list_display = ('name', 'email', 'subject', 'created_at')
    search_fields = ('name', 'email', 'subject')
    list_filter = ('created_at',)

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    # Customize Contact admin
    list_display = ('address', 'phone', 'email')
    search_fields = ('address', 'phone', 'email')

@admin.register(BlogPost)
class BlogPostAdmin(SummernoteModelAdmin):
    # Use Summernote for content field in BlogPost
    summernote_fields = ('content',)
    list_display = ('title', 'author', 'is_published', 'created_at', 'updated_at')
    list_filter = ('is_published', 'created_at')
    search_fields = ('title', 'author__username')
    prepopulated_fields = {'slug': ('title',)}
