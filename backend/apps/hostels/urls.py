"""
URL configuration for hostels app.
"""

from django.urls import path

from . import views

urlpatterns = [
    # Hostels
    path('', views.HostelListCreateView.as_view(), name='hostel-list'),
    path('<int:pk>/', views.HostelDetailView.as_view(), name='hostel-detail'),
    path('statistics/', views.HostelStatisticsView.as_view(), name='hostel-statistics'),
    
    # Rooms
    path('rooms/', views.RoomListCreateView.as_view(), name='room-list'),
    path('rooms/<int:pk>/', views.RoomDetailView.as_view(), name='room-detail'),
    path('rooms/available/', views.AvailableRoomsView.as_view(), name='room-available'),
    path('rooms/bulk-create/', views.BulkRoomCreateView.as_view(), name='room-bulk-create'),
    path('<int:hostel_id>/rooms/', views.RoomByHostelView.as_view(), name='hostel-rooms'),
    
    # Bed Spaces
    path('rooms/<int:room_id>/bed-spaces/', views.BedSpaceListView.as_view(), name='bed-space-list'),
    path('bed-spaces/<int:pk>/', views.BedSpaceUpdateView.as_view(), name='bed-space-update'),
]
