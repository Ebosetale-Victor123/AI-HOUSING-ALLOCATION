"""
Views for Applications app.
"""

from rest_framework import generics, status, filters, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Count, Avg, Q
from django.shortcuts import get_object_or_404
from django.utils import timezone

from .models import Application, ApplicationPeriod, WaitingList
from .serializers import (
    ApplicationSerializer, ApplicationCreateSerializer,
    ApplicationUpdateSerializer, ApplicationListSerializer,
    ApplicationReviewSerializer, ApplicationPeriodSerializer,
    WaitingListSerializer, ApplicationStatisticsSerializer
)
from utils.permissions import (
    IsStudent, IsAdmin, IsStudentOwner, IsOwnerOrAdmin, IsAdminOrReadOnly
)
from utils.exceptions import DuplicateApplicationError, ApplicationClosedError
import logging

logger = logging.getLogger(__name__)


class ApplicationSubmitView(generics.CreateAPIView):
    """View for submitting housing applications."""
    
    serializer_class = ApplicationCreateSerializer
    permission_classes = [permissions.IsAuthenticated, IsStudent]
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        application = serializer.save()
        
        logger.info(
            f"Application submitted by student: {request.user.email} "
            f"for session: {application.academic_session}"
        )
        
        return Response(
            ApplicationSerializer(application).data,
            status=status.HTTP_201_CREATED
        )


class ApplicationListView(generics.ListAPIView):
    """View for listing applications (admin) or own applications (student)."""
    
    serializer_class = ApplicationListSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'academic_session', 'preferred_hostel']
    search_fields = [
        'student__user__first_name', 'student__user__last_name',
        'student__user__matric_number', 'student__user__email'
    ]
    ordering_fields = ['application_date', 'priority_score', 'status']
    ordering = ['-application_date']
    
    def get_queryset(self):
        """Filter applications based on user type."""
        user = self.request.user
        
        # Admins can see all applications
        if user.user_type in ['admin', 'super_admin']:
            queryset = Application.objects.select_related(
                'student', 'student__user', 'preferred_hostel'
            ).all()
        else:
            # Students can only see their own
            try:
                profile = user.student_profile
                queryset = Application.objects.filter(student=profile)
            except:
                return Application.objects.none()
        
        # Additional filters
        has_medical = self.request.query_params.get('has_medical')
        if has_medical is not None:
            if has_medical.lower() == 'true':
                queryset = queryset.exclude(medical_certificate='')
            else:
                queryset = queryset.filter(medical_certificate='')
        
        min_score = self.request.query_params.get('min_score')
        if min_score:
            queryset = queryset.filter(priority_score__gte=min_score)
        
        max_score = self.request.query_params.get('max_score')
        if max_score:
            queryset = queryset.filter(priority_score__lte=max_score)
        
        return queryset


class ApplicationDetailView(generics.RetrieveAPIView):
    """View for retrieving application details."""
    
    queryset = Application.objects.select_related(
        'student', 'student__user', 'preferred_hostel', 'reviewed_by'
    )
    serializer_class = ApplicationSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrAdmin]


