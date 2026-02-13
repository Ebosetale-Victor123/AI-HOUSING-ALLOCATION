"""
Views for Student app.
"""

from rest_framework import generics, status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.utils import timezone

from .models import StudentProfile, AcademicHistory, Document
from .serializers import (
    StudentProfileSerializer, StudentProfileCreateSerializer,
    StudentProfileUpdateSerializer, StudentProfileListSerializer,
    AcademicHistorySerializer, DocumentSerializer,
    DocumentVerificationSerializer, StudentDashboardSerializer
)
from utils.permissions import (
    IsStudent, IsAdmin, IsStudentOwner, IsOwnerOrAdmin
)
from utils.validators import document_validator
import logging

logger = logging.getLogger(__name__)


class StudentProfileView(generics.RetrieveAPIView):
    """View for retrieving own student profile."""
    
    serializer_class = StudentProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_object(self):
        """Get or create student profile for current user."""
        user = self.request.user
        
        # Only students can have profiles
        if not user.is_student:
            raise permissions.PermissionDenied(
                'Only students can have student profiles.'
            )
        
        profile, created = StudentProfile.objects.get_or_create(
            user=user,
            defaults={'gender': 'M'}  # Default gender, should be updated
        )
        
        if created:
            logger.info(f"Created student profile for user: {user.email}")
        
        return profile


class StudentProfileCreateView(generics.CreateAPIView):
    """View for creating student profile."""
    
    serializer_class = StudentProfileCreateSerializer
    permission_classes = [permissions.IsAuthenticated, IsStudent]


class StudentProfileUpdateView(generics.UpdateAPIView):
    """View for updating student profile."""
    
    serializer_class = StudentProfileUpdateSerializer
    permission_classes = [permissions.IsAuthenticated, IsStudentOwner]
    
    def get_object(self):
        return get_object_or_404(StudentProfile, user=self.request.user)
    
    def perform_update(self, serializer):
        serializer.save()
        logger.info(f"Updated student profile for user: {self.request.user.email}")


class StudentListView(generics.ListAPIView):
    """View for listing all students (admin only)."""
    
    serializer_class = StudentProfileListSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdmin]
    
    def get_queryset(self):
        """Filter students based on query params."""
        queryset = StudentProfile.objects.select_related('user').all()
        
        # Filter by level
        level = self.request.query_params.get('level')
        if level:
            queryset = queryset.filter(level=level)
        
        # Filter by gender
        gender = self.request.query_params.get('gender')
        if gender:
            queryset = queryset.filter(gender=gender)
        
        # Filter by disability status
        disability = self.request.query_params.get('disability')
        if disability is not None:
            queryset = queryset.filter(
                disability_status=disability.lower() == 'true'
            )
        
        # Filter by financial aid
        financial_aid = self.request.query_params.get('financial_aid')
        if financial_aid is not None:
            queryset = queryset.filter(
                financial_aid_status=financial_aid.lower() == 'true'
            )
        
        # Filter by department
        department = self.request.query_params.get('department')
        if department:
            queryset = queryset.filter(
                user__department__icontains=department
            )
        
        # Filter by GPA range
        min_gpa = self.request.query_params.get('min_gpa')
        if min_gpa:
            queryset = queryset.filter(current_gpa__gte=min_gpa)
        
        max_gpa = self.request.query_params.get('max_gpa')
        if max_gpa:
            queryset = queryset.filter(current_gpa__lte=max_gpa)
        
        return queryset.order_by('-user__date_joined')


class StudentDetailView(generics.RetrieveAPIView):
    """View for retrieving student details (admin or owner)."""
    
    queryset = StudentProfile.objects.select_related('user').all()
    serializer_class = StudentProfileSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrAdmin]
    lookup_field = 'pk'


class StudentDashboardView(generics.GenericAPIView):
    """View for student dashboard data."""
    
    serializer_class = StudentDashboardSerializer
    permission_classes = [permissions.IsAuthenticated, IsStudent]
    
    def get(self, request):
        """Get dashboard data for current student."""
        profile = get_object_or_404(StudentProfile, user=request.user)
        serializer = self.get_serializer(profile)
        return Response(serializer.data)


