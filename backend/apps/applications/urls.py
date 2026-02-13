"""
URL configuration for applications app.
"""

from django.urls import path

from . import views

urlpatterns = [
    # Application Submission
    path('submit/', views.ApplicationSubmitView.as_view(), name='application-submit'),
    path('status/', views.ApplicationStatusView.as_view(), name='application-status'),
    
    # Application List and Detail
    path('', views.ApplicationListView.as_view(), name='application-list'),
    path('<int:pk>/', views.ApplicationDetailView.as_view(), name='application-detail'),
    path('<int:pk>/review/', views.ApplicationReviewView.as_view(), name='application-review'),
    
    # Bulk Actions
    path('bulk-action/', views.BulkApplicationActionView.as_view(), name='application-bulk-action'),
    
    # Application Periods
    path('periods/', views.ApplicationPeriodListCreateView.as_view(), name='application-period-list'),
    path('periods/current/', views.CurrentApplicationPeriodView.as_view(), name='application-period-current'),
    path('periods/<int:pk>/', views.ApplicationPeriodDetailView.as_view(), name='application-period-detail'),
    
    # Waiting List
    path('waiting-list/', views.WaitingListView.as_view(), name='waiting-list'),
    
    # Statistics
    path('statistics/', views.ApplicationStatisticsView.as_view(), name='application-statistics'),
]
