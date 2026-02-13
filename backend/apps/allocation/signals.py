"""
Signals for allocation app.
"""

from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from .models import Allocation, AuditLog
import logging

logger = logging.getLogger(__name__)


@receiver(post_save, sender=Allocation)
def allocation_post_save(sender, instance, created, **kwargs):
    """Handle post-save allocation operations."""
    if created:
        logger.info(
            f"New allocation created: {instance.id} for "
            f"{instance.application.student.user.email}"
        )
