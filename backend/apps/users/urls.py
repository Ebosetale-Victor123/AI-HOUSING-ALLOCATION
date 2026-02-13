"""
URL configuration for users app.
"""

from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from . import views

urlpatterns = [
    # Authentication
    path('register/', views.RegisterView.as_view(), name='auth-register'),
    path('login/', views.LoginView.as_view(), name='auth-login'),
    path('refresh/', TokenRefreshView.as_view(), name='auth-refresh'),
    
    # Profile
    path('profile/', views.UserProfileView.as_view(), name='auth-profile'),
    path('change-password/', views.ChangePasswordView.as_view(), name='auth-change-password'),
    
    # Password Reset
    path('password-reset/', views.PasswordResetRequestView.as_view(), name='auth-password-reset'),
    path('password-reset/confirm/', views.PasswordResetConfirmView.as_view(), name='auth-password-reset-confirm'),
    
    # Email Verification
    path('verify-email/', views.EmailVerificationView.as_view(), name='auth-verify-email'),
    
    # Admin Endpoints
    path('users/', views.UserListView.as_view(), name='user-list'),
    path('users/<int:pk>/', views.UserDetailView.as_view(), name='user-detail'),
]
