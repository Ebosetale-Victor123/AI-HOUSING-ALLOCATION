"""
Application models for SmartAlloc.
"""

from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

from apps.users.models import User
from apps.students.models import StudentProfile
from apps.hostels.models import Hostel
from utils.constants import ApplicationStatus, DEFAULT_ACADEMIC_SESSION
from utils.validators import validate_academic_session, validate_file_size


class Application(models.Model):
    """
    Housing application model.
    """
    
    student = models.ForeignKey(
        StudentProfile,
        on_delete=models.CASCADE,
        related_name='applications',
        help_text='The student applying for housing'
    )
    
    academic_session = models.CharField(
        max_length=9,
        default=DEFAULT_ACADEMIC_SESSION,
        validators=[validate_academic_session],
        help_text='Academic session (e.g., 2024/2025)'
    )
    
    preferred_hostel = models.ForeignKey(
        Hostel,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='applications',
        help_text='Preferred hostel (optional)'
    )
    
    # Application Status
    status = models.CharField(
        max_length=20,
        choices=ApplicationStatus.choices,
        default=ApplicationStatus.PENDING,
        help_text='Current status of the application'
    )
    
    # AI-Generated Priority Score
    priority_score = models.FloatField(
        null=True,
        blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        help_text='AI-generated priority score (0-100)'
    )
    
    ai_confidence = models.FloatField(
        null=True,
        blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(1)],
        help_text='Model confidence in the prediction (0-1)'
    )
    
    # Scoring Factors (stored for transparency)
    gpa_factor = models.FloatField(
        null=True,
        blank=True,
        help_text='GPA contribution to score'
    )
    
    distance_factor = models.FloatField(
        null=True,
        blank=True,
        help_text='Distance contribution to score'
    )
    
    level_factor = models.FloatField(
        null=True,
        blank=True,
        help_text='Academic level contribution to score'
    )
    
    need_factor = models.FloatField(
        null=True,
        blank=True,
        help_text='Need-based contribution to score'
    )
    
    # Additional Information
    special_requests = models.TextField(
        blank=True,
        help_text='Any special requests or considerations'
    )
    
    medical_certificate = models.FileField(
        upload_to='medical_certificates/%Y/%m/',
        null=True,
        blank=True,
        help_text='Medical certificate (if applicable)'
    )
    
    # Timestamps
    application_date = models.DateTimeField(auto_now_add=True)
    allocation_date = models.DateTimeField(
        null=True,
        blank=True,
        help_text='When the application was allocated'
    )
    
    reviewed_at = models.DateTimeField(
        null=True,
        blank=True,
        help_text='When the application was reviewed'
    )
    
    reviewed_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='reviewed_applications',
        help_text='Admin who reviewed the application'
    )
    
    review_notes = models.TextField(
        blank=True,
        help_text='Notes from the review process'
    )
    
    class Meta:
        verbose_name = 'Application'
        verbose_name_plural = 'Applications'
        ordering = ['-priority_score', 'application_date']
        unique_together = ['student', 'academic_session']
        permissions = [
            ('can_review_applications', 'Can review housing applications'),
            ('can_approve_applications', 'Can approve/reject applications'),
            ('can_view_all_applications', 'Can view all applications'),
        ]
    
    def __str__(self):
        return f"{self.student.user.full_name} - {self.academic_session} ({self.status})"
    
    @property
    def is_pending(self):
        """Check if application is pending."""
        return self.status == ApplicationStatus.PENDING
    
    @property
    def is_allocated(self):
        """Check if application has been allocated."""
        return self.status == ApplicationStatus.ALLOCATED
    
    @property
    def is_approved(self):
        """Check if application has been approved."""
        return self.status == ApplicationStatus.APPROVED
    
    @property
    def scoring_factors(self):
        """Return scoring factors as a dictionary."""
        return {
            'gpa': self.gpa_factor,
            'distance': self.distance_factor,
            'level': self.level_factor,
            'need': self.need_factor,
        }
    
    def approve(self, reviewed_by=None, notes=''):
        """Approve the application."""
        self.status = ApplicationStatus.APPROVED
        self.reviewed_at = models.DateTimeField()._get_current_value()
        self.reviewed_by = reviewed_by
        self.review_notes = notes
        self.save(update_fields=[
            'status', 'reviewed_at', 'reviewed_by', 'review_notes'
        ])
    
    def reject(self, reviewed_by=None, notes=''):
        """Reject the application."""
        self.status = ApplicationStatus.REJECTED
        self.reviewed_at = models.DateTimeField()._get_current_value()
        self.reviewed_by = reviewed_by
        self.review_notes = notes
        self.save(update_fields=[
            'status', 'reviewed_at', 'reviewed_by', 'review_notes'
        ])
    
    def mark_allocated(self):
        """Mark application as allocated."""
        from django.utils import timezone
        self.status = ApplicationStatus.ALLOCATED
        self.allocation_date = timezone.now()
        self.save(update_fields=['status', 'allocation_date'])


class ApplicationPeriod(models.Model):
    """
    Application period settings.
    """
    
    academic_session = models.CharField(
        max_length=9,
        unique=True,
        validators=[validate_academic_session],
        help_text='Academic session'
    )
    
    name = models.CharField(
        max_length=100,
        help_text='Name of the application period'
    )
    
    description = models.TextField(
        blank=True,
        help_text='Description of the application period'
    )
    
    start_date = models.DateTimeField(
        help_text='When applications open'
    )
    
    end_date = models.DateTimeField(
        help_text='When applications close'
    )
    
    is_active = models.BooleanField(
        default=False,
        help_text='Is this the current active period?'
    )
    
    allow_new_applications = models.BooleanField(
        default=True,
        help_text='Are new applications currently accepted?'
    )
    
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='created_periods'
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Application Period'
        verbose_name_plural = 'Application Periods'
        ordering = ['-start_date']
    
    def __str__(self):
        return f"{self.name} ({self.academic_session})"
    
    @property
    def is_open(self):
        """Check if application period is currently open."""
        from django.utils import timezone
        now = timezone.now()
        return (
            self.is_active and
            self.allow_new_applications and
            self.start_date <= now <= self.end_date
        )
    
    @property
    def status(self):
        """Get current status of the period."""
        from django.utils import timezone
        now = timezone.now()
        
        if not self.is_active:
            return 'inactive'
        elif now < self.start_date:
            return 'upcoming'
        elif now > self.end_date:
            return 'closed'
        elif not self.allow_new_applications:
            return 'paused'
        else:
            return 'open'


class WaitingList(models.Model):
    """
    Waiting list for students who couldn't be allocated.
    """
    
    application = models.OneToOneField(
        Application,
        on_delete=models.CASCADE,
        related_name='waiting_list_entry'
    )
    
    position = models.PositiveIntegerField(
        help_text='Position in the waiting list'
    )
    
    added_at = models.DateTimeField(auto_now_add=True)
    
    is_priority = models.BooleanField(
        default=False,
        help_text='Is this a priority waiting list entry?'
    )
    
    notes = models.TextField(
        blank=True,
        help_text='Additional notes'
    )
    
    class Meta:
        verbose_name = 'Waiting List Entry'
        verbose_name_plural = 'Waiting List'
        ordering = ['is_priority', 'position', 'added_at']
    
    def __str__(self):
        return f"#{self.position} - {self.application.student.user.full_name}"
