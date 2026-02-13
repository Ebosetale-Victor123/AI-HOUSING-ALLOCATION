"""
Admin configuration for allocation app.
"""

from django.contrib import admin

from .models import Allocation, AuditLog, AllocationRun


@admin.register(Allocation)
class AllocationAdmin(admin.ModelAdmin):
    """Admin configuration for Allocation model."""
    
    list_display = [
        'id', 'student', 'room', 'bed_space_number',
        'allocated_by', 'is_confirmed', 'is_active', 'created_at'
    ]
    list_filter = [
        'allocated_by', 'admin_override', 'is_confirmed',
        'is_active', 'created_at'
    ]
    search_fields = [
        'application__student__user__email',
        'application__student__user__matric_number',
        'room__room_number'
    ]
    readonly_fields = ['created_at', 'updated_at', 'confirmed_at']
    
    fieldsets = (
        ('Application', {
            'fields': ('application',)
        }),
        ('Room Assignment', {
            'fields': ('room', 'bed_space', 'bed_space_number')
        }),
        ('Allocation Details', {
            'fields': (
                'allocated_by', 'allocated_by_user',
                'allocation_reason', 'admin_override'
            )
        }),
        ('Confirmation', {
            'fields': ('is_confirmed', 'confirmed_at')
        }),
        ('Status', {
            'fields': ('is_active', 'cancelled_at', 'cancellation_reason')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    actions = ['mark_confirmed', 'mark_cancelled']
    
    def student(self, obj):
        return obj.application.student.user.full_name
    student.short_description = 'Student'
    
    def mark_confirmed(self, request, queryset):
        from django.utils import timezone
        queryset.update(is_confirmed=True, confirmed_at=timezone.now())
    mark_confirmed.short_description = 'Mark selected allocations as confirmed'
    
    def mark_cancelled(self, request, queryset):
        from django.utils import timezone
        queryset.update(is_active=False, cancelled_at=timezone.now())
    mark_cancelled.short_description = 'Mark selected allocations as cancelled'


@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    """Admin configuration for AuditLog model."""
    
    list_display = [
        'action', 'user', 'timestamp', 'model_version'
    ]
    list_filter = ['action', 'model_version', 'timestamp']
    search_fields = ['user__email', 'details']
    readonly_fields = ['timestamp']
    
    def has_add_permission(self, request):
        return False
    
    def has_change_permission(self, request, obj=None):
        return False


@admin.register(AllocationRun)
class AllocationRunAdmin(admin.ModelAdmin):
    """Admin configuration for AllocationRun model."""
    
    list_display = [
        'id', 'academic_session', 'status', 'started_by',
        'started_at', 'total_applications', 'successful_allocations'
    ]
    list_filter = ['status', 'started_at']
    search_fields = ['academic_session', 'error_message']
    readonly_fields = [
        'started_at', 'completed_at', 'celery_task_id'
    ]
    
    actions = ['mark_cancelled']
    
    def mark_cancelled(self, request, queryset):
        queryset.filter(status='PENDING').update(status='CANCELLED')
    mark_cancelled.short_description = 'Cancel selected pending runs'


