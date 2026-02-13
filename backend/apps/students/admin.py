"""
Admin configuration for students app.
"""

from django.contrib import admin

from .models import StudentProfile, AcademicHistory, Document


@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    """Admin configuration for StudentProfile model."""
    
    list_display = [
        'user', 'level', 'gender', 'current_gpa',
        'disability_status', 'financial_aid_status',
        'distance_from_campus', 'created_at'
    ]
    list_filter = [
        'level', 'gender', 'disability_status',
        'financial_aid_status', 'created_at'
    ]
    search_fields = [
        'user__email', 'user__first_name', 'user__last_name',
        'user__matric_number'
    ]
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('User Information', {
            'fields': ('user',)
        }),
        ('Academic Information', {
            'fields': ('current_gpa', 'level')
        }),
        ('Personal Information', {
            'fields': ('gender', 'date_of_birth', 'home_address', 'distance_from_campus')
        }),
        ('Special Needs', {
            'fields': ('disability_status', 'disability_details', 'financial_aid_status'),
            'classes': ('collapse',)
        }),
        ('Emergency Contact', {
            'fields': ('emergency_contact_name', 'emergency_contact_phone'),
            'classes': ('collapse',)
        }),
        ('Medical Information', {
            'fields': ('medical_conditions',),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(AcademicHistory)
class AcademicHistoryAdmin(admin.ModelAdmin):
    """Admin configuration for AcademicHistory model."""
    
    list_display = ['student', 'academic_session', 'gpa', 'level']
    list_filter = ['academic_session', 'level']
    search_fields = [
        'student__user__email', 'student__user__matric_number'
    ]


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    """Admin configuration for Document model."""
    
    list_display = [
        'title', 'student', 'document_type',
        'is_verified', 'verified_by', 'uploaded_at'
    ]
    list_filter = ['document_type', 'is_verified', 'uploaded_at']
    search_fields = [
        'title', 'student__user__email', 'student__user__matric_number'
    ]
    readonly_fields = ['uploaded_at']
    
    actions = ['verify_documents']
    
    def verify_documents(self, request, queryset):
        """Bulk verify documents."""
        from django.utils import timezone
        updated = queryset.update(
            is_verified=True,
            verified_by=request.user,
            verified_at=timezone.now()
        )
        self.message_user(request, f'{updated} documents were verified.')
    verify_documents.short_description = 'Verify selected documents'
