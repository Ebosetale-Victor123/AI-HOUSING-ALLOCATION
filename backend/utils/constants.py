"""
Constants and enums for the SmartAlloc system.
"""

from django.db import models


class UserType(models.TextChoices):
    """User role types."""
    STUDENT = 'student', 'Student'
    ADMIN = 'admin', 'Admin'
    SUPER_ADMIN = 'super_admin', 'Super Admin'


class Gender(models.TextChoices):
    """Gender choices."""
    MALE = 'M', 'Male'
    FEMALE = 'F', 'Female'


class Level(models.IntegerChoices):
    """Academic levels."""
    LEVEL_100 = 100, '100 Level'
    LEVEL_200 = 200, '200 Level'
    LEVEL_300 = 300, '300 Level'
    LEVEL_400 = 400, '400 Level'
    LEVEL_500 = 500, '500 Level'


class HostelGenderType(models.TextChoices):
    """Hostel gender assignment."""
    MALE = 'male', 'Male'
    FEMALE = 'female', 'Female'
    MIXED = 'mixed', 'Mixed'


class RoomType(models.TextChoices):
    """Room types."""
    STANDARD = 'standard', 'Standard'
    PREMIUM = 'premium', 'Premium'
    MEDICAL = 'medical', 'Medical'


class ApplicationStatus(models.TextChoices):
    """Application lifecycle statuses."""
    PENDING = 'pending', 'Pending'
    APPROVED = 'approved', 'Approved'
    REJECTED = 'rejected', 'Rejected'
    ALLOCATED = 'allocated', 'Allocated'
    CANCELLED = 'cancelled', 'Cancelled'


class AllocationStatus(models.TextChoices):
    """Allocation statuses."""
    PENDING = 'pending', 'Pending'
    CONFIRMED = 'confirmed', 'Confirmed'
    DECLINED = 'declined', 'Declined'
    COMPLETED = 'completed', 'Completed'


# Allocation Algorithm Constraints
ALLOCATION_CONSTRAINTS = {
    'gender_strict': True,        # No mixed-gender hostels
    'disability_priority': True,  # Auto top-score for disabled
    'seniority_boost': 1.2,       # Multiplier for 400/500 level
    'max_distance_cap': 500,      # Max km for scoring
    'room_capacity_strict': True, # No overbooking
    'default_room_capacity': 4,   # Default room capacity
    'max_occupancy_buffer': 0,    # No overbooking allowed
}

# Priority Score Weights (for synthetic data generation and validation)
PRIORITY_WEIGHTS = {
    'gpa': 0.40,                  # 40% weight for GPA
    'distance': 0.30,             # 30% weight for distance
    'level': 0.20,                # 20% weight for academic level
    'need_based': 0.10,           # 10% weight for need-based factors
}

# Score Ranges
MIN_PRIORITY_SCORE = 0.0
MAX_PRIORITY_SCORE = 100.0
MIN_GPA = 0.0
MAX_GPA = 5.0

# Default Pagination
DEFAULT_PAGE_SIZE = 20
MAX_PAGE_SIZE = 100

# File Upload Limits
MAX_FILE_SIZE_MB = 5
ALLOWED_DOCUMENT_TYPES = ['.pdf', '.jpg', '.jpeg', '.png']

# Academic Sessions
ACADEMIC_SESSION_PATTERN = r'^\d{4}/\d{4}$'  # e.g., "2024/2025"
DEFAULT_ACADEMIC_SESSION = "2024/2025"
