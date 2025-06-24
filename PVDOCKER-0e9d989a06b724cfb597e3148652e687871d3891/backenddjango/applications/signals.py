"""
Django signals for automatic Active Loan management.

This module contains signals that handle automatic creation of
ActiveLoan instances when application stages change to 'settled'.
"""

from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.utils import timezone
from datetime import timedelta
import logging

from .models import Application, ActiveLoan

logger = logging.getLogger(__name__)


@receiver(pre_save, sender=Application)
def track_stage_changes(sender, instance, **kwargs):
    """
    Track stage changes in applications for automatic active loan creation.
    
    This signal tracks when an application stage changes to 'settled'
    and prepares for ActiveLoan creation.
    """
    if instance.pk:  # Only for existing instances
        try:
            old_instance = Application.objects.get(pk=instance.pk)
            instance._previous_stage = old_instance.stage
        except Application.DoesNotExist:
            instance._previous_stage = None
    else:
        instance._previous_stage = None


@receiver(post_save, sender=Application)
def create_active_loan_on_settlement(sender, instance, created, **kwargs):
    """
    Automatically create ActiveLoan when application stage changes to 'settled'.
    
    This signal creates an ActiveLoan instance with default settings
    when an application is marked as settled.
    """
    if not created:  # Only for updates, not new creations
        previous_stage = getattr(instance, '_previous_stage', None)
        
        if instance.stage == 'settled' and previous_stage != 'settled':
            # Check if ActiveLoan doesn't already exist
            if not hasattr(instance, 'active_loan'):
                try:
                    # Create ActiveLoan with default values
                    active_loan = ActiveLoan.objects.create(
                        application=instance,
                        settlement_date=timezone.now().date(),
                        capitalised_interest_months=instance.capitalised_interest_term or 0,
                        interest_payments_required=False,  # Default to no interest payments
                        loan_expiry_date=timezone.now().date() + timedelta(days=365),  # Default 1 year
                        is_active=True
                    )
                    
                    logger.info(f"Created ActiveLoan {active_loan.id} for Application {instance.reference_number}")
                    
                except Exception as e:
                    logger.error(f"Failed to create ActiveLoan for Application {instance.reference_number}: {str(e)}")
            else:
                logger.info(f"ActiveLoan already exists for Application {instance.reference_number}")


@receiver(post_save, sender=ActiveLoan)
def log_active_loan_creation(sender, instance, created, **kwargs):
    """
    Log ActiveLoan creation for audit purposes.
    """
    if created:
        logger.info(f"New ActiveLoan created: {instance.id} for Application {instance.application.reference_number}")
        
        # Update application stage if not already settled
        if instance.application.stage != 'settled':
            instance.application.stage = 'settled'
            instance.application.save()
            logger.info(f"Updated Application {instance.application.reference_number} stage to 'settled'")


# Signal to handle stage history updates
@receiver(pre_save, sender=Application)
def update_stage_history(sender, instance, **kwargs):
    """
    Update stage history when application stage changes.
    
    This signal maintains a history of stage changes for audit purposes.
    """
    if instance.pk:  # Only for existing instances
        try:
            old_instance = Application.objects.get(pk=instance.pk)
            if old_instance.stage != instance.stage:
                # Initialize stage_history if it doesn't exist
                if not isinstance(instance.stage_history, list):
                    instance.stage_history = []
                
                # Add new stage change to history
                stage_change = {
                    'from_stage': old_instance.stage,
                    'to_stage': instance.stage,
                    'timestamp': timezone.now().isoformat(),
                    'user': getattr(instance, '_current_user', 'System'),
                    'notes': getattr(instance, '_stage_change_notes', 'Automatic stage change')
                }
                
                instance.stage_history.append(stage_change)
                
                logger.info(f"Stage changed for Application {instance.reference_number}: {old_instance.stage} -> {instance.stage}")
                
        except Application.DoesNotExist:
            pass 