"""
Admin configuration for applications app.
"""

from django.contrib import admin

from .models import Application, ApplicationPeriod, WaitingList


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    """Admin configuration for Application model."""
    
    list_display = [
        'id', 'student', 'academic_session', 'preferred_hostel',
        'status', 'priority_score', 'application_date', 'allocation_date'
    ]
    list_filter = [
        'status', 'academic_session', 'application_date',
        'student__disability_status', 'student__financial_aid_status'
    ]
    search_fields = [
        'student__user__email', 'student__user__first_name',
        'student__user__last_name', 'student__user__matric_number'
    ]
    readonly_fields = ['application_date', 'allocation_date']
    
    fieldsets = (
        ('Student Information', {
            'fields': ('student', 'academic_session')
        }),
        ('Preferences', {
            'fields': ('preferred_hostel', 'special_requests')
        }),
        ('AI Scoring', {
            'fields': (
                'priority_score', 'ai_confidence',
                'gpa_factor', 'distance_factor',
                'level_factor', 'need_factor'
            ),
            'classes': ('collapse',)
        }),
        ('Status', {
            'fields': ('status', 'medical_certificate')
        }),
        ('Review', {
            'fields': ('reviewed_at', 'reviewed_by', 'review_notes'),
            'classes': ('collapse',)
        }),
        ('Dates', {
            'fields': ('application_date', 'allocation_date'),
            'classes': ('collapse',)
        }),
    )
    
    actions = ['mark_approved', 'mark_rejected', 'reset_priority_score']
    
    def mark_approved(self, request, queryset):
        for app in queryset:
            app.approve(reviewed_by=request.user)
    mark_approved.short_description = 'Mark selected applications as approved'
    
    def mark_rejected(self, request, queryset):
        for app in queryset:
            app.reject(reviewed_by=request.user)
    mark_rejected.short_description = 'Mark selected applications as rejected'
    
    def reset_priority_score(self, request, queryset):
        queryset.update(
            priority_score=None,
            ai_confidence=None,
            gpa_factor=None,
            distance_factor=None,
            level_factor=None,
            need_factor=None
        )
    reset_priority_score.short_description = 'Reset AI priority scores'


@admin.register(ApplicationPeriod)
class ApplicationPeriodAdmin(admin.ModelAdmin):
    """Admin configuration for ApplicationPeriod model."""
    
    list_display = [
        'name', 'academic_session', 'start_date', 'end_date',
        'is_active', 'allow_new_applications'
    ]
    list_filter = ['is_active', 'allow_new_applications']
    search_fields = ['name', 'academic_session']
    
    actions = ['activate_period', 'deactivate_period']
    
    def activate_period(self, request, queryset):
        if queryset.count() == 1:
            period = queryset.first()
            period.is_active = True
            period.save()
    activate_period.short_description = 'Activate selected period'
    
    def deactivate_period(self, request, queryset):
        queryset.update(is_active=False)
    deactivate_period.short_description = 'Deactivate selected periods'


@admin.register(WaitingList)
class WaitingListAdmin(admin.ModelAdmin):
    """Admin configuration for WaitingList model."""
    
    list_display = ['position', 'application', 'is_priority', 'added_at']
    list_filter = ['is_priority', 'added_at']
    search_fields = [
        'application__student__user__email',
        'application__student__user__matric_number'
    ]
    ordering = ['position']
