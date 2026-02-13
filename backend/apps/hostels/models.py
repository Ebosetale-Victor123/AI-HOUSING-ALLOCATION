"""
Hostel and Room models for SmartAlloc.
"""

from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

from utils.constants import HostelGenderType, RoomType
from utils.validators import RoomCapacityValidator


class Hostel(models.Model):
    """
    Hostel building model.
    """
    
    name = models.CharField(
        max_length=100,
        unique=True,
        help_text='Name of the hostel'
    )
    
    code = models.CharField(
        max_length=10,
        unique=True,
        help_text='Short code for the hostel (e.g., HH1)'
    )
    
    gender_type = models.CharField(
        max_length=10,
        choices=HostelGenderType.choices,
        help_text='Gender assignment for this hostel'
    )
    
    description = models.TextField(
        blank=True,
        help_text='Description of the hostel'
    )
    
    address = models.TextField(
        blank=True,
        help_text='Physical address of the hostel'
    )
    
    total_rooms = models.PositiveIntegerField(
        default=0,
        help_text='Total number of rooms'
    )
    
    warden_name = models.CharField(
        max_length=100,
        blank=True,
        help_text='Name of the hostel warden'
    )
    
    warden_contact = models.CharField(
        max_length=20,
        blank=True,
        help_text='Contact number for the warden'
    )
    
    # Geographic coordinates (optional, for distance calculations)
    location_lat = models.FloatField(
        null=True,
        blank=True,
        help_text='Latitude coordinate'
    )
    
    location_lng = models.FloatField(
        null=True,
        blank=True,
        help_text='Longitude coordinate'
    )
    
    # Facilities
    has_electricity = models.BooleanField(
        default=True,
        help_text='Does the hostel have stable electricity?'
    )
    
    has_water = models.BooleanField(
        default=True,
        help_text='Does the hostel have running water?'
    )
    
    has_internet = models.BooleanField(
        default=True,
        help_text='Does the hostel have internet access?'
    )
    
    has_common_room = models.BooleanField(
        default=False,
        help_text='Does the hostel have a common room?'
    )
    
    has_kitchen = models.BooleanField(
        default=False,
        help_text='Does the hostel have a kitchen facility?'
    )
    
    # Status
    is_active = models.BooleanField(
        default=True,
        help_text='Is the hostel currently active?'
    )
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Hostel'
        verbose_name_plural = 'Hostels'
        ordering = ['name']
    
    def __str__(self):
        return f"{self.name} ({self.code})"
    
    @property
    def total_capacity(self):
        """Calculate total capacity across all rooms."""
        return sum(room.capacity for room in self.rooms.all())
    
    @property
    def current_occupancy(self):
        """Calculate current total occupancy."""
        return sum(room.current_occupancy for room in self.rooms.all())
    
    @property
    def available_spaces(self):
        """Calculate available spaces."""
        return self.total_capacity - self.current_occupancy
    
    @property
    def occupancy_rate(self):
        """Calculate occupancy rate as percentage."""
        total = self.total_capacity
        if total == 0:
            return 0
        return (self.current_occupancy / total) * 100
    
    def update_total_rooms(self):
        """Update total_rooms count from related rooms."""
        self.total_rooms = self.rooms.count()
        self.save(update_fields=['total_rooms'])


class Room(models.Model):
    """
    Individual room model within a hostel.
    """
    
    hostel = models.ForeignKey(
        Hostel,
        on_delete=models.CASCADE,
        related_name='rooms',
        help_text='The hostel this room belongs to'
    )
    
    room_number = models.CharField(
        max_length=20,
        help_text='Room number (e.g., 101, A12)'
    )
    
    capacity = models.PositiveSmallIntegerField(
        default=4,
        validators=[RoomCapacityValidator()],
        help_text='Maximum number of students'
    )
    
    current_occupancy = models.PositiveSmallIntegerField(
        default=0,
        help_text='Current number of occupants'
    )
    
    floor_level = models.PositiveSmallIntegerField(
        default=1,
        help_text='Floor level (1 = ground floor)'
    )
    
    room_type = models.CharField(
        max_length=20,
        choices=RoomType.choices,
        default=RoomType.STANDARD,
        help_text='Type of room'
    )
    
    is_accessible = models.BooleanField(
        default=False,
        help_text='Is this room accessible for students with disabilities?'
    )
    
    # Room facilities
    has_balcony = models.BooleanField(default=False)
    has_air_conditioning = models.BooleanField(default=False)
    has_private_bathroom = models.BooleanField(default=False)
    has_furniture = models.BooleanField(default=True)
    
    # Status
    is_active = models.BooleanField(
        default=True,
        help_text='Is the room available for allocation?'
    )
    
    is_under_maintenance = models.BooleanField(
        default=False,
        help_text='Is the room currently under maintenance?'
    )
    
    maintenance_notes = models.TextField(
        blank=True,
        help_text='Notes about maintenance'
    )
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Room'
        verbose_name_plural = 'Rooms'
        ordering = ['hostel', 'floor_level', 'room_number']
        unique_together = ['hostel', 'room_number']
    
    def __str__(self):
        return f"{self.hostel.code} - Room {self.room_number}"
    
    @property
    def available_spaces(self):
        """Calculate available bed spaces."""
        return self.capacity - self.current_occupancy
    
    @property
    def is_full(self):
        """Check if room is at full capacity."""
        return self.current_occupancy >= self.capacity
    
    @property
    def is_available(self):
        """Check if room is available for allocation."""
        return (
            self.is_active and
            not self.is_under_maintenance and
            not self.is_full
        )
    
    def can_accommodate(self, count=1):
        """Check if room can accommodate additional students."""
        return self.available_spaces >= count
    
    def increment_occupancy(self, count=1):
        """Increase occupancy count."""
        if self.can_accommodate(count):
            self.current_occupancy += count
            self.save(update_fields=['current_occupancy'])
            return True
        return False
    
    def decrement_occupancy(self, count=1):
        """Decrease occupancy count."""
        if self.current_occupancy >= count:
            self.current_occupancy -= count
            self.save(update_fields=['current_occupancy'])
            return True
        return False


class BedSpace(models.Model):
    """
    Individual bed space within a room.
    """
    
    room = models.ForeignKey(
        Room,
        on_delete=models.CASCADE,
        related_name='bed_spaces',
        help_text='The room this bed space belongs to'
    )
    
    space_number = models.PositiveSmallIntegerField(
        help_text='Bed space number within the room (1, 2, 3, etc.)'
    )
    
    is_occupied = models.BooleanField(
        default=False,
        help_text='Is this bed space currently occupied?'
    )
    
    is_active = models.BooleanField(
        default=True,
        help_text='Is this bed space available for allocation?'
    )
    
    notes = models.TextField(
        blank=True,
        help_text='Additional notes about this bed space'
    )
    
    class Meta:
        verbose_name = 'Bed Space'
        verbose_name_plural = 'Bed Spaces'
        ordering = ['room', 'space_number']
        unique_together = ['room', 'space_number']
    
    def __str__(self):
        return f"{self.room} - Bed {self.space_number}"
    
    def allocate(self):
        """Mark bed space as occupied."""
        if not self.is_occupied and self.is_active:
            self.is_occupied = True
            self.save(update_fields=['is_occupied'])
            # Update room occupancy
            self.room.increment_occupancy()
            return True
        return False
    
    def deallocate(self):
        """Mark bed space as available."""
        if self.is_occupied:
            self.is_occupied = False
            self.save(update_fields=['is_occupied'])
            # Update room occupancy
            self.room.decrement_occupancy()
            return True
        return False
