"""
Signals for students app.
"""

from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from .models import StudentProfile, Document
import logging

logger = logging.getLogger(__name__)


@receiver(post_save, sender=StudentProfile)
def student_profile_post_save(sender, instance, created, **kwargs):
    """Handle post-save student profile operations."""
    if created:
        logger.info(f"Student profile created for user: {instance.user.email}")


@receiver(post_delete, sender=Document)
def document_post_delete(sender, instance, **kwargs):
    """Delete file when document record is deleted."""
    if instance.file:
        instance.file.delete(save=False)
        logger.info(f"Deleted file: {instance.file.name}")
