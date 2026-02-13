"""
Serializers for Student models.
"""

from rest_framework import serializers

from .models import StudentProfile, AcademicHistory, Document
from apps.users.serializers import UserSerializer


class StudentProfileSerializer(serializers.ModelSerializer):
    """Serializer for StudentProfile model."""
    
    user = UserSerializer(read_only=True)
    seniority_score = serializers.FloatField(read_only=True)
    needs_accessible_room = serializers.BooleanField(read_only=True)
    
    class Meta:
        model = StudentProfile
        fields = [
            'id', 'user', 'current_gpa', 'level', 'gender',
            'date_of_birth', 'home_address', 'distance_from_campus',
            'disability_status', 'disability_details', 'financial_aid_status',
            'emergency_contact_name', 'emergency_contact_phone',
            'medical_conditions', 'seniority_score', 'needs_accessible_room',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class StudentProfileCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating StudentProfile."""
    
    class Meta:
        model = StudentProfile
        fields = [
            'current_gpa', 'level', 'gender', 'date_of_birth',
            'home_address', 'distance_from_campus', 'disability_status',
            'disability_details', 'financial_aid_status',
            'emergency_contact_name', 'emergency_contact_phone',
            'medical_conditions'
        ]
    
    def validate(self, attrs):
        """Validate profile data."""
        # Ensure disability details are provided if disability_status is True
        if attrs.get('disability_status') and not attrs.get('disability_details'):
            raise serializers.ValidationError({
                'disability_details': 'Please provide details about your accessibility needs.'
            })
        
        return attrs
    
    def create(self, validated_data):
        """Create profile and associate with current user."""
        user = self.context['request'].user
        
        # Check if profile already exists
        if hasattr(user, 'student_profile'):
            raise serializers.ValidationError(
                'Student profile already exists for this user.'
            )
        
        validated_data['user'] = user
        return super().create(validated_data)


class StudentProfileUpdateSerializer(serializers.ModelSerializer):
    """Serializer for updating StudentProfile."""
    
    class Meta:
        model = StudentProfile
        fields = [
            'current_gpa', 'level', 'home_address', 'distance_from_campus',
            'disability_status', 'disability_details', 'financial_aid_status',
            'emergency_contact_name', 'emergency_contact_phone',
            'medical_conditions'
        ]
    
    def validate(self, attrs):
        """Validate profile data."""
        # Ensure disability details are provided if disability_status is True
        if attrs.get('disability_status') and not attrs.get('disability_details'):
            # Check if existing profile has details
            instance = self.instance
            if not instance or not instance.disability_details:
                raise serializers.ValidationError({
                    'disability_details': 'Please provide details about your accessibility needs.'
                })
        
        return attrs


class StudentProfileListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for listing students."""
    
    user_id = serializers.IntegerField(source='user.id', read_only=True)
    full_name = serializers.CharField(source='user.full_name', read_only=True)
    email = serializers.EmailField(source='user.email', read_only=True)
    matric_number = serializers.CharField(source='user.matric_number', read_only=True)
    department = serializers.CharField(source='user.department', read_only=True)
    
    class Meta:
        model = StudentProfile
        fields = [
            'id', 'user_id', 'full_name', 'email', 'matric_number',
            'department', 'current_gpa', 'level', 'gender',
            'disability_status', 'financial_aid_status'
        ]


class AcademicHistorySerializer(serializers.ModelSerializer):
    """Serializer for AcademicHistory model."""
    
    class Meta:
        model = AcademicHistory
        fields = ['id', 'academic_session', 'gpa', 'level', 'created_at']
        read_only_fields = ['id', 'created_at']


class DocumentSerializer(serializers.ModelSerializer):
    """Serializer for Document model."""
    
    file_url = serializers.SerializerMethodField()
    
    class Meta:
        model = Document
        fields = [
            'id', 'document_type', 'title', 'file', 'file_url',
            'description', 'is_verified', 'verified_by', 'verified_at', 'uploaded_at'
        ]
        read_only_fields = ['id', 'is_verified', 'verified_by', 'verified_at', 'uploaded_at']
    
    def get_file_url(self, obj):
        """Get the URL for the file."""
        if obj.file:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.file.url)
            return obj.file.url
        return None
    
    def validate_file(self, value):
        """Validate file size and type."""
        from utils.validators import validate_file_size
        validate_file_size(value)
        return value


class DocumentVerificationSerializer(serializers.ModelSerializer):
    """Serializer for verifying documents (admin only)."""
    
    class Meta:
        model = Document
        fields = ['is_verified']


class StudentDashboardSerializer(serializers.ModelSerializer):
    """Serializer for student dashboard data."""
    
    user = UserSerializer(read_only=True)
    documents_count = serializers.IntegerField(source='documents.count', read_only=True)
    pending_documents = serializers.IntegerField(
        source='documents.filter.is_verified'.count,
        read_only=True
    )
    
    class Meta:
        model = StudentProfile
        fields = [
            'id', 'user', 'current_gpa', 'level', 'gender',
            'disability_status', 'financial_aid_status',
            'documents_count', 'pending_documents',
            'created_at', 'updated_at'
        ]
