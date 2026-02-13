"""
Core allocation engine for SmartAlloc.
"""

from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass
from collections import defaultdict
import logging

from django.db import transaction
from django.utils import timezone

from apps.applications.models import Application
from apps.hostels.models import Hostel, Room, BedSpace
from apps.students.models import StudentProfile
from .models import Allocation, AllocationRun, AuditLog
from apps.applications.models import WaitingList
from .ml_models.predictor import get_predictor
from utils.constants import ALLOCATION_CONSTRAINTS
from utils.exceptions import (
    AllocationError, InsufficientCapacityError,
    GenderMismatchError, RoomFullError
)

logger = logging.getLogger(__name__)


@dataclass
class AllocationResult:
    """Result of a single allocation."""
    application_id: int
    student_id: int
    student_name: str
    room_id: int
    room_number: str
    hostel_name: str
    bed_space_number: Optional[int]
    success: bool
    message: str


class AllocationEngine:
    """
    Core allocation engine that assigns rooms to students
    based on priority scores and constraints.
    """
    
    def __init__(self, run_record: Optional[AllocationRun] = None):
        """
        Initialize the allocation engine.
        
        Args:
            run_record: Optional AllocationRun record for tracking
        """
        self.run_record = run_record
        self.predictor = get_predictor()
        self.results: List[AllocationResult] = []
        self.waiting_list: List[Application] = []
    
    def calculate_priority_scores(self, applications: List[Application]) -> Dict[int, float]:
        """
        Calculate priority scores for all applications.
        
        Args:
            applications: List of applications to score
        
        Returns:
            Dictionary mapping application IDs to priority scores
        """
        scores = {}
        
        for app in applications:
            try:
                # Get prediction
                prediction = self.predictor.predict(
                    app.student,
                    use_domain_knowledge=True
                )
                
                score = prediction['priority_score']
                
                # Apply seniority boost for 400/500 level students
                if ALLOCATION_CONSTRAINTS.get('seniority_boost'):
                    if app.student.level in [400, 500]:
                        score *= ALLOCATION_CONSTRAINTS['seniority_boost']
                
                # Ensure disability priority
                if ALLOCATION_CONSTRAINTS.get('disability_priority'):
                    if app.student.disability_status:
                        score = max(score, 95.0)  # Minimum score for disabled students
                
                # Clamp to valid range
                score = max(0.0, min(100.0, score))
                
                scores[app.id] = score
                
                # Update application with score
                app.priority_score = score
                app.ai_confidence = prediction.get('confidence', 0.8)
                
                # Store feature contributions
                features = prediction.get('feature_importance', {})
                app.gpa_factor = features.get('gpa_normalized', 0) * 40
                app.distance_factor = features.get('distance_transformed', 0) * 30
                app.level_factor = features.get('level_encoded', 0) * 20
                app.need_factor = (
                    features.get('disability_flag', 0) * 5 +
                    features.get('financial_aid_flag', 0) * 5
                )
                
                app.save()
                
                # Create audit log
                AuditLog.objects.create(
                    action='PRIORITY_CALCULATED',
                    application=app,
                    details={
                        'priority_score': score,
                        'confidence': app.ai_confidence,
                        'scoring_method': prediction.get('scoring_method', 'unknown'),
                    },
                    input_features=prediction.get('feature_importance'),
                    model_version=prediction.get('model_version', 'unknown'),
                    raw_score=prediction.get('raw_score'),
                    final_score=score,
                )
                
            except Exception as e:
                logger.error(f"Error calculating score for app {app.id}: {e}")
                scores[app.id] = 0.0
        
        return scores
    
    def allocate_batch(
        self,
        applications: List[Application],
        academic_session: str
    ) -> Tuple[List[AllocationResult], List[Application]]:
        """
        Run batch allocation for multiple applications.
        
        Args:
            applications: List of applications to allocate
            academic_session: Academic session for this allocation
        
        Returns:
            Tuple of (successful allocations, waiting list)
        """
        logger.info(f"Starting batch allocation for {len(applications)} applications")
        
        # Step 1: Calculate priority scores
        logger.info("Calculating priority scores...")
        scores = self.calculate_priority_scores(applications)
        
        # Step 2: Sort applications by priority score (descending)
        sorted_apps = sorted(
            applications,
            key=lambda a: (scores.get(a.id, 0), a.application_date),
            reverse=True
        )
        
        # Step 3: Get available rooms grouped by gender
        rooms_by_gender = self._get_available_rooms_by_gender()
        
        # Step 4: Allocate students
        successful = []
        waiting_list = []
        
        with transaction.atomic():
            for app in sorted_apps:
                try:
                    result = self._allocate_single(app, rooms_by_gender)
                    
                    if result.success:
                        successful.append(result)
                        
                        # Create allocation record
                        allocation = Allocation.objects.create(
                            application=app,
                            room_id=result.room_id,
                            bed_space_number=result.bed_space_number,
                            allocated_by='AI_System',
                            allocation_reason=result.message,
                        )
                        
                        # Mark application as allocated
                        app.mark_allocated()
                        
                        # Update room occupancy
                        room = Room.objects.get(id=result.room_id)
                        room.increment_occupancy()
                        
                        # Create audit log
                        AuditLog.objects.create(
                            action='ALLOCATION_CREATED',
                            application=app,
                            allocation=allocation,
                            details={
                                'room_id': result.room_id,
                                'room_number': result.room_number,
                                'hostel_name': result.hostel_name,
                                'priority_score': app.priority_score,
                            }
                        )
                        
                    else:
                        waiting_list.append(app)
                        
                except Exception as e:
                    logger.error(f"Error allocating app {app.id}: {e}")
                    waiting_list.append(app)
        
        # Step 5: Create waiting list entries
        for position, app in enumerate(waiting_list, 1):
            WaitingList.objects.create(
                application=app,
                position=position,
                is_priority=app.student.disability_status,
            )
        
        self.results = successful
        self.waiting_list = waiting_list
        
        # Update run record if provided
        if self.run_record:
            self.run_record.total_applications = len(applications)
            self.run_record.successful_allocations = len(successful)
            self.run_record.waiting_list_count = len(waiting_list)
            self.run_record.mark_completed()
        
        logger.info(
            f"Batch allocation complete: "
            f"{len(successful)} successful, {len(waiting_list)} on waiting list"
        )
        
        return successful, waiting_list
    
    def _get_available_rooms_by_gender(self) -> Dict[str, List[Room]]:
        """
        Get available rooms grouped by gender type.
        
        Returns:
            Dictionary mapping gender to list of available rooms
        """
        rooms = Room.objects.filter(
            is_active=True,
            is_under_maintenance=False,
        ).select_related('hostel').prefetch_related('bed_spaces')
        
        rooms_by_gender = defaultdict(list)
        
        for room in rooms:
            if room.is_available:
                gender = room.hostel.gender_type
                rooms_by_gender[gender].append(room)
        
        # Sort by accessibility (accessible rooms first), then by room number
        for gender in rooms_by_gender:
            rooms_by_gender[gender].sort(
                key=lambda r: (not r.is_accessible, r.room_number)
            )
        
        return dict(rooms_by_gender)
    
    def _allocate_single(
        self,
        application: Application,
        rooms_by_gender: Dict[str, List[Room]]
    ) -> AllocationResult:
        """
        Allocate a single student to a room.
        
        Args:
            application: Application to allocate
            rooms_by_gender: Available rooms grouped by gender
        
        Returns:
            AllocationResult
        """
        student = application.student
        
        # Determine eligible room types
        if student.gender == 'M':
            eligible_genders = ['male', 'mixed']
        elif student.gender == 'F':
            eligible_genders = ['female', 'mixed']
        else:
            eligible_genders = ['mixed']
        
        # Collect eligible rooms
        eligible_rooms = []
        for gender in eligible_genders:
            eligible_rooms.extend(rooms_by_gender.get(gender, []))
        
        if not eligible_rooms:
            return AllocationResult(
                application_id=application.id,
                student_id=student.id,
                student_name=student.user.full_name,
                room_id=0,
                room_number='',
                hostel_name='',
                bed_space_number=None,
                success=False,
                message='No available rooms matching gender requirements'
            )
        
        # Filter for accessible rooms if needed
        if student.disability_status:
            accessible_rooms = [r for r in eligible_rooms if r.is_accessible]
            if accessible_rooms:
                eligible_rooms = accessible_rooms
        
        # Filter for preferred hostel if specified
        if application.preferred_hostel:
            preferred_rooms = [
                r for r in eligible_rooms
                if r.hostel.id == application.preferred_hostel.id
            ]
            if preferred_rooms:
                eligible_rooms = preferred_rooms
        
        # Find best available room
        selected_room = None
        selected_bed_space = None
        
        for room in eligible_rooms:
            # Find available bed space
            bed_space = room.bed_spaces.filter(
                is_occupied=False,
                is_active=True
            ).first()
            
            if bed_space:
                selected_room = room
                selected_bed_space = bed_space
                break
        
        if not selected_room:
            return AllocationResult(
                application_id=application.id,
                student_id=student.id,
                student_name=student.user.full_name,
                room_id=0,
                room_number='',
                hostel_name='',
                bed_space_number=None,
                success=False,
                message='No available bed spaces'
            )
        
        # Mark bed space as occupied
        selected_bed_space.allocate()
        
        return AllocationResult(
            application_id=application.id,
            student_id=student.id,
            student_name=student.user.full_name,
            room_id=selected_room.id,
            room_number=selected_room.room_number,
            hostel_name=selected_room.hostel.name,
            bed_space_number=selected_bed_space.space_number,
            success=True,
            message=f'Allocated to {selected_room.hostel.name}, Room {selected_room.room_number}'
        )
    
    def manual_override(
        self,
        application: Application,
        room: Room,
        bed_space: Optional[BedSpace] = None,
        admin_user=None,
        reason: str = ''
    ) -> Allocation:
        """
        Manually override an allocation.
        
        Args:
            application: Application to allocate
            room: Room to assign
            bed_space: Specific bed space (optional)
            admin_user: Admin performing the override
            reason: Reason for override
        
        Returns:
            New or updated Allocation
        """
        with transaction.atomic():
            # Cancel existing allocation if any
            try:
                existing = application.allocation
                existing.cancel(reason='Overridden by admin')
            except Allocation.DoesNotExist:
                pass
            
            # Create new allocation
            allocation = Allocation.objects.create(
                application=application,
                room=room,
                bed_space=bed_space,
                bed_space_number=bed_space.space_number if bed_space else None,
                allocated_by='Admin_User',
                allocated_by_user=admin_user,
                allocation_reason=reason,
                admin_override=True,
            )
            
            # Update application
            application.mark_allocated()
            
            # Update room occupancy
            if bed_space:
                bed_space.allocate()
            else:
                room.increment_occupancy()
            
            # Create audit log
            AuditLog.objects.create(
                action='MANUAL_OVERRIDE',
                user=admin_user,
                application=application,
                allocation=allocation,
                details={
                    'room_id': room.id,
                    'reason': reason,
                }
            )
            
            logger.info(
                f"Manual override: App {application.id} -> Room {room.id} by {admin_user}"
            )
            
            return allocation
