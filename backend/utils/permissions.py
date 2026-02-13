"""
Custom permission classes for SmartAlloc.
"""

from rest_framework import permissions


class IsSuperAdmin(permissions.BasePermission):
    """Permission for Super Admin users."""
    
    def has_permission(self, request, view):
        return (
            request.user and 
            request.user.is_authenticated and 
            request.user.user_type == 'super_admin'
        )


class IsAdmin(permissions.BasePermission):
    """Permission for Admin users (includes Super Admin)."""
    
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        return request.user.user_type in ['admin', 'super_admin']


class IsHousingOfficer(permissions.BasePermission):
    """Permission for Housing Officers (Admin or Super Admin)."""
    
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        return request.user.user_type in ['admin', 'super_admin']


class IsStudent(permissions.BasePermission):
    """Permission for Student users."""
    
    def has_permission(self, request, view):
        return (
            request.user and 
            request.user.is_authenticated and 
            request.user.user_type == 'student'
        )


class IsOwnerOrAdmin(permissions.BasePermission):
    """
    Permission that allows users to access their own objects,
    while admins can access all objects.
    """
    
    def has_object_permission(self, request, view, obj):
        # Admin can access all
        if request.user.user_type in ['admin', 'super_admin']:
            return True
        
        # Check if object has a user attribute
        if hasattr(obj, 'user'):
            return obj.user == request.user
        
        # Check if object is a user
        if hasattr(obj, 'id') and hasattr(request.user, 'id'):
            return obj.id == request.user.id
        
        return False


class ReadOnly(permissions.BasePermission):
    """Permission for read-only access."""
    
    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS


class IsAdminOrReadOnly(permissions.BasePermission):
    """Permission for admin write access, everyone can read."""
    
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return (
            request.user and 
            request.user.is_authenticated and 
            request.user.user_type in ['admin', 'super_admin']
        )


class IsStudentOwner(permissions.BasePermission):
    """
    Permission that allows students to only access their own data.
    """
    
    def has_object_permission(self, request, view, obj):
        if not request.user or not request.user.is_authenticated:
            return False
        
        # Admins can access all
        if request.user.user_type in ['admin', 'super_admin']:
            return True
        
        # Students can only access their own data
        if request.user.user_type == 'student':
            if hasattr(obj, 'user'):
                return obj.user == request.user
            if hasattr(obj, 'student'):
                return obj.student.user == request.user
        
        return False
