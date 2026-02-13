"""
Admin configuration for users app.
"""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _

from .models import User, EmailVerificationToken, PasswordResetToken


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """Admin configuration for User model."""
    
    list_display = [
        'email', 'first_name', 'last_name', 'user_type',
        'matric_number', 'department', 'is_verified', 'is_active', 'date_joined'
    ]
    list_filter = ['user_type', 'is_verified', 'is_active', 'date_joined', 'department']
    search_fields = ['email', 'first_name', 'last_name', 'matric_number', 'department']
    ordering = ['-date_joined']
    
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {
            'fields': ('first_name', 'last_name', 'phone_number', 'department')
        }),
        (_('Student info'), {
            'fields': ('matric_number',),
            'classes': ('collapse',)
        }),
        (_('Permissions'), {
            'fields': ('user_type', 'is_active', 'is_staff', 'is_superuser', 'is_verified', 'groups', 'user_permissions'),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'user_type'),
        }),
    )
    
    readonly_fields = ['date_joined', 'last_login']


@admin.register(EmailVerificationToken)
class EmailVerificationTokenAdmin(admin.ModelAdmin):
    """Admin configuration for EmailVerificationToken model."""
    
    list_display = ['user', 'created_at', 'expires_at', 'is_used', 'is_expired']
    list_filter = ['is_used', 'created_at']
    search_fields = ['user__email', 'token']
    readonly_fields = ['token', 'created_at']


@admin.register(PasswordResetToken)
class PasswordResetTokenAdmin(admin.ModelAdmin):
    """Admin configuration for PasswordResetToken model."""
    
    list_display = ['user', 'created_at', 'expires_at', 'is_used', 'ip_address', 'is_expired']
    list_filter = ['is_used', 'created_at']
    search_fields = ['user__email', 'token']
    readonly_fields = ['token', 'created_at']
