"""
Allocation models for SmartAlloc.
"""

from django.db import models
from django.core.validators import MinValueValidator

from apps.users.models import User
from apps.applications.models import Application
from apps.hostels.models import Room, BedSpace


class Allocation(models.Model):
    """
    Final room allocation model.
    """
    
    ALLOCATED_BY_CHOICES = [
        ('AI_System', 'AI System'),
        ('Admin_User', 'Admin User'),
    ]
    
    application = models.OneToOneField(
        Application,
        on_delete=models.CASCADE,
        related_name='allocation',
        help_text='The application that was allocated'
    )
    
    room = models.ForeignKey(
        Room,
        on_delete=models.CASCADE,
        related_name='allocations',
        help_text='The room assigned to the student'
    )
    
    bed_space = models.ForeignKey(
        BedSpace,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='allocation',
        help_text='The specific bed space assigned'
    )
    
    bed_space_number = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
        help_text='Bed space number within the room'
    )
    
    allocated_by = models.CharField(
        max_length=20,
        choices=ALLOCATED_BY_CHOICES,
        default='AI_System',
        help_text='Who made the allocation'
    )
    
    allocated_by_user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='manual_allocations',
        help_text='Admin user who manually allocated (if applicable)'
    )
    
    allocation_reason = models.TextField(
        blank=True,
        help_text='Reason for this allocation (explainability)'
    )
    
    admin_override = models.BooleanField(
        default=False,
        help_text='Was this allocation manually overridden by admin?'
    )
    
    # Student confirmation
    is_confirmed = models.BooleanField(
        default=False,
        help_text='Has the student confirmed the allocation?'
    )
    
    confirmed_at = models.DateTimeField(
        null=True,
        blank=True,
        help_text='When the student confirmed'
    )
    
    # Status
    is_active = models.BooleanField(
        default=True,
        help_text='Is this allocation currently active?'
    )
    
    cancelled_at = models.DateTimeField(
        null=True,
        blank=True,
        help_text='When the allocation was cancelled'
    )
    
    cancellation_reason = models.TextField(
        blank=True,
        help_text='Reason for cancellation'
    )
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Allocation'
        verbose_name_plural = 'Allocations'
        ordering = ['-created_at']
        permissions = [
            ('can_view_allocations', 'Can view all allocations'),
            ('can_create_allocation', 'Can create allocations'),
            ('can_override_allocation', 'Can override allocations'),
            ('can_cancel_allocation', 'Can cancel allocations'),
        ]
    
    def __str__(self):
        student_name = self.application.student.user.full_name
        return f"{student_name} -> {self.room}"
    
    @property
    def student(self):
        """Get the student from application."""
        return self.application.student
    
    def confirm(self):
        """Mark allocation as confirmed by student."""
        from django.utils import timezone
        self.is_confirmed = True
        self.confirmed_at = timezone.now()
        self.save(update_fields=['is_confirmed', 'confirmed_at'])
    
    def cancel(self, reason=''):
        """Cancel the allocation."""
        from django.utils import timezone
        self.is_active = False
        self.cancelled_at = timezone.now()
        self.cancellation_reason = reason
        self.save(update_fields=['is_active', 'cancelled_at', 'cancellation_reason'])
        
        # Free up bed space
        if self.bed_space:
            self.bed_space.deallocate()


class AuditLog(models.Model):
    """
    Audit log for allocation decisions.
    """
    
    ACTION_CHOICES = [
        ('ALLOCATION_CREATED', 'Allocation Created'),
        ('ALLOCATION_MODIFIED', 'Allocation Modified'),
        ('ALLOCATION_CANCELLED', 'Allocation Cancelled'),
        ('ALLOCATION_CONFIRMED', 'Allocation Confirmed'),
        ('PRIORITY_CALCULATED', 'Priority Calculated'),
        ('BATCH_ALLOCATION_RUN', 'Batch Allocation Run'),
        ('MANUAL_OVERRIDE', 'Manual Override'),
        ('SCORING_ADJUSTED', 'Scoring Adjusted'),
    ]
    
    action = models.CharField(
        max_length=30,
        choices=ACTION_CHOICES,
        help_text='Type of action performed'
    )
    
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='allocation_audit_logs',
        help_text='User who performed the action'
    )
    
    application = models.ForeignKey(
        Application,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='audit_logs',
        help_text='Related application'
    )
    
    allocation = models.ForeignKey(
        Allocation,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='audit_logs',
        help_text='Related allocation'
    )
    
    timestamp = models.DateTimeField(auto_now_add=True)
    
    ip_address = models.GenericIPAddressField(
        null=True,
        blank=True,
        help_text='IP address of the user'
    )
    
    details = models.JSONField(
        default=dict,
        help_text='Additional details about the action'
    )
    
    # For ML explainability
    input_features = models.JSONField(
        null=True,
        blank=True,
        help_text='Input features used for ML decisions'
    )
    
    model_version = models.CharField(
        max_length=20,
        blank=True,
        help_text='ML model version used'
    )
    
    raw_score = models.FloatField(
        null=True,
        blank=True,
        help_text='Raw ML model output'
    )
    
    final_score = models.FloatField(
        null=True,
        blank=True,
        help_text='Final adjusted score'
    )
    
    class Meta:
        verbose_name = 'Audit Log'
        verbose_name_plural = 'Audit Logs'
        ordering = ['-timestamp']
    
    def __str__(self):
        return f"{self.action} - {self.timestamp}"


class AllocationRun(models.Model):
    """
    Record of allocation batch runs.
    """
    
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('RUNNING', 'Running'),
        ('COMPLETED', 'Completed'),
        ('FAILED', 'Failed'),
        ('CANCELLED', 'Cancelled'),
    ]
    
    academic_session = models.CharField(
        max_length=9,
        help_text='Academic session for this run'
    )
    
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='PENDING'
    )
    
    started_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='started_allocation_runs'
    )
    
    started_at = models.DateTimeField(auto_now_add=True)
    
    completed_at = models.DateTimeField(
        null=True,
        blank=True
    )
    
    total_applications = models.PositiveIntegerField(
        default=0,
        help_text='Total applications processed'
    )
    
    successful_allocations = models.PositiveIntegerField(
        default=0,
        help_text='Number of successful allocations'
    )
    
    failed_allocations = models.PositiveIntegerField(
        default=0,
        help_text='Number of failed allocations'
    )
    
    waiting_list_count = models.PositiveIntegerField(
        default=0,
        help_text='Number of students added to waiting list'
    )
    
    error_message = models.TextField(
        blank=True,
        help_text='Error message if run failed'
    )
    
    parameters = models.JSONField(
        default=dict,
        help_text='Parameters used for this run'
    )
    
    celery_task_id = models.CharField(
        max_length=100,
        blank=True,
        help_text='Celery task ID for async tracking'
    )
    
    class Meta:
        verbose_name = 'Allocation Run'
        verbose_name_plural = 'Allocation Runs'
        ordering = ['-started_at']
    
    def __str__(self):
        return f"Allocation Run {self.id} - {self.academic_session} ({self.status})"
    
    def mark_completed(self):
        """Mark the run as completed."""
        from django.utils import timezone
        self.status = 'COMPLETED'
        self.completed_at = timezone.now()
        self.save(update_fields=['status', 'completed_at'])
    
    def mark_failed(self, error_message):
        """Mark the run as failed."""
        from django.utils import timezone
        self.status = 'FAILED'
        self.error_message = error_message
        self.completed_at = timezone.now()
        self.save(update_fields=['status', 'error_message', 'completed_at'])