class ApplicationStatusView(generics.GenericAPIView):
    """View for checking application status."""
    
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        """Get status of current user's application."""
        user = request.user
        
        if not user.is_student:
            return Response(
                {'error': 'Only students can have applications'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        academic_session = request.query_params.get(
            'session', ApplicationPeriod.objects.filter(
                is_active=True
            ).first()
        )
        
        if not academic_session:
            return Response(
                {'error': 'No active application period'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        try:
            application = Application.objects.get(
                student=user.student_profile,
                academic_session=academic_session
            )
            return Response(ApplicationSerializer(application).data)
        except Application.DoesNotExist:
            return Response({
                'has_application': False,
                'message': 'No application found for this session'
            })


class ApplicationReviewView(generics.GenericAPIView):
    """View for reviewing applications (admin only)."""
    
    permission_classes = [permissions.IsAuthenticated, IsAdmin]
    
    def post(self, request, pk):
        """Review an application."""
        application = get_object_or_404(Application, pk=pk)
        
        serializer = ApplicationReviewSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        action = serializer.validated_data['action']
        notes = serializer.validated_data.get('notes', '')
        
        if action == 'approve':
            application.approve(reviewed_by=request.user, notes=notes)
            message = 'Application approved successfully'
        else:
            application.reject(reviewed_by=request.user, notes=notes)
            message = 'Application rejected'
        
        logger.info(
            f"Application {application.id} {action}d by {request.user.email}"
        )
        
        return Response({
            'message': message,
            'application': ApplicationSerializer(application).data
        })


class ApplicationPeriodListCreateView(generics.ListCreateAPIView):
    """View for listing and creating application periods."""
    
    queryset = ApplicationPeriod.objects.all()
    serializer_class = ApplicationPeriodSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['is_active', 'academic_session']
    ordering = ['-start_date']


class ApplicationPeriodDetailView(generics.RetrieveUpdateDestroyAPIView):
    """View for retrieving, updating, or deleting application periods."""
    
    queryset = ApplicationPeriod.objects.all()
    serializer_class = ApplicationPeriodSerializer
    permission_classes = [IsAdminOrReadOnly]


class CurrentApplicationPeriodView(generics.GenericAPIView):
    """View for getting current active application period."""
    
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        """Get current active period."""
        try:
            period = ApplicationPeriod.objects.get(is_active=True)
            return Response(ApplicationPeriodSerializer(period).data)
        except ApplicationPeriod.DoesNotExist:
            return Response(
                {'error': 'No active application period'},
                status=status.HTTP_404_NOT_FOUND
            )


class WaitingListView(generics.ListAPIView):
    """View for viewing waiting list."""
    
    serializer_class = WaitingListSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdmin]
    
    def get_queryset(self):
        """Get waiting list entries."""
        return WaitingList.objects.select_related(
            'application', 'application__student', 'application__student__user'
        ).all()


class ApplicationStatisticsView(generics.GenericAPIView):
    """View for application statistics."""
    
    permission_classes = [permissions.IsAuthenticated, IsAdmin]
    
    def get(self, request):
        """Get application statistics."""
        academic_session = request.query_params.get('session')
        
        queryset = Application.objects.all()
        if academic_session:
            queryset = queryset.filter(academic_session=academic_session)
        
        total = queryset.count()
        
        # By status
        by_status = queryset.values('status').annotate(
            count=Count('id')
        ).order_by('status')
        
        # By level
        by_level = queryset.values('student__level').annotate(
            count=Count('id')
        ).order_by('student__level')
        
        # By gender
        by_gender = queryset.values('student__gender').annotate(
            count=Count('id')
        ).order_by('student__gender')
        
        # With disability
        with_disability = queryset.filter(
            student__disability_status=True
        ).count()
        
        # With financial aid
        with_financial_aid = queryset.filter(
            student__financial_aid_status=True
        ).count()
        
        # Average priority score
        avg_score = queryset.aggregate(
            avg_score=Avg('priority_score')
        )['avg_score'] or 0
        
        # Top 10 scorers
        top_scorers = queryset.exclude(
            priority_score__isnull=True
        ).order_by('-priority_score')[:10].values(
            'id',
            'student__user__first_name',
            'student__user__last_name',
            'student__user__matric_number',
            'priority_score'
        )
        
        data = {
            'total_applications': total,
            'by_status': list(by_status),
            'by_level': list(by_level),
            'by_gender': list(by_gender),
            'with_disability': with_disability,
            'with_financial_aid': with_financial_aid,
            'average_priority_score': round(avg_score, 2),
            'top_scorers': list(top_scorers),
        }
        
        return Response(data)


class BulkApplicationActionView(generics.GenericAPIView):
    """View for bulk actions on applications (admin only)."""
    
    permission_classes = [permissions.IsAuthenticated, IsAdmin]
    
    def post(self, request):
        """Perform bulk action on applications."""
        action = request.data.get('action')
        application_ids = request.data.get('application_ids', [])
        
        if not application_ids:
            return Response(
                {'error': 'No application IDs provided'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        applications = Application.objects.filter(id__in=application_ids)
        
        if action == 'approve':
            count = 0
            for app in applications:
                app.approve(reviewed_by=request.user)
                count += 1
            return Response({
                'message': f'{count} applications approved successfully'
            })
        
        elif action == 'reject':
            count = 0
            for app in applications:
                app.reject(reviewed_by=request.user)
                count += 1
            return Response({
                'message': f'{count} applications rejected successfully'
            })
        
        else:
            return Response(
                {'error': 'Invalid action'},
                status=status.HTTP_400_BAD_REQUEST
            )


# Import at the end to avoid circular import
from rest_framework import permissions
from utils.permissions import IsAdminOrReadOnly
