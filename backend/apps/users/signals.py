"""
Signals for users app.
"""

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings

from .models import User
import logging

logger = logging.getLogger(__name__)


@receiver(post_save, sender=User)
def user_post_save(sender, instance, created, **kwargs):
    """Handle post-save user operations."""
    if created:
        logger.info(f"New user created: {instance.email}")
        
        # TODO: Send welcome email
        # TODO: Create notification preferences
        # TODO: Create audit log entry
