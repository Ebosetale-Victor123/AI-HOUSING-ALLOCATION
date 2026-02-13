"""
Serializers for Application models.
"""

from rest_framework import serializers
from django.utils import timezone

from .models import Application, ApplicationPeriod, WaitingList
from apps.students.models import StudentProfile
from apps.students.serializers import StudentProfileListSerializer
from apps.hostels.serializers import HostelSerializer


class ApplicationSerializer(serializers.ModelSerializer):
    """Serializer for Application model."""
    
    student = StudentProfileListSerializer(read_only=True)
    preferred_hostel_details = HostelSerializer(
        source='preferred_hostel',
        read_only=True
    )
    scoring_factors = serializers.DictField(read_only=True)
    
    class Meta:
        model = Application
        fields = [
            'id', 'student', 'academic_session', 'preferred_hostel',
            'preferred_hostel_details', 'status', 'priority_score',
            'ai_confidence', 'scoring_factors', 'special_requests',
            'medical_certificate', 'application_date', 'allocation_date',
            'reviewed_at', 'reviewed_by', 'review_notes'
        ]
        read_only_fields = [
            'id', 'status', 'priority_score', 'ai_confidence',
            'application_date', 'allocation_date', 'reviewed_at',
            'reviewed_by', 'review_notes'
        ]


class ApplicationCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating Application."""
    
    class Meta:
        model = Application
        fields = [
            'academic_session', 'preferred_hostel',
            'special_requests', 'medical_certificate'
        ]
    
    def validate(self, attrs):
        """Validate application data."""
        request = self.context.get('request')
        user = request.user
        
        # Check if user is a student
        if not user.is_student:
            raise serializers.ValidationError(
                'Only students can submit housing applications.'
            )
        
        # Check if student profile exists
        try:
            student_profile = user.student_profile
        except StudentProfile.DoesNotExist:
            raise serializers.ValidationError(
                'Please complete your student profile before applying.'
            )
        
        # Check for existing application in this session
        academic_session = attrs.get('academic_session')
        existing = Application.objects.filter(
            student=student_profile,
            academic_session=academic_session
        ).exists()
        
        if existing:
            raise serializers.ValidationError(
                'You have already submitted an application for this session.'
            )
        
        # Check if application period is open
        try:
            period = ApplicationPeriod.objects.get(
                academic_session=academic_session,
                is_active=True
            )
            if not period.is_open:
                raise serializers.ValidationError(
                    'Applications are currently closed for this session.'
                )
        except ApplicationPeriod.DoesNotExist:
            raise serializers.ValidationError(
                'No active application period found for this session.'
            )
        
        # Validate preferred hostel gender matches student gender
        preferred_hostel = attrs.get('preferred_hostel')
        if preferred_hostel:
            if (
                preferred_hostel.gender_type != 'mixed' and
                preferred_hostel.gender_type != student_profile.gender.lower()
            ):
                raise serializers.ValidationError(
                    'Preferred hostel gender does not match your profile.'
                )
        
        return attrs
    
    def create(self, validated_data):
        """Create application and associate with student."""
        request = self.context.get('request')
        student_profile = request.user.student_profile
        
        validated_data['student'] = student_profile
        return super().create(validated_data)


class ApplicationUpdateSerializer(serializers.ModelSerializer):
    """Serializer for updating Application (admin only)."""
    
    class Meta:
        model = Application
        fields = ['status', 'review_notes', 'priority_score']


class ApplicationListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for listing applications."""
    
    student_name = serializers.CharField(
        source='student.user.full_name',
        read_only=True
    )
    student_matric = serializers.CharField(
        source='student.user.matric_number',
        read_only=True
    )
    
    class Meta:
        model = Application
        fields = [
            'id', 'student_name', 'student_matric',
            'academic_session', 'preferred_hostel',
            'status', 'priority_score', 'application_date'
        ]


class ApplicationReviewSerializer(serializers.Serializer):
    """Serializer for reviewing applications."""
    
    action = serializers.ChoiceField(
        choices=['approve', 'reject']
    )
    notes = serializers.CharField(required=False, allow_blank=True)


class ApplicationPeriodSerializer(serializers.ModelSerializer):
    """Serializer for ApplicationPeriod model."""
    
    is_open = serializers.BooleanField(read_only=True)
    status = serializers.CharField(read_only=True)
    
    class Meta:
        model = ApplicationPeriod
        fields = [
            'id', 'academic_session', 'name', 'description',
            'start_date', 'end_date', 'is_active',
            'allow_new_applications', 'is_open', 'status',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']
    
    def validate(self, attrs):
        """Validate period dates."""
        start_date = attrs.get('start_date')
        end_date = attrs.get('end_date')
        
        if start_date and end_date and start_date >= end_date:
            raise serializers.ValidationError(
                'End date must be after start date.'
            )
        
        return attrs


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
        read_only_fields = ['id', 'added_at']


class ApplicationStatisticsSerializer(serializers.Serializer):
    """Serializer for application statistics."""
    
    total_applications = serializers.IntegerField()
    by_status = serializers.ListField()
    by_level = serializers.ListField()
    by_gender = serializers.ListField()
    with_disability = serializers.IntegerField()
    with_financial_aid = serializers.IntegerField()
    average_priority_score = serializers.FloatField()
    top_scorers = serializers.ListField()
