"""
Signals for applications app.
"""

from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from .models import Application, ApplicationPeriod
import logging

logger = logging.getLogger(__name__)


@receiver(post_save, sender=Application)
def application_post_save(sender, instance, created, **kwargs):
    """Handle post-save application operations."""
    if created:
        logger.info(
            f"New application created: {instance.id} by "
            f"{instance.student.user.email} for {instance.academic_session}"
        )


@receiver(pre_save, sender=ApplicationPeriod)
def application_period_pre_save(sender, instance, **kwargs):
    """Handle pre-save application period operations."""
    if instance.is_active:
        # Deactivate other periods when activating this one
        ApplicationPeriod.objects.filter(is_active=True).exclude(
            pk=instance.pk
        ).update(is_active=False)
