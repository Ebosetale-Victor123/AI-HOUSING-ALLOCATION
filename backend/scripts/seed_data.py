#!/usr/bin/env python
"""
Seed data script for SmartAlloc.
Generates sample data for development and testing.
"""

import os
import sys
import random
from datetime import datetime, timedelta

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import django
django.setup()

from django.contrib.auth import get_user_model
from apps.students.models import StudentProfile
from apps.hostels.models import Hostel, Room, BedSpace
from apps.applications.models import ApplicationPeriod
from utils.constants import UserType, Gender, Level, HostelGenderType, RoomType

User = get_user_model()


def create_superuser():
    """Create superuser if doesn't exist."""
    if not User.objects.filter(email='admin@smartalloc.edu').exists():
        User.objects.create_superuser(
            email='admin@smartalloc.edu',
            password='admin123',
            first_name='Admin',
            last_name='User',
            user_type=UserType.SUPER_ADMIN
        )
        print("Created superuser: admin@smartalloc.edu / admin123")


def create_hostels():
    """Create sample hostels."""
    hostels_data = [
        {
            'name': 'Hall A - Male',
            'code': 'HA',
            'gender_type': HostelGenderType.MALE,
            'description': 'Standard male hostel',
            'warden_name': 'Mr. John Doe',
        },
        {
            'name': 'Hall B - Female',
            'code': 'HB',
            'gender_type': HostelGenderType.FEMALE,
            'description': 'Standard female hostel',
            'warden_name': 'Mrs. Jane Smith',
        },
        {
            'name': 'Hall C - Mixed',
            'code': 'HC',
            'gender_type': HostelGenderType.MIXED,
            'description': 'Mixed gender postgraduate hostel',
            'warden_name': 'Dr. Michael Brown',
        },
        {
            'name': 'Hall D - Premium Male',
            'code': 'HD',
            'gender_type': HostelGenderType.MALE,
            'description': 'Premium male hostel with AC',
            'warden_name': 'Mr. Robert Wilson',
            'has_air_conditioning': True,
        },
        {
            'name': 'Hall E - Premium Female',
            'code': 'HE',
            'gender_type': HostelGenderType.FEMALE,
            'description': 'Premium female hostel with AC',
            'warden_name': 'Mrs. Sarah Johnson',
            'has_air_conditioning': True,
        },
    ]
    
    for hostel_data in hostels_data:
        hostel, created = Hostel.objects.get_or_create(
            code=hostel_data['code'],
            defaults=hostel_data
        )
        if created:
            print(f"Created hostel: {hostel.name}")
            create_rooms_for_hostel(hostel)


def create_rooms_for_hostel(hostel):
    """Create rooms for a hostel."""
    floors = 3
    rooms_per_floor = 10
    
    for floor in range(1, floors + 1):
        for room_num in range(1, rooms_per_floor + 1):
            room_number = f"{floor}{room_num:02d}"
            
            # Make some rooms accessible on ground floor
            is_accessible = (floor == 1 and room_num <= 2)
            
            # Make some rooms premium
            room_type = RoomType.PREMIUM if hostel.code in ['HD', 'HE'] else RoomType.STANDARD
            
            room = Room.objects.create(
                hostel=hostel,
                room_number=room_number,
                capacity=4,
                floor_level=floor,
                room_type=room_type,
                is_accessible=is_accessible,
                has_air_conditioning=hostel.code in ['HD', 'HE'],
            )
            
            # Create bed spaces
            for i in range(1, room.capacity + 1):
                BedSpace.objects.create(room=room, space_number=i)
    
    hostel.update_total_rooms()
    print(f"  Created {floors * rooms_per_floor} rooms for {hostel.name}")


def create_students(n=50):
    """Create sample students."""
    departments = ['Computer Science', 'Engineering', 'Medicine', 'Law', 'Business']
    first_names = ['Alice', 'Bob', 'Charlie', 'Diana', 'Edward', 'Fiona', 'George', 'Hannah',
                   'Ian', 'Julia', 'Kevin', 'Laura', 'Michael', 'Nina', 'Oscar', 'Paula']
    last_names = ['Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Garcia', 'Miller', 'Davis']
    
    created_count = 0
    
    for i in range(n):
        email = f"student{i+1}@university.edu"
        
        if User.objects.filter(email=email).exists():
            continue
        
        first_name = random.choice(first_names)
        last_name = random.choice(last_names)
        
        user = User.objects.create_user(
            email=email,
            password='student123',
            first_name=first_name,
            last_name=last_name,
            user_type=UserType.STUDENT,
            matric_number=f"CSC/2024/{i+1:04d}",
            department=random.choice(departments),
            is_verified=True
        )
        
        # Create student profile
        level = random.choice([100, 200, 300, 400, 500])
        gender = random.choice([Gender.MALE, Gender.FEMALE])
        
        profile = StudentProfile.objects.create(
            user=user,
            current_gpa=round(random.uniform(2.0, 5.0), 2),
            level=level,
            gender=gender,
            distance_from_campus=round(random.uniform(5, 500), 1),
            disability_status=random.random() < 0.05,  # 5% have disabilities
            financial_aid_status=random.random() < 0.30,  # 30% have financial aid
        )
        
        created_count += 1
    
    print(f"Created {created_count} students")


def create_application_period():
    """Create application period."""
    from django.utils import timezone
    
    now = timezone.now()
    
    period, created = ApplicationPeriod.objects.get_or_create(
        academic_session='2024/2025',
        defaults={
            'name': '2024/2025 Academic Session',
            'description': 'Housing application for 2024/2025 session',
            'start_date': now - timedelta(days=30),
            'end_date': now + timedelta(days=30),
            'is_active': True,
            'allow_new_applications': True,
        }
    )
    
    if created:
        print(f"Created application period: {period.name}")


def main():
    """Main function."""
    print("=" * 50)
    print("SmartAlloc Seed Data Generator")
    print("=" * 50)
    print()
    
    print("Creating superuser...")
    create_superuser()
    print()
    
    print("Creating hostels and rooms...")
    create_hostels()
    print()
    
    print("Creating students...")
    create_students(n=50)
    print()
    
    print("Creating application period...")
    create_application_period()
    print()
    
    print("=" * 50)
    print("Seed data generation complete!")
    print("=" * 50)
    print()
    print("You can now:")
    print("1. Log in as admin: admin@smartalloc.edu / admin123")
    print("2. Log in as student: student1@university.edu / student123")
    print("3. Train the ML model: python scripts/train_model.sh")


if __name__ == '__main__':
    main()
