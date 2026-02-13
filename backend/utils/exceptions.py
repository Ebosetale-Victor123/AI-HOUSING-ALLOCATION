"""
Custom exceptions for SmartAlloc.
"""

from rest_framework.exceptions import APIException
from rest_framework import status


class SmartAllocException(APIException):
    """Base exception for SmartAlloc."""
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    default_detail = 'An error occurred.'
    default_code = 'error'


class AllocationError(SmartAllocException):
    """Exception raised during allocation process."""
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'Allocation process failed.'
    default_code = 'allocation_error'


class InsufficientCapacityError(AllocationError):
    """Exception raised when hostel capacity is insufficient."""
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'Insufficient hostel capacity for all applicants.'
    default_code = 'insufficient_capacity'


class InvalidAllocationStateError(AllocationError):
    """Exception raised when allocation is in invalid state."""
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'Invalid allocation state.'
    default_code = 'invalid_allocation_state'


class MLModelError(SmartAllocException):
    """Exception raised when ML model fails."""
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    default_detail = 'ML model prediction failed.'
    default_code = 'ml_model_error'


class ModelNotTrainedError(MLModelError):
    """Exception raised when model is not trained."""
    status_code = status.HTTP_503_SERVICE_UNAVAILABLE
    default_detail = 'ML model is not trained yet.'
    default_code = 'model_not_trained'


class ValidationError(SmartAllocException):
    """Exception raised for validation errors."""
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'Validation error.'
    default_code = 'validation_error'


class PermissionDeniedError(SmartAllocException):
    """Exception raised for permission errors."""
    status_code = status.HTTP_403_FORBIDDEN
    default_detail = 'Permission denied.'
    default_code = 'permission_denied'


class ResourceNotFoundError(SmartAllocException):
    """Exception raised when resource is not found."""
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = 'Resource not found.'
    default_code = 'not_found'


class DuplicateApplicationError(SmartAllocException):
    """Exception raised when student submits duplicate application."""
    status_code = status.HTTP_409_CONFLICT
    default_detail = 'You have already submitted an application for this session.'
    default_code = 'duplicate_application'


class ApplicationClosedError(SmartAllocException):
    """Exception raised when application period is closed."""
    status_code = status.HTTP_403_FORBIDDEN
    default_detail = 'Application period is currently closed.'
    default_code = 'application_closed'


class RoomFullError(AllocationError):
    """Exception raised when room is at full capacity."""
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'Room is already at full capacity.'
    default_code = 'room_full'


class GenderMismatchError(AllocationError):
    """Exception raised when gender doesn't match hostel type."""
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'Student gender does not match hostel assignment.'
    default_code = 'gender_mismatch'
