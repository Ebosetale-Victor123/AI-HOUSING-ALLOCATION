"""
Views for User authentication and management.
"""

from django.contrib.auth import authenticate
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils import timezone
from django.utils.crypto import get_random_string
from django.conf import settings
from datetime import timedelta
from rest_framework import status, generics, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenRefreshView

from .models import User, EmailVerificationToken, PasswordResetToken
from .serializers import (
    UserSerializer, UserCreateSerializer, UserUpdateSerializer,
    ChangePasswordSerializer, LoginSerializer, PasswordResetRequestSerializer,
    PasswordResetConfirmSerializer
)
from utils.permissions import IsOwnerOrAdmin
import logging

logger = logging.getLogger(__name__)


def get_tokens_for_user(user):
    """Generate JWT tokens for user."""
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


class RegisterView(generics.CreateAPIView):
    """View for user registration."""
    
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer
    permission_classes = [permissions.AllowAny]
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        # Generate tokens
        tokens = get_tokens_for_user(user)
        
        # Send verification email
        self.send_verification_email(user)
        
        logger.info(f"New user registered: {user.email}")
        
        return Response({
            'message': 'User registered successfully. Please check your email to verify your account.',
            'user': UserSerializer(user).data,
            'tokens': tokens
        }, status=status.HTTP_201_CREATED)
    
    def send_verification_email(self, user):
        """Send email verification token."""
        try:
            # Create verification token
            token = get_random_string(64)
            expires_at = timezone.now() + timedelta(hours=24)
            
            EmailVerificationToken.objects.create(
                user=user,
                token=token,
                expires_at=expires_at
            )
            
            # TODO: Implement actual email sending
            # For now, just log the token
            logger.info(f"Verification token for {user.email}: {token}")
            
        except Exception as e:
            logger.error(f"Failed to send verification email: {e}")


class LoginView(generics.GenericAPIView):
    """View for user login."""
    
    serializer_class = LoginSerializer
    permission_classes = [permissions.AllowAny]
    
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        email = serializer.validated_data['email']
        password = serializer.validated_data['password']
        
        user = authenticate(request, username=email, password=password)
        
        if not user:
            return Response(
                {'error': 'Invalid credentials'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        if not user.is_active:
            return Response(
                {'error': 'Account is deactivated'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        tokens = get_tokens_for_user(user)
        
        logger.info(f"User logged in: {user.email}")
        
        return Response({
            'message': 'Login successful',
            'user': UserSerializer(user).data,
            'tokens': tokens
        })


class UserProfileView(generics.RetrieveUpdateAPIView):
    """View for retrieving and updating user profile."""
    
    serializer_class = UserUpdateSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_object(self):
        return self.request.user
    
    def retrieve(self, request, *args, **kwargs):
        """Return full user data."""
        user = self.get_object()
        return Response(UserSerializer(user).data)


class ChangePasswordView(generics.GenericAPIView):
    """View for changing password."""
    
    serializer_class = ChangePasswordSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        user = request.user
        user.set_password(serializer.validated_data['new_password'])
        user.save()
        
        logger.info(f"Password changed for user: {user.email}")
        
        return Response({
            'message': 'Password changed successfully'
        })


class PasswordResetRequestView(generics.GenericAPIView):
    """View for requesting password reset."""
    
    serializer_class = PasswordResetRequestSerializer
    permission_classes = [permissions.AllowAny]
    
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        email = serializer.validated_data['email']
        
        try:
            user = User.objects.get(email=email)
            
            # Create password reset token
            token = get_random_string(64)
            expires_at = timezone.now() + timedelta(hours=1)
            
            PasswordResetToken.objects.create(
                user=user,
                token=token,
                expires_at=expires_at,
                ip_address=request.META.get('REMOTE_ADDR')
            )
            
            # TODO: Implement actual email sending
            logger.info(f"Password reset token for {user.email}: {token}")
            
        except User.DoesNotExist:
            # Don't reveal if email exists
            pass
        
        return Response({
            'message': 'If an account exists with this email, you will receive password reset instructions.'
        })


class PasswordResetConfirmView(generics.GenericAPIView):
    """View for confirming password reset."""
    
    serializer_class = PasswordResetConfirmSerializer
    permission_classes = [permissions.AllowAny]
    
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        token = serializer.validated_data['token']
        new_password = serializer.validated_data['new_password']
        
        try:
            reset_token = PasswordResetToken.objects.get(token=token)
            
            if not reset_token.is_valid:
                return Response(
                    {'error': 'Invalid or expired token'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Reset password
            user = reset_token.user
            user.set_password(new_password)
            user.save()
            
            # Mark token as used
            reset_token.is_used = True
            reset_token.save()
            
            logger.info(f"Password reset completed for user: {user.email}")
            
            return Response({
                'message': 'Password reset successful. Please login with your new password.'
            })
            
        except PasswordResetToken.DoesNotExist:
            return Response(
                {'error': 'Invalid token'},
                status=status.HTTP_400_BAD_REQUEST
            )


class EmailVerificationView(generics.GenericAPIView):
    """View for verifying email address."""
    
    permission_classes = [permissions.AllowAny]
    
    def post(self, request, *args, **kwargs):
        token = request.data.get('token')
        
        if not token:
            return Response(
                {'error': 'Token is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            verification_token = EmailVerificationToken.objects.get(token=token)
            
            if not verification_token.is_valid:
                return Response(
                    {'error': 'Invalid or expired token'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Verify user
            user = verification_token.user
            user.is_verified = True
            user.save()
            
            # Mark token as used
            verification_token.is_used = True
            verification_token.save()
            
            logger.info(f"Email verified for user: {user.email}")
            
            return Response({
                'message': 'Email verified successfully'
            })
            
        except EmailVerificationToken.DoesNotExist:
            return Response(
                {'error': 'Invalid token'},
                status=status.HTTP_400_BAD_REQUEST
            )


class UserListView(generics.ListAPIView):
    """View for listing users (admin only)."""
    
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """Filter users based on query params."""
        queryset = User.objects.all()
        
        # Filter by user type
        user_type = self.request.query_params.get('user_type')
        if user_type:
            queryset = queryset.filter(user_type=user_type)
        
        # Filter by department
        department = self.request.query_params.get('department')
        if department:
            queryset = queryset.filter(department__icontains=department)
        
        # Filter by verification status
        is_verified = self.request.query_params.get('is_verified')
        if is_verified is not None:
            queryset = queryset.filter(is_verified=is_verified.lower() == 'true')
        
        return queryset.order_by('-date_joined')
    
    def check_permissions(self, request):
        """Only admins can list all users."""
        super().check_permissions(request)
        if request.user.user_type not in ['admin', 'super_admin']:
            self.permission_denied(request, message='Admin access required')


class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    """View for retrieving, updating, or deleting a user."""
    
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrAdmin]
    
    def get_serializer_class(self):
        """Use update serializer for PUT/PATCH."""
        if self.request.method in ['PUT', 'PATCH']:
            return UserUpdateSerializer
        return UserSerializer
    
    def perform_destroy(self, instance):
        """Soft delete - deactivate user instead of deleting."""
        instance.is_active = False
        instance.save()
        logger.info(f"User deactivated: {instance.email}")
