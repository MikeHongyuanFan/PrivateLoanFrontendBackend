"""
Abstract base models for shared functionality across the applications package.

These models provide common patterns that are reused across multiple models:
- Timestamped: created_at, updated_at tracking
- UserTracking: created_by, updated_by tracking with timestamps  
- BaseApplication: Standard metadata for application-related models
"""

from django.db import models
from django.conf import settings
from django.utils import timezone


class TimestampedModel(models.Model):
    """
    Abstract base model that provides timestamp tracking.
    
    Provides:
    - created_at: When the record was created
    - updated_at: When the record was last updated
    """
    created_at = models.DateTimeField(
        default=timezone.now,
        help_text="When this record was created"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        help_text="When this record was last updated"
    )
    
    class Meta:
        abstract = True


class UserTrackingModel(TimestampedModel):
    """
    Abstract base model that provides user and timestamp tracking.
    
    Extends TimestampedModel with:
    - created_by: Who created the record
    """
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="created_%(class)s_set",
        help_text="User who created this record"
    )
    
    class Meta:
        abstract = True


class BaseApplicationModel(UserTrackingModel):
    """
    Abstract base model for application-related entities.
    
    Provides standard metadata fields that most application-related
    models should have. Extends UserTrackingModel.
    """
    
    class Meta:
        abstract = True
        ordering = ['-created_at'] 