class AcademicHistoryListView(generics.ListCreateAPIView):
    """View for listing and creating academic history."""
    
    serializer_class = AcademicHistorySerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """Get academic history for current student."""
        user = self.request.user
        
        # Admins can view all
        if user.user_type in ['admin', 'super_admin']:
            student_id = self.request.query_params.get('student_id')
            if student_id:
                return AcademicHistory.objects.filter(student_id=student_id)
            return AcademicHistory.objects.all()
        
        # Students can only view their own
        try:
            profile = user.student_profile
            return AcademicHistory.objects.filter(student=profile)
        except StudentProfile.DoesNotExist:
            return AcademicHistory.objects.none()
    
    def perform_create(self, serializer):
        """Associate with student profile."""
        profile = get_object_or_404(StudentProfile, user=self.request.user)
        serializer.save(student=profile)


class DocumentListCreateView(generics.ListCreateAPIView):
    """View for listing and uploading documents."""
    
    serializer_class = DocumentSerializer
    permission_classes = [permissions.IsAuthenticated, IsStudent]
    
    def get_queryset(self):
        """Get documents for current student."""
        profile = get_object_or_404(StudentProfile, user=self.request.user)
        return Document.objects.filter(student=profile)
    
    def perform_create(self, serializer):
        """Associate document with student profile."""
        profile = get_object_or_404(StudentProfile, user=self.request.user)
        serializer.save(student=profile)
        logger.info(f"Document uploaded by student: {self.request.user.email}")


class DocumentDetailView(generics.RetrieveUpdateDestroyAPIView):
    """View for retrieving, updating, or deleting a document."""
    
    serializer_class = DocumentSerializer
    permission_classes = [permissions.IsAuthenticated, IsStudentOwner]
    
    def get_queryset(self):
        """Get documents for current student."""
        profile = get_object_or_404(StudentProfile, user=self.request.user)
        return Document.objects.filter(student=profile)
    
    def perform_destroy(self, instance):
        """Delete document file and record."""
        if instance.file:
            instance.file.delete(save=False)
        instance.delete()
        logger.info(f"Document deleted by student: {self.request.user.email}")


class DocumentVerificationView(generics.UpdateAPIView):
    """View for verifying documents (admin only)."""
    
    queryset = Document.objects.all()
    serializer_class = DocumentVerificationSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdmin]
    
    def perform_update(self, serializer):
        """Mark document as verified."""
        serializer.save(
            is_verified=True,
            verified_by=self.request.user,
            verified_at=timezone.now()
        )
        logger.info(f"Document verified by admin: {self.request.user.email}")


class StudentStatisticsView(generics.GenericAPIView):
    """View for student statistics (admin only)."""
    
    permission_classes = [permissions.IsAuthenticated, IsAdmin]
    
    def get(self, request):
        """Get student statistics."""
        from django.db.models import Avg, Count, Q
        
        total_students = StudentProfile.objects.count()
        
        # By level
        by_level = StudentProfile.objects.values('level').annotate(
            count=Count('id')
        ).order_by('level')
        
        # By gender
        by_gender = StudentProfile.objects.values('gender').annotate(
            count=Count('id')
        )
        
        # By disability status
        with_disability = StudentProfile.objects.filter(
            disability_status=True
        ).count()
        
        # By financial aid
        with_financial_aid = StudentProfile.objects.filter(
            financial_aid_status=True
        ).count()
        
        # Average GPA
        avg_gpa = StudentProfile.objects.aggregate(
            avg_gpa=Avg('current_gpa')
        )['avg_gpa'] or 0
        
        # Average distance
        avg_distance = StudentProfile.objects.aggregate(
            avg_distance=Avg('distance_from_campus')
        )['avg_distance'] or 0
        
        return Response({
            'total_students': total_students,
            'by_level': list(by_level),
            'by_gender': list(by_gender),
            'with_disability': with_disability,
            'with_financial_aid': with_financial_aid,
            'average_gpa': round(avg_gpa, 2),
            'average_distance_km': round(avg_distance, 2),
        })
