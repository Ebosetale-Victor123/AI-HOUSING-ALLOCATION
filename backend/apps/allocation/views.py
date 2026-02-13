"""
Views for Allocation app.
"""

from rest_framework import generics, status, filters
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404

from .models import Allocation, AuditLog, AllocationRun
from apps.applications.models import WaitingList
from .serializers import (
    AllocationSerializer, AllocationListSerializer, AllocationCreateSerializer,
    ManualAllocationSerializer, AuditLogSerializer, AllocationRunSerializer,
    StartAllocationRunSerializer, WaitingListSerializer,
    MLModelStatusSerializer, PriorityScoreRequestSerializer,
    PriorityScoreResponseSerializer
)
from .tasks import run_batch_allocation, send_allocation_notifications
from .allocation_engine import AllocationEngine
from .ml_models.predictor import get_predictor
from utils.permissions import IsAdmin, IsAdminOrReadOnly, IsStudentOwner
import logging

logger = logging.getLogger(__name__)


class AllocationListView(generics.ListAPIView):
    """View for listing allocations."""
    
    serializer_class = AllocationListSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['room__hostel', 'is_confirmed', 'is_active', 'allocated_by']
    search_fields = [
        'application__student__user__first_name',
        'application__student__user__last_name',
        'application__student__user__matric_number'
    ]
    ordering_fields = ['created_at', 'application__priority_score']
    ordering = ['-created_at']
    
    def get_queryset(self):
        """Filter allocations based on user type."""
        user = self.request.user
        
        if user.user_type in ['admin', 'super_admin']:
            queryset = Allocation.objects.select_related(
                'application', 'application__student', 'application__student__user',
                'room', 'room__hostel'
            ).all()
        else:
            # Students can only see their own allocation
            try:
                profile = user.student_profile
                queryset = Allocation.objects.filter(
                    application__student=profile
                ).select_related('room', 'room__hostel')
            except:
                return Allocation.objects.none()
        
        return queryset


class AllocationDetailView(generics.RetrieveAPIView):
    """View for retrieving allocation details."""
    
    queryset = Allocation.objects.select_related(
        'application', 'room', 'allocated_by_user'
    )
    serializer_class = AllocationSerializer
    permission_classes = [IsAdminOrReadOnly]


class AllocationCreateView(generics.CreateAPIView):
    """View for creating manual allocations (admin only)."""
    
    serializer_class = AllocationCreateSerializer
    permission_classes = [IsAdmin]
    
    def perform_create(self, serializer):
        """Create allocation with admin tracking."""
        allocation = serializer.save(
            allocated_by='Admin_User',
            allocated_by_user=self.request.user
        )
        
        # Mark application as allocated
        allocation.application.mark_allocated()
        
        # Update bed space
        if allocation.bed_space:
            allocation.bed_space.allocate()
        else:
            allocation.room.increment_occupancy()
        
        logger.info(
            f"Manual allocation created by {self.request.user.email}: "
            f"App {allocation.application.id} -> Room {allocation.room.id}"
        )


