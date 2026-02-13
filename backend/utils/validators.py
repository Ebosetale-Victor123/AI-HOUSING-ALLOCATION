"""
Custom validators for SmartAlloc.
"""

import re
from datetime import date
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
from django.utils.deconstruct import deconstructible
import phonenumbers


def validate_matric_number(value):
    """
    Validate matriculation number format.
    Expected format: DEP/YYYY/XXXX or similar patterns
    """
    if not value:
        return
    
    # Common matric number patterns
    patterns = [
        r'^[A-Z]{3}/\d{4}/\d{4}$',  # e.g., CSC/2024/001
        r'^[A-Z]{3}/\d{4}/\d{3}$',  # e.g., CSC/2024/001
        r'^\d{4}/\d{6}$',           # e.g., 2024/123456
        r'^[A-Z]{2}/\d{4}/\d{5}$',  # e.g., EE/2024/12345
    ]
    
    value = value.upper().strip()
    
    if not any(re.match(pattern, value) for pattern in patterns):
        raise ValidationError(
            'Invalid matric number format. Expected formats: '
            'DEP/YYYY/XXXX, YYYY/XXXXXX, or similar.'
        )


def validate_academic_session(value):
    """
    Validate academic session format (YYYY/YYYY).
    e.g., "2024/2025"
    """
    if not value:
        return
    
    pattern = r'^\d{4}/\d{4}$'
    if not re.match(pattern, value):
        raise ValidationError(
            'Invalid academic session format. Expected: "YYYY/YYYY" (e.g., "2024/2025")'
        )
    
    # Validate that years are consecutive
    try:
        year1, year2 = map(int, value.split('/'))
        if year2 != year1 + 1:
            raise ValidationError(
                'Academic session years must be consecutive (e.g., "2024/2025")'
            )
        if year1 < 2000 or year1 > 2100:
            raise ValidationError(
                'Academic session year must be between 2000 and 2100'
            )
    except ValueError:
        raise ValidationError('Invalid academic session format.')


def validate_gpa(value):
    """
    Validate GPA is within valid range (0.0 - 5.0).
    """
    if value is None:
        return
    
    if not isinstance(value, (int, float)):
        raise ValidationError('GPA must be a number.')
    
    if value < 0.0 or value > 5.0:
        raise ValidationError('GPA must be between 0.0 and 5.0.')


def validate_phone_number(value):
    """
    Validate international phone number format.
    """
    if not value:
        return
    
    try:
        phone_number = phonenumbers.parse(value, None)
        if not phonenumbers.is_valid_number(phone_number):
            raise ValidationError('Invalid phone number format.')
    except phonenumbers.NumberParseException:
        raise ValidationError('Invalid phone number format. Include country code (e.g., +234).')


def validate_distance(value):
    """
    Validate distance is non-negative and within reasonable range.
    """
    if value is None:
        return
    
    if not isinstance(value, (int, float)):
        raise ValidationError('Distance must be a number.')
    
    if value < 0:
        raise ValidationError('Distance cannot be negative.')
    
    if value > 20000:  # Max 20,000 km (earth's circumference is ~40,000 km)
        raise ValidationError('Distance seems unrealistic. Please verify.')


def validate_future_date(value):
    """
    Validate that a date is not in the future.
    """
    if value and value > date.today():
        raise ValidationError('Date cannot be in the future.')


def validate_past_date(value):
    """
    Validate that a date is not in the past (for deadlines, etc.).
    """
    if value and value < date.today():
        raise ValidationError('Date cannot be in the past.')


def validate_adult_age(value):
    """
    Validate that person is at least 16 years old.
    """
    if not value:
        return
    
    today = date.today()
    age = today.year - value.year - ((today.month, today.day) < (value.month, value.day))
    
    if age < 16:
        raise ValidationError('Student must be at least 16 years old.')
    
    if age > 100:
        raise ValidationError('Please verify the date of birth.')


# File validators
document_validator = FileExtensionValidator(
    allowed_extensions=['pdf', 'jpg', 'jpeg', 'png'],
    message='Only PDF, JPG, JPEG, and PNG files are allowed.'
)


def validate_file_size(file):
    """
    Validate file size is under 5MB.
    """
    max_size_mb = 5
    max_size_bytes = max_size_mb * 1024 * 1024
    
    if file.size > max_size_bytes:
        raise ValidationError(f'File size must be under {max_size_mb}MB.')


@deconstructible
class RoomCapacityValidator:
    """
    Validate that room capacity is within hostel limits.
    """
    
    def __call__(self, value):
        if value is None:
            return
        
        if not isinstance(value, int):
            raise ValidationError('Capacity must be an integer.')
        
        if value < 1:
            raise ValidationError('Capacity must be at least 1.')
        
        if value > 8:
            raise ValidationError('Capacity cannot exceed 8.')
    
    def __eq__(self, other):
        return isinstance(other, self.__class__)
