"""
URL configuration for allocation app.
"""

from django.urls import path

from . import views

urlpatterns = [
    # Allocations
    path('', views.AllocationListView.as_view(), name='allocation-list'),
    path('create/', views.AllocationCreateView.as_view(), name='allocation-create'),
    path('<int:pk>/', views.AllocationDetailView.as_view(), name='allocation-detail'),
    path('<int:pk>/confirm/', views.AllocationConfirmView.as_view(), name='allocation-confirm'),
    path('<int:pk>/cancel/', views.AllocationCancelView.as_view(), name='allocation-cancel'),
    
    # Manual Override
    path('manual-override/', views.ManualOverrideView.as_view(), name='allocation-override'),
    
    # Allocation Runs
    path('runs/', views.AllocationRunListView.as_view(), name='allocation-run-list'),
    path('runs/start/', views.StartAllocationRunView.as_view(), name='allocation-run-start'),
    path('runs/<int:pk>/status/', views.AllocationRunStatusView.as_view(), name='allocation-run-status'),
    
    # Waiting List
    path('waiting-list/', views.WaitingListView.as_view(), name='allocation-waiting-list'),
    
    # Audit Logs
    path('audit-logs/', views.AuditLogListView.as_view(), name='allocation-audit-logs'),
    
    # ML Model
    path('ml/status/', views.MLModelStatusView.as_view(), name='ml-model-status'),
    path('ml/predict/', views.PredictPriorityScoreView.as_view(), name='ml-predict'),
    
    # Statistics
    path('statistics/', views.AllocationStatisticsView.as_view(), name='allocation-statistics'),
]
