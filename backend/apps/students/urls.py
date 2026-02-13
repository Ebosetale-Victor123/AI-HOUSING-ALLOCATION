"""
URL configuration for students app.
"""

from django.urls import path

from . import views

urlpatterns = [
    # Student Profile
    path('profile/', views.StudentProfileView.as_view(), name='student-profile'),
    path('profile/create/', views.StudentProfileCreateView.as_view(), name='student-profile-create'),
    path('profile/update/', views.StudentProfileUpdateView.as_view(), name='student-profile-update'),
    
    # Student List (Admin)
    path('', views.StudentListView.as_view(), name='student-list'),
    path('<int:pk>/', views.StudentDetailView.as_view(), name='student-detail'),
    
    # Dashboard
    path('dashboard/', views.StudentDashboardView.as_view(), name='student-dashboard'),
    
    # Academic History
    path('academic-history/', views.AcademicHistoryListView.as_view(), name='academic-history'),
    
    # Documents
    path('documents/', views.DocumentListCreateView.as_view(), name='document-list'),
    path('documents/<int:pk>/', views.DocumentDetailView.as_view(), name='document-detail'),
    path('documents/<int:pk>/verify/', views.DocumentVerificationView.as_view(), name='document-verify'),
    
    # Statistics (Admin)
    path('statistics/', views.StudentStatisticsView.as_view(), name='student-statistics'),
]
