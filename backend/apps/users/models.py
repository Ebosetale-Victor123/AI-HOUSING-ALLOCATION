"""
Custom User model for SmartAlloc.
"""

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from utils.constants import UserType
from utils.validators import validate_matric_number, validate_phone_number


class User(AbstractUser):
    """
    Custom User model with additional fields for university context.
    """
    
    # Remove username field and use email as primary identifier
    username = None
    email = models.EmailField(
        _('email address'),
        unique=True,
        help_text=_('Required. Used as the primary identifier.')
    )
    
    # User type for role-based access control
    user_type = models.CharField(
        max_length=20,
        choices=UserType.choices,
        default=UserType.STUDENT,
        help_text=_('Type of user (Student, Admin, Super Admin)')
    )
    
    # Student-specific fields
    matric_number = models.CharField(
        max_length=20,
        unique=True,
        null=True,
        blank=True,
        validators=[validate_matric_number],
        help_text=_('Unique matriculation number for students')
    )
    
    # Common profile fields
    department = models.CharField(
        max_length=100,
        blank=True,
        help_text=_('Academic department or unit')
    )
    
    phone_number = models.CharField(
        max_length=20,
        blank=True,
        validators=[validate_phone_number],
        help_text=_('Phone number with country code (e.g., +234...)')
    )
    
    # Verification status
    is_verified = models.BooleanField(
        default=False,
        help_text=_('Designates whether the user has verified their email.')
    )
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Set email as the username field
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']
    
    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        ordering = ['-date_joined']
        permissions = [
            ('can_view_all_students', 'Can view all student profiles'),
            ('can_manage_allocations', 'Can manage housing allocations'),
            ('can_run_allocation', 'Can run allocation algorithm'),
            ('can_override_allocation', 'Can manually override allocations'),
        ]
    
    def __str__(self):
        if self.matric_number:
            return f"{self.email} ({self.matric_number})"
        return self.email
    
    @property
    def is_student(self):
        """Check if user is a student."""
        return self.user_type == UserType.STUDENT
    
    @property
    def is_admin(self):
        """Check if user is an admin (includes super admin)."""
        return self.user_type in [UserType.ADMIN, UserType.SUPER_ADMIN]
    
    @property
    def is_super_admin(self):
        """Check if user is a super admin."""
        return self.user_type == UserType.SUPER_ADMIN
    
    @property
    def full_name(self):
        """Return user's full name."""
        return f"{self.first_name} {self.last_name}".strip()
    
    def get_student_profile(self):
        """Get associated student profile if exists."""
        if self.is_student:
            try:
                return self.studentprofile
            except:
                return None
        return None


class EmailVerificationToken(models.Model):
    """
    Model to store email verification tokens.
    """
    
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='verification_tokens'
    )
    token = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    is_used = models.BooleanField(default=False)
    
    class Meta:
        verbose_name = 'Email Verification Token'
        verbose_name_plural = 'Email Verification Tokens'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Verification token for {self.user.email}"
    
    @property
    def is_expired(self):
        """Check if token has expired."""
        from django.utils import timezone
        return timezone.now() > self.expires_at
    
    @property
    def is_valid(self):
        """Check if token is still valid."""
        return not self.is_used and not self.is_expired


class PasswordResetToken(models.Model):
    """
    Model to store password reset tokens.
    """
    
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='password_reset_tokens'
    )
    token = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    is_used = models.BooleanField(default=False)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    
    class Meta:
        verbose_name = 'Password Reset Token'
        verbose_name_plural = 'Password Reset Tokens'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Password reset token for {self.user.email}"
    
    @property
    def is_expired(self):
        """Check if token has expired."""
        from django.utils import timezone
        return timezone.now() > self.expires_at
    
    @property
    def is_valid(self):
        """Check if token is still valid."""
        return not self.is_used and not self.is_expired
