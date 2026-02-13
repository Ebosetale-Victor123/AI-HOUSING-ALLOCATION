"""
Serializers for Allocation models.
"""

from rest_framework import serializers

from .models import Allocation, AuditLog, AllocationRun
from apps.applications.models import WaitingList
from apps.applications.serializers import ApplicationSerializer
from apps.hostels.serializers import RoomSerializer, HostelSerializer


class AllocationSerializer(serializers.ModelSerializer):
    """Serializer for Allocation model."""
    
    student_name = serializers.CharField(
        source='application.student.user.full_name',
        read_only=True
    )
    student_matric = serializers.CharField(
        source='application.student.user.matric_number',
        read_only=True
    )
    room_details = RoomSerializer(source='room', read_only=True)
    application_details = ApplicationSerializer(source='application', read_only=True)
    
    class Meta:
        model = Allocation
        fields = [
            'id', 'application', 'application_details', 'student_name', 'student_matric',
            'room', 'room_details', 'bed_space', 'bed_space_number',
            'allocated_by', 'allocated_by_user', 'allocation_reason',
            'admin_override', 'is_confirmed', 'confirmed_at',
            'is_active', 'cancelled_at', 'cancellation_reason',
            'created_at', 'updated_at'
        ]
        read_only_fields = [
            'id', 'allocated_by', 'allocated_by_user',
            'is_confirmed', 'confirmed_at', 'created_at', 'updated_at'
        ]


class AllocationListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for listing allocations."""
    
    student_name = serializers.CharField(
        source='application.student.user.full_name',
        read_only=True
    )
    student_matric = serializers.CharField(
        source='application.student.user.matric_number',
        read_only=True
    )
    hostel_name = serializers.CharField(
        source='room.hostel.name',
        read_only=True
    )
    room_number = serializers.CharField(
        source='room.room_number',
        read_only=True
    )
    priority_score = serializers.FloatField(
        source='application.priority_score',
        read_only=True
    )
    
    class Meta:
        model = Allocation
        fields = [
            'id', 'student_name', 'student_matric',
            'hostel_name', 'room_number', 'bed_space_number',
            'priority_score', 'allocated_by', 'is_confirmed',
            'is_active', 'created_at'
        ]


class AllocationCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating allocations."""
    
    class Meta:
        model = Allocation
        fields = ['application', 'room', 'bed_space', 'allocation_reason']
    
    def validate(self, attrs):
        """Validate allocation data."""
        room = attrs.get('room')
        bed_space = attrs.get('bed_space')
        application = attrs.get('application')
        
        # Check if room is available
        if not room.is_available:
            raise serializers.ValidationError(
                {'room': 'Room is not available for allocation.'}
            )
        
        # Check gender compatibility
        student_gender = application.student.gender
        hostel_gender = room.hostel.gender_type
        
        if hostel_gender != 'mixed':
            if (hostel_gender == 'male' and student_gender != 'M') or \
               (hostel_gender == 'female' and student_gender != 'F'):
                raise serializers.ValidationError(
                    {'room': 'Room gender type does not match student gender.'}
                )
        
        # Check accessibility if needed
        if application.student.disability_status and not room.is_accessible:
            raise serializers.ValidationError(
                {'room': 'Student requires an accessible room.'}
            )
        
        # Validate bed space
        if bed_space:
            if bed_space.room != room:
                raise serializers.ValidationError(
                    {'bed_space': 'Bed space does not belong to the selected room.'}
                )
            if bed_space.is_occupied:
                raise serializers.ValidationError(
                    {'bed_space': 'Bed space is already occupied.'}
                )
        
        # Check if application already has an allocation
        if hasattr(application, 'allocation'):
            raise serializers.ValidationError(
                {'application': 'Application already has an allocation.'}
            )
        
        return attrs


class ManualAllocationSerializer(serializers.Serializer):
    """Serializer for manual allocation by admin."""
    
    application_id = serializers.IntegerField()
    room_id = serializers.IntegerField()
    bed_space_id = serializers.IntegerField(required=False, allow_null=True)
    reason = serializers.CharField(required=False, allow_blank=True)


class AuditLogSerializer(serializers.ModelSerializer):
    """Serializer for AuditLog model."""
    
    user_email = serializers.CharField(source='user.email', read_only=True)
    student_name = serializers.CharField(
        source='application.student.user.full_name',
        read_only=True
    )
    
    class Meta:
        model = AuditLog
        fields = [
            'id', 'action', 'user', 'user_email', 'student_name',
            'application', 'allocation', 'timestamp', 'ip_address',
            'details', 'model_version', 'raw_score', 'final_score'
        ]
        read_only_fields = ['id', 'timestamp']


class AllocationRunSerializer(serializers.ModelSerializer):
    """Serializer for AllocationRun model."""
    
    started_by_name = serializers.CharField(
        source='started_by.full_name',
        read_only=True
    )
    
    class Meta:
        model = AllocationRun
        fields = [
            'id', 'academic_session', 'status', 'started_by', 'started_by_name',
            'started_at', 'completed_at', 'total_applications',
            'successful_allocations', 'failed_allocations',
            'waiting_list_count', 'error_message', 'parameters',
            'celery_task_id'
        ]
        read_only_fields = [
            'id', 'started_at', 'completed_at', 'error_message',
            'celery_task_id'
        ]


class StartAllocationRunSerializer(serializers.Serializer):
    """Serializer for starting an allocation run."""
    
    academic_session = serializers.CharField(max_length=9)
    parameters = serializers.JSONField(required=False, default=dict)


class AllocationOverrideSerializer(serializers.Serializer):
    """Serializer for overriding an allocation."""
    
    allocation_id = serializers.IntegerField()
    new_room_id = serializers.IntegerField()
    new_bed_space_id = serializers.IntegerField(required=False, allow_null=True)
    reason = serializers.CharField()


class WaitingListSerializer(serializers.ModelSerializer):
    """Serializer for WaitingList model."""
    
    student_name = serializers.CharField(
        source='application.student.user.full_name',
        read_only=True
    )
    student_matric = serializers.CharField(
        source='application.student.user.matric_number',
        read_only=True
    )
    priority_score = serializers.FloatField(
        source='application.priority_score',
        read_only=True
    )
    
    class Meta:
        model = WaitingList
        fields = [
            'id', 'application', 'student_name', 'student_matric',
            'position', 'priority_score', 'added_at', 'is_priority', 'notes'
        ]


class MLModelStatusSerializer(serializers.Serializer):
    """Serializer for ML model status."""
    
    is_loaded = serializers.BooleanField()
    model_version = serializers.CharField()
    model_path = serializers.CharField()
    model_type = serializers.CharField(required=False)
    n_features = serializers.IntegerField(required=False)
    n_estimators = serializers.IntegerField(required=False)


class PriorityScoreRequestSerializer(serializers.Serializer):
    """Serializer for requesting priority score prediction."""
    
    gpa = serializers.FloatField(min_value=0, max_value=5, required=False)
    level = serializers.IntegerField()
    distance = serializers.FloatField(min_value=0, required=False)
    disability = serializers.BooleanField(default=False)
    financial_aid = serializers.BooleanField(default=False)


class PriorityScoreResponseSerializer(serializers.Serializer):
    """Serializer for priority score response."""
    
    priority_score = serializers.FloatField()
    confidence = serializers.FloatField()
    feature_importance = serializers.DictField()
    model_version = serializers.CharField()
    scoring_method = serializers.CharField()
