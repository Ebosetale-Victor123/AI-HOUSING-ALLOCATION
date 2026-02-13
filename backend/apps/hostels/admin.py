"""
Admin configuration for hostels app.
"""

from django.contrib import admin

from .models import Hostel, Room, BedSpace


class RoomInline(admin.TabularInline):
    """Inline admin for Room model."""
    model = Room
    extra = 0
    fields = ['room_number', 'capacity', 'current_occupancy', 'floor_level', 'room_type', 'is_accessible', 'is_active']
    readonly_fields = ['current_occupancy']


class BedSpaceInline(admin.TabularInline):
    """Inline admin for BedSpace model."""
    model = BedSpace
    extra = 0
    fields = ['space_number', 'is_occupied', 'is_active']


@admin.register(Hostel)
class HostelAdmin(admin.ModelAdmin):
    """Admin configuration for Hostel model."""
    
    list_display = [
        'name', 'code', 'gender_type', 'total_rooms',
        'warden_name', 'is_active', 'created_at'
    ]
    list_filter = ['gender_type', 'is_active', 'has_electricity', 'has_water', 'has_internet']
    search_fields = ['name', 'code', 'description', 'warden_name']
    readonly_fields = ['created_at', 'updated_at']
    inlines = [RoomInline]
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'code', 'gender_type', 'description', 'address')
        }),
        ('Management', {
            'fields': ('warden_name', 'warden_contact')
        }),
        ('Location', {
            'fields': ('location_lat', 'location_lng'),
            'classes': ('collapse',)
        }),
        ('Facilities', {
            'fields': (
                'has_electricity', 'has_water', 'has_internet',
                'has_common_room', 'has_kitchen'
            ),
            'classes': ('collapse',)
        }),
        ('Status', {
            'fields': ('is_active', 'total_rooms')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    """Admin configuration for Room model."""
    
    list_display = [
        'hostel', 'room_number', 'capacity', 'current_occupancy',
        'room_type', 'is_accessible', 'floor_level', 'is_active'
    ]
    list_filter = [
        'hostel', 'room_type', 'is_accessible',
        'is_active', 'is_under_maintenance', 'floor_level'
    ]
    search_fields = ['room_number', 'hostel__name', 'hostel__code']
    readonly_fields = ['current_occupancy', 'created_at', 'updated_at']
    inlines = [BedSpaceInline]
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('hostel', 'room_number', 'capacity', 'current_occupancy')
        }),
        ('Room Details', {
            'fields': ('floor_level', 'room_type', 'is_accessible')
        }),
        ('Facilities', {
            'fields': (
                'has_balcony', 'has_air_conditioning',
                'has_private_bathroom', 'has_furniture'
            ),
            'classes': ('collapse',)
        }),
        ('Status', {
            'fields': ('is_active', 'is_under_maintenance', 'maintenance_notes')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    actions = ['mark_under_maintenance', 'mark_available', 'reset_occupancy']
    
    def mark_under_maintenance(self, request, queryset):
        queryset.update(is_under_maintenance=True)
    mark_under_maintenance.short_description = 'Mark selected rooms as under maintenance'
    
    def mark_available(self, request, queryset):
        queryset.update(is_under_maintenance=False, is_active=True)
    mark_available.short_description = 'Mark selected rooms as available'
    
    def reset_occupancy(self, request, queryset):
        queryset.update(current_occupancy=0)
        # Also reset bed spaces
        for room in queryset:
            room.bed_spaces.update(is_occupied=False)
    reset_occupancy.short_description = 'Reset occupancy for selected rooms'


@admin.register(BedSpace)
class BedSpaceAdmin(admin.ModelAdmin):
    """Admin configuration for BedSpace model."""
    
    list_display = ['room', 'space_number', 'is_occupied', 'is_active']
    list_filter = ['is_occupied', 'is_active', 'room__hostel']
    search_fields = ['room__room_number', 'room__hostel__name']
    
    actions = ['mark_available', 'mark_occupied']
    
    def mark_available(self, request, queryset):
        queryset.update(is_occupied=False)
    mark_available.short_description = 'Mark selected bed spaces as available'
    
    def mark_occupied(self, request, queryset):
        queryset.update(is_occupied=True)
    mark_occupied.short_description = 'Mark selected bed spaces as occupied'
