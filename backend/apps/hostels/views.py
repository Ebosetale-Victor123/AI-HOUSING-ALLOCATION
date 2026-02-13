"""
Views for Hostel app.
"""

from rest_framework import generics, status, filters
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Sum, Count, Q
from django.shortcuts import get_object_or_404

from .models import Hostel, Room, BedSpace
from .serializers import (
    HostelSerializer, HostelDetailSerializer,
    RoomSerializer, RoomListSerializer, RoomCreateSerializer,
    BedSpaceSerializer, HostelStatisticsSerializer
)
from utils.permissions import IsAdminOrReadOnly, IsAdmin, ReadOnly


class HostelListCreateView(generics.ListCreateAPIView):
    """View for listing and creating hostels."""
    
    queryset = Hostel.objects.all()
    serializer_class = HostelSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['gender_type', 'is_active']
    search_fields = ['name', 'code', 'description']
    ordering_fields = ['name', 'created_at']
    ordering = ['name']


class HostelDetailView(generics.RetrieveUpdateDestroyAPIView):
    """View for retrieving, updating, or deleting a hostel."""
    
    queryset = Hostel.objects.prefetch_related('rooms')
    serializer_class = HostelDetailSerializer
    permission_classes = [IsAdminOrReadOnly]
    
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return HostelDetailSerializer
        return HostelSerializer
    
    def perform_destroy(self, instance):
        """Soft delete - deactivate hostel instead of deleting."""
        instance.is_active = False
        instance.save()


class RoomListCreateView(generics.ListCreateAPIView):
    """View for listing and creating rooms."""
    
    queryset = Room.objects.select_related('hostel').prefetch_related('bed_spaces')
    serializer_class = RoomSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = [
        'hostel', 'hostel__gender_type', 'room_type',
        'is_accessible', 'is_active', 'is_under_maintenance',
        'floor_level'
    ]
    search_fields = ['room_number', 'hostel__name']
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return RoomCreateSerializer
        return RoomSerializer
    
    def get_queryset(self):
        """Filter rooms based on availability."""
        queryset = super().get_queryset()
        
        # Filter by availability
        available = self.request.query_params.get('available')
        if available is not None:
            if available.lower() == 'true':
                queryset = queryset.filter(
                    is_active=True,
                    is_under_maintenance=False,
                    current_occupancy__lt=models.F('capacity')
                )
        
        # Filter by available spaces
        min_spaces = self.request.query_params.get('min_spaces')
        if min_spaces:
            queryset = queryset.filter(
                capacity__gt=models.F('current_occupancy')
            ).annotate(
                available=models.F('capacity') - models.F('current_occupancy')
            ).filter(available__gte=int(min_spaces))
        
        return queryset


class RoomDetailView(generics.RetrieveUpdateDestroyAPIView):
    """View for retrieving, updating, or deleting a room."""
    
    queryset = Room.objects.select_related('hostel').prefetch_related('bed_spaces')
    serializer_class = RoomSerializer
    permission_classes = [IsAdminOrReadOnly]
    
    def perform_destroy(self, instance):
        """Soft delete - deactivate room instead of deleting."""
        instance.is_active = False
        instance.save()
        instance.hostel.update_total_rooms()


class RoomByHostelView(generics.ListAPIView):
    """View for listing rooms in a specific hostel."""
    
    serializer_class = RoomListSerializer
    permission_classes = [IsAdminOrReadOnly]
    
    def get_queryset(self):
        hostel_id = self.kwargs.get('hostel_id')
        return Room.objects.filter(hostel_id=hostel_id).select_related('hostel')


class BedSpaceListView(generics.ListAPIView):
    """View for listing bed spaces in a room."""
    
    serializer_class = BedSpaceSerializer
    permission_classes = [IsAdminOrReadOnly]
    
    def get_queryset(self):
        room_id = self.kwargs.get('room_id')
        return BedSpace.objects.filter(room_id=room_id)


class BedSpaceUpdateView(generics.UpdateAPIView):
    """View for updating bed space status."""
    
    queryset = BedSpace.objects.all()
    serializer_class = BedSpaceSerializer
    permission_classes = [IsAdmin]


class HostelStatisticsView(generics.GenericAPIView):
    """View for hostel statistics."""
    
    permission_classes = [IsAdminOrReadOnly]
    
    def get(self, request):
        """Get hostel statistics."""
        hostels = Hostel.objects.all()
        
        # Basic counts
        total_hostels = hostels.count()
        total_rooms = Room.objects.count()
        
        # Capacity calculations
        capacity_data = Room.objects.aggregate(
            total_capacity=Sum('capacity'),
            total_occupancy=Sum('current_occupancy')
        )
        
        total_capacity = capacity_data['total_capacity'] or 0
        total_occupancy = capacity_data['total_occupancy'] or 0
        
        overall_occupancy_rate = 0
        if total_capacity > 0:
            overall_occupancy_rate = (total_occupancy / total_capacity) * 100
        
        # By gender type
        by_gender = []
        for gender_type, label in Hostel._meta.get_field('gender_type').choices:
            count = hostels.filter(gender_type=gender_type).count()
            by_gender.append({'gender_type': gender_type, 'label': label, 'count': count})
        
        # By room type
        by_room_type = Room.objects.values('room_type').annotate(
            count=Count('id')
        ).order_by('room_type')
        
        data = {
            'total_hostels': total_hostels,
            'total_rooms': total_rooms,
            'total_capacity': total_capacity,
            'total_occupancy': total_occupancy,
            'overall_occupancy_rate': round(overall_occupancy_rate, 2),
            'by_gender_type': by_gender,
            'by_room_type': list(by_room_type),
        }
        
        serializer = HostelStatisticsSerializer(data)
        return Response(serializer.data)


class AvailableRoomsView(generics.ListAPIView):
    """View for listing available rooms for allocation."""
    
    serializer_class = RoomListSerializer
    permission_classes = [IsAdminOrReadOnly]
    
    def get_queryset(self):
        """Get rooms with available spaces."""
        queryset = Room.objects.filter(
            is_active=True,
            is_under_maintenance=False
        ).select_related('hostel')
        
        # Filter by gender type
        gender = self.request.query_params.get('gender')
        if gender:
            queryset = queryset.filter(hostel__gender_type=gender)
        
        # Filter by accessibility
        accessible = self.request.query_params.get('accessible')
        if accessible is not None:
            queryset = queryset.filter(is_accessible=accessible.lower() == 'true')
        
        # Filter rooms with available space
        queryset = queryset.filter(capacity__gt=models.F('current_occupancy'))
        
        return queryset.order_by('hostel__name', 'room_number')


class BulkRoomCreateView(generics.GenericAPIView):
    """View for bulk creating rooms."""
    
    permission_classes = [IsAdmin]
    
    def post(self, request):
        """Create multiple rooms."""
        rooms_data = request.data.get('rooms', [])
        
        if not rooms_data:
            return Response(
                {'error': 'No room data provided'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        created_rooms = []
        errors = []
        
        for idx, room_data in enumerate(rooms_data):
            serializer = RoomCreateSerializer(data=room_data)
            if serializer.is_valid():
                room = serializer.save()
                created_rooms.append(RoomSerializer(room).data)
            else:
                errors.append({'index': idx, 'errors': serializer.errors})
        
        return Response({
            'created_count': len(created_rooms),
            'rooms': created_rooms,
            'errors': errors
        })
