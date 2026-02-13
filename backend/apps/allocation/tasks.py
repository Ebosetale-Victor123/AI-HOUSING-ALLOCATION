"""
Celery tasks for allocation operations.
"""

from celery import shared_task
from django.db import transaction

from apps.applications.models import Application
from .models import AllocationRun
from .allocation_engine import AllocationEngine
import logging

logger = logging.getLogger(__name__)


@shared_task(bind=True, max_retries=3)
def run_batch_allocation(self, run_id: int):
    """
    Run batch allocation as a Celery task.
    
    Args:
        run_id: ID of the AllocationRun record
    """
    try:
        # Get the run record
        run_record = AllocationRun.objects.get(id=run_id)
        run_record.status = 'RUNNING'
        run_record.celery_task_id = self.request.id
        run_record.save()
        
        logger.info(f"Starting batch allocation run {run_id}")
        
        # Get pending applications for this session
        applications = Application.objects.filter(
            academic_session=run_record.academic_session,
            status='pending'
        ).select_related('student', 'student__user')
        
        if not applications.exists():
            run_record.mark_failed("No pending applications found")
            return {'status': 'failed', 'error': 'No pending applications'}
        
        # Initialize allocation engine
        engine = AllocationEngine(run_record=run_record)
        
        # Run allocation
        successful, waiting_list = engine.allocate_batch(
            list(applications),
            run_record.academic_session
        )
        
        logger.info(
            f"Batch allocation run {run_id} completed: "
            f"{len(successful)} successful, {len(waiting_list)} on waiting list"
        )
        
        return {
            'status': 'success',
            'run_id': run_id,
            'total': len(applications),
            'successful': len(successful),
            'waiting_list': len(waiting_list),
        }
        
    except AllocationRun.DoesNotExist:
        logger.error(f"AllocationRun {run_id} not found")
        return {'status': 'error', 'error': 'Run record not found'}
        
    except Exception as exc:
        logger.exception(f"Batch allocation run {run_id} failed")
        
        # Update run record with error
        try:
            run_record = AllocationRun.objects.get(id=run_id)
            run_record.mark_failed(str(exc))
        except:
            pass
        
        # Retry the task
        raise self.retry(exc=exc, countdown=60)


@shared_task
def send_allocation_notifications(allocation_ids: list):
    """
    Send email notifications to students about their allocations.
    
    Args:
        allocation_ids: List of Allocation IDs to notify
    """
    from .models import Allocation
    from django.core.mail import send_mail
    from django.conf import settings
    
    allocations = Allocation.objects.filter(
        id__in=allocation_ids
    ).select_related(
        'application__student__user',
        'room__hostel'
    )
    
    for allocation in allocations:
        try:
            student = allocation.application.student
            user = student.user
            room = allocation.room
            hostel = room.hostel
            
            subject = f'Room Allocation for {allocation.application.academic_session}'
            message = f"""
Dear {user.first_name},

We are pleased to inform you that you have been allocated a room for the {allocation.application.academic_session} academic session.

Allocation Details:
- Hostel: {hostel.name}
- Room Number: {room.room_number}
- Bed Space: {allocation.bed_space_number or 'N/A'}

Please log in to the housing portal to confirm your allocation.

Best regards,
Housing Office
"""
            
            send_mail(
                subject=subject,
                message=message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user.email],
                fail_silently=True,
            )
            
            logger.info(f"Allocation notification sent to {user.email}")
            
        except Exception as e:
            logger.error(f"Failed to send notification for allocation {allocation.id}: {e}")


@shared_task
def generate_allocation_report(run_id: int):
    """
    Generate allocation report after a batch run.
    
    Args:
        run_id: ID of the AllocationRun record
    """
    from .models import Allocation, AuditLog
    from apps.applications.models import WaitingList
    
    try:
        run_record = AllocationRun.objects.get(id=run_id)
        
        # Generate report data
        allocations = Allocation.objects.filter(
            application__academic_session=run_record.academic_session
        )
        
        waiting_list = WaitingList.objects.filter(
            application__academic_session=run_record.academic_session
        )
        
        report_data = {
            'run_id': run_id,
            'academic_session': run_record.academic_session,
            'started_at': run_record.started_at,
            'completed_at': run_record.completed_at,
            'total_applications': run_record.total_applications,
            'successful_allocations': run_record.successful_allocations,
            'waiting_list_count': run_record.waiting_list_count,
            'allocations_by_hostel': {},
            'average_priority_score': 0,
        }
        
        # Calculate statistics
        from django.db.models import Avg
        avg_score = allocations.aggregate(
            avg=Avg('application__priority_score')
        )['avg'] or 0
        report_data['average_priority_score'] = round(avg_score, 2)
        
        # Allocations by hostel
        from django.db.models import Count
        by_hostel = allocations.values(
            'room__hostel__name'
        ).annotate(
            count=Count('id')
        )
        report_data['allocations_by_hostel'] = {
            item['room__hostel__name']: item['count']
            for item in by_hostel
        }
        
        logger.info(f"Allocation report generated for run {run_id}")
        
        return report_data
        
    except AllocationRun.DoesNotExist:
        logger.error(f"AllocationRun {run_id} not found")
        return None
    except Exception as e:
        logger.error(f"Failed to generate report for run {run_id}: {e}")
        return None


@shared_task
def cleanup_old_allocation_runs(days: int = 30):
    """
    Clean up old allocation run records.
    
    Args:
        days: Delete runs older than this many days
    """
    from datetime import timedelta
    from django.utils import timezone
    
    cutoff_date = timezone.now() - timedelta(days=days)
    
    old_runs = AllocationRun.objects.filter(
        started_at__lt=cutoff_date,
        status__in=['COMPLETED', 'FAILED', 'CANCELLED']
    )
    
    count = old_runs.count()
    old_runs.delete()
    
    logger.info(f"Cleaned up {count} old allocation runs")
    
    return {'deleted': count}
