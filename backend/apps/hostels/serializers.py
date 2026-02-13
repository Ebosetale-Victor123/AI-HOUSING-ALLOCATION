"""
Serializers for Hostel models.
"""

from rest_framework import serializers

from .models import Hostel, Room, BedSpace


class BedSpaceSerializer(serializers.ModelSerializer):
    """Serializer for BedSpace model."""
    
    class Meta:
        model = BedSpace
        fields = ['id', 'space_number', 'is_occupied', 'is_active', 'notes']
        read_only_fields = ['id']


class RoomSerializer(serializers.ModelSerializer):
    """Serializer for Room model."""
    
    hostel_name = serializers.CharField(source='hostel.name', read_only=True)
    hostel_code = serializers.CharField(source='hostel.code', read_only=True)
    available_spaces = serializers.IntegerField(read_only=True)
    is_full = serializers.BooleanField(read_only=True)
    is_available = serializers.BooleanField(read_only=True)
    bed_spaces = BedSpaceSerializer(many=True, read_only=True)
    
    class Meta:
        model = Room
        fields = [
            'id', 'hostel', 'hostel_name', 'hostel_code',
            'room_number', 'capacity', 'current_occupancy',
            'available_spaces', 'is_full', 'is_available',
            'floor_level', 'room_type', 'is_accessible',
            'has_balcony', 'has_air_conditioning',
            'has_private_bathroom', 'has_furniture',
            'is_active', 'is_under_maintenance', 'maintenance_notes',
            'bed_spaces', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'current_occupancy', 'created_at', 'updated_at']


class RoomListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for listing rooms."""
    
    hostel_name = serializers.CharField(source='hostel.name', read_only=True)
    hostel_code = serializers.CharField(source='hostel.code', read_only=True)
    available_spaces = serializers.IntegerField(read_only=True)
    
    class Meta:
        model = Room
        fields = [
            'id', 'hostel', 'hostel_name', 'hostel_code',
            'room_number', 'capacity', 'current_occupancy',
            'available_spaces', 'room_type', 'is_accessible',
            'is_active', 'is_under_maintenance'
        ]


class RoomCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating rooms with bed spaces."""
    
    create_bed_spaces = serializers.BooleanField(
        write_only=True,
        default=True,
        help_text='Automatically create bed spaces based on capacity'
    )
    
    class Meta:
        model = Room
        fields = [
            'hostel', 'room_number', 'capacity', 'floor_level',
            'room_type', 'is_accessible', 'has_balcony',
            'has_air_conditioning', 'has_private_bathroom',
            'has_furniture', 'create_bed_spaces'
        ]
    
    def create(self, validated_data):
        create_bed_spaces = validated_data.pop('create_bed_spaces', True)
        room = super().create(validated_data)
        
        # Create bed spaces
        if create_bed_spaces:
            for i in range(1, room.capacity + 1):
                BedSpace.objects.create(room=room, space_number=i)
        
        # Update hostel room count
        room.hostel.update_total_rooms()
        
        return room


class HostelSerializer(serializers.ModelSerializer):
    """Serializer for Hostel model."""
    
    total_capacity = serializers.IntegerField(read_only=True)
    current_occupancy = serializers.IntegerField(read_only=True)
    available_spaces = serializers.IntegerField(read_only=True)
    occupancy_rate = serializers.FloatField(read_only=True)
    room_count = serializers.IntegerField(source='rooms.count', read_only=True)
    
    class Meta:
        model = Hostel
        fields = [
            'id', 'name', 'code', 'gender_type', 'description',
            'address', 'total_rooms', 'room_count', 'total_capacity',
            'current_occupancy', 'available_spaces', 'occupancy_rate',
            'warden_name', 'warden_contact',
            'location_lat', 'location_lng',
            'has_electricity', 'has_water', 'has_internet',
            'has_common_room', 'has_kitchen',
            'is_active', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'total_rooms', 'created_at', 'updated_at']


class HostelDetailSerializer(HostelSerializer):
    """Detailed serializer for Hostel with rooms."""
    
    rooms = RoomListSerializer(many=True, read_only=True)
    
    class Meta(HostelSerializer.Meta):
        fields = HostelSerializer.Meta.fields + ['rooms']


class HostelStatisticsSerializer(serializers.Serializer):
    """Serializer for hostel statistics."""
    
    total_hostels = serializers.IntegerField()
    total_rooms = serializers.IntegerField()
    total_capacity = serializers.IntegerField()
    total_occupancy = serializers.IntegerField()
    overall_occupancy_rate = serializers.FloatField()
    by_gender_type = serializers.ListField()
    by_room_type = serializers.ListField()


class RoomAllocationSerializer(serializers.Serializer):
    """Serializer for room allocation data."""
    
    room_id = serializers.IntegerField()
    student_id = serializers.IntegerField()
    bed_space_number = serializers.IntegerField(required=False, allow_null=True)