class AllocationConfirmView(generics.GenericAPIView):
    """View for students to confirm their allocation."""
    
    permission_classes = [IsStudentOwner]
    
    def post(self, request, pk):
        """Confirm allocation."""
        allocation = get_object_or_404(Allocation, pk=pk)
        
        # Verify ownership
        if allocation.application.student.user != request.user:
            return Response(
                {'error': 'You can only confirm your own allocation'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        allocation.confirm()
        
        logger.info(f"Allocation {pk} confirmed by student")
        
        return Response({
            'message': 'Allocation confirmed successfully',
            'allocation': AllocationSerializer(allocation).data
        })


class AllocationCancelView(generics.GenericAPIView):
    """View for cancelling allocations (admin only)."""
    
    permission_classes = [IsAdmin]
    
    def post(self, request, pk):
        """Cancel allocation."""
        allocation = get_object_or_404(Allocation, pk=pk)
        
        reason = request.data.get('reason', '')
        allocation.cancel(reason=reason)
        
        logger.info(f"Allocation {pk} cancelled by {request.user.email}")
        
        return Response({
            'message': 'Allocation cancelled successfully',
            'allocation': AllocationSerializer(allocation).data
        })


class ManualOverrideView(generics.GenericAPIView):
    """View for manual allocation override."""
    
    serializer_class = ManualAllocationSerializer
    permission_classes = [IsAdmin]
    
    def post(self, request):
        """Perform manual override."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        from apps.applications.models import Application
        from apps.hostels.models import Room, BedSpace
        
        application = get_object_or_404(
            Application,
            id=serializer.validated_data['application_id']
        )
        
        room = get_object_or_404(
            Room,
            id=serializer.validated_data['room_id']
        )
        
        bed_space = None
        if serializer.validated_data.get('bed_space_id'):
            bed_space = get_object_or_404(
                BedSpace,
                id=serializer.validated_data['bed_space_id']
            )
        
        reason = serializer.validated_data.get('reason', '')
        
        # Perform override
        engine = AllocationEngine()
        allocation = engine.manual_override(
            application=application,
            room=room,
            bed_space=bed_space,
            admin_user=request.user,
            reason=reason
        )
        
        return Response({
            'message': 'Allocation override successful',
            'allocation': AllocationSerializer(allocation).data
        })


class AllocationRunListView(generics.ListAPIView):
    """View for listing allocation runs."""
    
    queryset = AllocationRun.objects.all()
    serializer_class = AllocationRunSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['status', 'academic_session']
    ordering = ['-started_at']


class StartAllocationRunView(generics.GenericAPIView):
    """View for starting a new allocation run."""
    
    serializer_class = StartAllocationRunSerializer
    permission_classes = [IsAdmin]
    
    def post(self, request):
        """Start allocation run."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # Create run record
        run = AllocationRun.objects.create(
            academic_session=serializer.validated_data['academic_session'],
            started_by=request.user,
            parameters=serializer.validated_data.get('parameters', {})
        )
        
        # Start Celery task
        task = run_batch_allocation.delay(run.id)
        
        logger.info(
            f"Allocation run {run.id} started by {request.user.email}"
        )
        
        return Response({
            'message': 'Allocation run started',
            'run_id': run.id,
            'task_id': task.id,
            'status': 'pending'
        })


class AllocationRunStatusView(generics.RetrieveAPIView):
    """View for checking allocation run status."""
    
    queryset = AllocationRun.objects.all()
    serializer_class = AllocationRunSerializer
    permission_classes = [IsAdminOrReadOnly]


class AuditLogListView(generics.ListAPIView):
    """View for listing audit logs."""
    
    queryset = AuditLog.objects.select_related(
        'user', 'application', 'allocation'
    ).all()
    serializer_class = AuditLogSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['action', 'model_version']
    ordering = ['-timestamp']


class WaitingListView(generics.ListAPIView):
    """View for listing waiting list."""
    
    serializer_class = WaitingListSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['is_priority']
    ordering = ['position']
    
    def get_queryset(self):
        """Filter waiting list by session."""
        queryset = WaitingList.objects.select_related(
            'application', 'application__student', 'application__student__user'
        ).all()
        
        session = self.request.query_params.get('session')
        if session:
            queryset = queryset.filter(application__academic_session=session)
        
        return queryset


class MLModelStatusView(generics.GenericAPIView):
    """View for checking ML model status."""
    
    permission_classes = [IsAdminOrReadOnly]
    
    def get(self, request):
        """Get model status."""
        predictor = get_predictor()
        
        data = predictor.get_model_info()
        
        serializer = MLModelStatusSerializer(data)
        return Response(serializer.data)


class PredictPriorityScoreView(generics.GenericAPIView):
    """View for predicting priority score (debug/testing)."""
    
    serializer_class = PriorityScoreRequestSerializer
    permission_classes = [IsAdminOrReadOnly]
    
    def post(self, request):
        """Predict priority score for given features."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        predictor = get_predictor()
        
        try:
            prediction = predictor.predict(
                serializer.validated_data,
                use_domain_knowledge=True
            )
            
            response_serializer = PriorityScoreResponseSerializer(prediction)
            return Response(response_serializer.data)
            
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class AllocationStatisticsView(generics.GenericAPIView):
    """View for allocation statistics."""
    
    permission_classes = [IsAdminOrReadOnly]
    
    def get(self, request):
        """Get allocation statistics."""
        from django.db.models import Count, Avg
        
        academic_session = request.query_params.get('session')
        
        queryset = Allocation.objects.all()
        if academic_session:
            queryset = queryset.filter(application__academic_session=academic_session)
        
        total = queryset.count()
        
        # By hostel
        by_hostel = queryset.values('room__hostel__name').annotate(
            count=Count('id')
        ).order_by('-count')
        
        # By room type
        by_room_type = queryset.values('room__room_type').annotate(
            count=Count('id')
        ).order_by('room__room_type')
        
        # Confirmation status
        confirmed = queryset.filter(is_confirmed=True).count()
        pending_confirmation = queryset.filter(is_confirmed=False, is_active=True).count()
        cancelled = queryset.filter(is_active=False).count()
        
        # Average priority score of allocated students
        avg_priority = queryset.aggregate(
            avg=Avg('application__priority_score')
        )['avg'] or 0
        
        return Response({
            'total_allocations': total,
            'by_hostel': list(by_hostel),
            'by_room_type': list(by_room_type),
            'confirmation_status': {
                'confirmed': confirmed,
                'pending_confirmation': pending_confirmation,
                'cancelled': cancelled,
            },
            'average_priority_score': round(avg_priority, 2),
        })
