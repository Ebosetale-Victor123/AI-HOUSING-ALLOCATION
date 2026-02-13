"""
Serializers for User model.
"""

from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from django.core.validators import validate_email

from .models import User
from utils.constants import UserType


class UserSerializer(serializers.ModelSerializer):
    """Serializer for User model."""
    
    full_name = serializers.CharField(source='get_full_name', read_only=True)
    
    class Meta:
        model = User
        fields = [
            'id', 'email', 'first_name', 'last_name', 'full_name',
            'user_type', 'matric_number', 'department', 'phone_number',
            'is_verified', 'is_active', 'date_joined', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'is_verified', 'date_joined', 'created_at', 'updated_at']


class UserCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating new users."""
    
    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password]
    )
    password_confirm = serializers.CharField(write_only=True, required=True)
    
    class Meta:
        model = User
        fields = [
            'id', 'email', 'password', 'password_confirm',
            'first_name', 'last_name', 'user_type',
            'matric_number', 'department', 'phone_number'
        ]
        read_only_fields = ['id']
    
    def validate(self, attrs):
        """Validate password confirmation."""
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError(
                {"password_confirm": "Password fields didn't match."}
            )
        
        # Validate email
        try:
            validate_email(attrs['email'])
        except:
            raise serializers.ValidationError(
                {"email": "Please provide a valid email address."}
            )
        
        # Validate student fields
        if attrs.get('user_type') == UserType.STUDENT:
            if not attrs.get('matric_number'):
                raise serializers.ValidationError(
                    {"matric_number": "Matric number is required for students."}
                )
        
        return attrs
    
    def create(self, validated_data):
        """Create user with hashed password."""
        validated_data.pop('password_confirm')
        password = validated_data.pop('password')
        
        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        
        return user


class UserUpdateSerializer(serializers.ModelSerializer):
    """Serializer for updating user profile."""
    
    class Meta:
        model = User
        fields = [
            'first_name', 'last_name', 'department',
            'phone_number', 'matric_number'
        ]
    
    def validate_matric_number(self, value):
        """Validate matric number is not already taken."""
        if value:
            existing = User.objects.filter(matric_number=value).exclude(
                id=self.instance.id
            ).exists()
            if existing:
                raise serializers.ValidationError(
                    "This matric number is already registered."
                )
        return value


class ChangePasswordSerializer(serializers.Serializer):
    """Serializer for password change."""
    
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(
        required=True,
        validators=[validate_password]
    )
    new_password_confirm = serializers.CharField(required=True)
    
    def validate(self, attrs):
        """Validate new passwords match."""
        if attrs['new_password'] != attrs['new_password_confirm']:
            raise serializers.ValidationError(
                {"new_password_confirm": "New password fields didn't match."}
            )
        return attrs
    
    def validate_old_password(self, value):
        """Validate old password is correct."""
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("Old password is incorrect.")
        return value


class LoginSerializer(serializers.Serializer):
    """Serializer for user login."""
    
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True, write_only=True)


class TokenResponseSerializer(serializers.Serializer):
    """Serializer for token response."""
    
    access = serializers.CharField()
    refresh = serializers.CharField()
    user = UserSerializer()


class PasswordResetRequestSerializer(serializers.Serializer):
    """Serializer for password reset request."""
    
    email = serializers.EmailField(required=True)


class PasswordResetConfirmSerializer(serializers.Serializer):
    """Serializer for password reset confirmation."""
    
    token = serializers.CharField(required=True)
    new_password = serializers.CharField(
        required=True,
        validators=[validate_password]
    )
    new_password_confirm = serializers.CharField(required=True)
    
    def validate(self, attrs):
        """Validate passwords match."""
        if attrs['new_password'] != attrs['new_password_confirm']:
            raise serializers.ValidationError(
                {"new_password_confirm": "Password fields didn't match."}
            )
        return attrs
