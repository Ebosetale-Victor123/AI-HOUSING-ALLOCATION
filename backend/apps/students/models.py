"""
Student profile models for SmartAlloc.
"""

from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

from apps.users.models import User
from utils.constants import Gender, Level
from utils.validators import validate_gpa, validate_distance, validate_adult_age


class StudentProfile(models.Model):
    """
    Extended profile information for student users.
    """
    
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='student_profile',
        help_text='Associated user account'
    )
    
    # Academic Information
    current_gpa = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[validate_gpa],
        help_text='Current GPA (0.00 - 5.00)'
    )
    
    level = models.PositiveSmallIntegerField(
        choices=Level.choices,
        default=Level.LEVEL_100,
        help_text='Current academic level'
    )
    
    # Personal Information
    gender = models.CharField(
        max_length=1,
        choices=Gender.choices,
        help_text='Gender for hostel assignment'
    )
    
    date_of_birth = models.DateField(
        null=True,
        blank=True,
        validators=[validate_adult_age],
        help_text='Date of birth'
    )
    
    # Location Information
    home_address = models.TextField(
        blank=True,
        help_text='Home address for distance calculation'
    )
    
    distance_from_campus = models.FloatField(
        null=True,
        blank=True,
        validators=[validate_distance],
        help_text='Distance from home to campus in kilometers'
    )
    
    # Disability Information
    disability_status = models.BooleanField(
        default=False,
        help_text='Does the student have accessibility needs?'
    )
    
    disability_details = models.TextField(
        blank=True,
        help_text='Details about accessibility requirements'
    )
    
    # Financial Information
    financial_aid_status = models.BooleanField(
        default=False,
        help_text='Is the student receiving financial aid?'
    )
    
    # Emergency Contact
    emergency_contact_name = models.CharField(
        max_length=100,
        blank=True,
        help_text='Emergency contact person name'
    )
    
    emergency_contact_phone = models.CharField(
        max_length=20,
        blank=True,
        help_text='Emergency contact phone number'
    )
    
    # Medical Information
    medical_conditions = models.TextField(
        blank=True,
        help_text='Any medical conditions the housing office should be aware of'
    )
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Student Profile'
        verbose_name_plural = 'Student Profiles'
        ordering = ['-created_at']
        permissions = [
            ('can_view_all_profiles', 'Can view all student profiles'),
            ('can_export_profiles', 'Can export student profiles'),
        ]
    
    def __str__(self):
        return f"{self.user.full_name} - {self.user.matric_number or 'No Matric'}"
    
    @property
    def seniority_score(self):
        """
        Calculate seniority score based on level and GPA.
        Returns a value that can be used in priority calculation.
        """
        if self.current_gpa:
            return float(self.level) * float(self.current_gpa)
        return float(self.level)
    
    @property
    def needs_accessible_room(self):
        """Check if student needs an accessible room."""
        return self.disability_status
    
    def get_priority_factors(self):
        """
        Return a dictionary of factors used in priority calculation.
        """
        return {
            'gpa': float(self.current_gpa) if self.current_gpa else 0.0,
            'level': self.level,
            'distance': self.distance_from_campus or 0.0,
            'disability': 1 if self.disability_status else 0,
            'financial_aid': 1 if self.financial_aid_status else 0,
        }


class AcademicHistory(models.Model):
    """
    Academic history for students (for trend analysis).
    """
    
    student = models.ForeignKey(
        StudentProfile,
        on_delete=models.CASCADE,
        related_name='academic_history'
    )
    
    academic_session = models.CharField(
        max_length=9,
        help_text='Academic session (e.g., 2023/2024)'
    )
    
    gpa = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        validators=[validate_gpa],
        help_text='GPA for the session'
    )
    
    level = models.PositiveSmallIntegerField(
        choices=Level.choices,
        help_text='Level during this session'
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Academic History'
        verbose_name_plural = 'Academic Histories'
        ordering = ['-academic_session']
        unique_together = ['student', 'academic_session']
    
    def __str__(self):
        return f"{self.student.user.full_name} - {self.academic_session}"


class Document(models.Model):
    """
    Documents uploaded by students (medical certificates, etc.).
    """
    
    DOCUMENT_TYPES = [
        ('medical', 'Medical Certificate'),
        ('financial', 'Financial Aid Document'),
        ('disability', 'Disability Documentation'),
        ('other', 'Other Document'),
    ]
    
    student = models.ForeignKey(
        StudentProfile,
        on_delete=models.CASCADE,
        related_name='documents'
    )
    
    document_type = models.CharField(
        max_length=20,
        choices=DOCUMENT_TYPES,
        help_text='Type of document'
    )
    
    title = models.CharField(
        max_length=200,
        help_text='Document title'
    )
    
    file = models.FileField(
        upload_to='documents/%Y/%m/',
        help_text='Uploaded document file'
    )
    
    description = models.TextField(
        blank=True,
        help_text='Additional description'
    )
    
    is_verified = models.BooleanField(
        default=False,
        help_text='Has this document been verified by admin?'
    )
    
    verified_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='verified_documents'
    )
    
    verified_at = models.DateTimeField(null=True, blank=True)
    
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Document'
        verbose_name_plural = 'Documents'
        ordering = ['-uploaded_at']
    
    def __str__(self):
        return f"{self.title} ({self.student.user.full_name})"
