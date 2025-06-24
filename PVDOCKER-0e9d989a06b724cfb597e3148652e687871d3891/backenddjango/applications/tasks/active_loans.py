"""
Tasks for Active Loan notifications and management.

This module contains Celery tasks for:
- Sending payment reminders for active loans
- Sending expiry warnings for loans nearing their end date
- Sending critical alerts for loans that are about to expire
- Sending immediate alerts for specific loan events
- Cleaning up old notifications
"""

from celery import shared_task
from django.utils import timezone
from django.db.models import Q
from datetime import timedelta
import logging

from ..models import ActiveLoan, Application
from django.contrib.auth import get_user_model
from users.services import create_notification
from users.models import User
from users.models import NotificationPreference

User = get_user_model()
logger = logging.getLogger(__name__)

@shared_task
def send_active_loan_payment_reminders():
    """
    Send reminders for upcoming interest payments.
    
    This task checks for active loans with interest payments due in the next 7 days
    and sends notifications to relevant staff.
    """
    today = timezone.now().date()
    reminder_threshold = today + timedelta(days=7)
    
    # Find loans with payments due in the next 7 days
    active_loans = ActiveLoan.objects.filter(
        is_active=True,
        interest_payments_required=True
    ).select_related('application')
    
    reminder_count = 0
    for loan in active_loans:
        # Check if any payment dates are within the reminder threshold
        for due_date_str in loan.interest_payment_due_dates:
            try:
                due_date = timezone.datetime.strptime(due_date_str, "%Y-%m-%d").date()
                if today <= due_date <= reminder_threshold:
                    days_until = (due_date - today).days
                    
                    # Create notification message
                    title = f"Payment Reminder: {loan.application.reference_number}"
                    message = f"Interest payment due in {days_until} days on {due_date} for loan {loan.application.reference_number}"
                    
                    # Send notifications to admin users
                    admin_users = User.objects.filter(role__in=['admin', 'accounts', 'super_user'])
                    for user in admin_users:
                        create_notification(
                            user=user,
                            title=title,
                            message=message,
                            notification_type='active_loan_payment',
                            related_object_id=loan.id,
                            related_object_type='active_loan'
                        )
                    
                    # Log the notification
                    logger.info(
                        f"Payment reminder for loan {loan.id} (App: {loan.application.reference_number}): "
                        f"Payment due in {days_until} days on {due_date}"
                    )
                    reminder_count += 1
                    break  # Only send one reminder per loan
            except (ValueError, TypeError):
                logger.error(f"Invalid date format in loan {loan.id}: {due_date_str}")
    
    return f"Sent {reminder_count} payment reminders"

@shared_task
def send_active_loan_expiry_warnings():
    """
    Send warnings for loans nearing their expiry date.
    
    This task checks for active loans expiring in the next 30 days
    and sends notifications to relevant staff.
    """
    today = timezone.now().date()
    warning_threshold = today + timedelta(days=30)
    
    # Find loans expiring in the next 30 days
    expiring_loans = ActiveLoan.objects.filter(
        is_active=True,
        loan_expiry_date__lte=warning_threshold,
        loan_expiry_date__gt=today
    ).select_related('application')
    
    warning_count = 0
    for loan in expiring_loans:
        days_until = (loan.loan_expiry_date - today).days
        
        # Create notification message
        title = f"Loan Expiry Warning: {loan.application.reference_number}"
        message = f"Loan {loan.application.reference_number} expires in {days_until} days on {loan.loan_expiry_date}"
        
        # Send notifications to admin users
        admin_users = User.objects.filter(role__in=['admin', 'accounts', 'super_user'])
        for user in admin_users:
            create_notification(
                user=user,
                title=title,
                message=message,
                notification_type='active_loan_expiry',
                related_object_id=loan.id,
                related_object_type='active_loan'
            )
        
        # Log the notification
        logger.info(
            f"Expiry warning for loan {loan.id} (App: {loan.application.reference_number}): "
            f"Expires in {days_until} days on {loan.loan_expiry_date}"
        )
        warning_count += 1
    
    return f"Sent {warning_count} expiry warnings"

@shared_task
def send_critical_expiry_alerts():
    """
    Send critical alerts for loans expiring very soon.
    
    This task checks for active loans expiring in the next 7 days
    and sends urgent notifications to relevant staff.
    """
    today = timezone.now().date()
    critical_threshold = today + timedelta(days=7)
    
    # Find loans expiring in the next 7 days
    critical_loans = ActiveLoan.objects.filter(
        is_active=True,
        loan_expiry_date__lte=critical_threshold,
        loan_expiry_date__gt=today
    ).select_related('application')
    
    alert_count = 0
    for loan in critical_loans:
        days_until = (loan.loan_expiry_date - today).days
        
        # Create notification message
        title = f"CRITICAL: Loan Expiry Alert: {loan.application.reference_number}"
        message = f"URGENT: Loan {loan.application.reference_number} expires in {days_until} days on {loan.loan_expiry_date}"
        
        # Send notifications to admin users
        admin_users = User.objects.filter(role__in=['admin', 'accounts', 'super_user'])
        for user in admin_users:
            create_notification(
                user=user,
                title=title,
                message=message,
                notification_type='active_loan_critical',
                related_object_id=loan.id,
                related_object_type='active_loan'
            )
        
        # Log the notification
        logger.info(
            f"CRITICAL ALERT for loan {loan.id} (App: {loan.application.reference_number}): "
            f"Expires in {days_until} days on {loan.loan_expiry_date}"
        )
        alert_count += 1
    
    return f"Sent {alert_count} critical expiry alerts"

@shared_task
def send_immediate_active_loan_alert(loan_id, alert_type="manual", message=None, user_id=None):
    """
    Send an immediate alert for a specific loan.
    
    Args:
        loan_id: The ID of the ActiveLoan
        alert_type: Type of alert (payment, expiry, manual)
        message: Optional custom message
        user_id: Specific user to notify (optional, defaults to all admins)
    """
    try:
        loan = ActiveLoan.objects.get(id=loan_id)
        
        logger.info(f"=== SEND IMMEDIATE ALERT DEBUG ===")
        logger.info(f"Loan ID: {loan_id}")
        logger.info(f"Alert type: {alert_type}")
        logger.info(f"Message provided: {message}")
        logger.info(f"User ID: {user_id}")
        
        # Create notification message if not provided
        if not message:
            logger.info("No custom message provided, using default messages")
            if alert_type == "payment":
                title = f"Urgent Payment Reminder: {loan.application.reference_number}"
                message = f"Urgent payment reminder for loan {loan.application.reference_number}"
            elif alert_type == "expiry":
                title = f"Urgent Expiry Alert: {loan.application.reference_number}"
                message = f"Urgent expiry alert for loan {loan.application.reference_number}"
            else:
                title = f"Alert: {loan.application.reference_number}"
                message = f"Manual alert for loan {loan.application.reference_number}"
        else:
            # Use the custom message provided
            logger.info(f"Using custom message: {message}")
            title = f"Alert: {loan.application.reference_number}"
        
        logger.info(f"Final title: {title}")
        logger.info(f"Final message: {message}")
        
        # Determine notification type based on alert_type
        notification_type_map = {
            'payment': 'active_loan_payment',
            'expiry': 'active_loan_expiry',
            'manual': 'active_loan_manual'
        }
        notification_type = notification_type_map.get(alert_type, 'active_loan_manual')
        
        # Send notifications to specific user or all admin users
        if user_id:
            users = User.objects.filter(id=user_id)
            logger.info(f"Sending alert to specific user ID: {user_id}")
        else:
            users = User.objects.filter(role__in=['admin', 'accounts', 'super_user'])
            logger.info(f"Sending alert to all admin users. Found {users.count()} users with roles: admin, accounts, super_user")
        
        notifications_created = 0
        for user in users:
            logger.info(f"Processing user: {user.email} (ID: {user.id}, Role: {user.role})")
            
            # Check user's notification preferences
            try:
                preferences = NotificationPreference.objects.get(user=user)
                preference_enabled = preferences.get_in_app_preference(notification_type)
                logger.info(f"User {user.email} has preferences. {notification_type}_in_app: {preference_enabled}")
            except NotificationPreference.DoesNotExist:
                logger.info(f"User {user.email} has no preferences, creating default")
                preferences = NotificationPreference.objects.create(user=user)
                preference_enabled = preferences.get_in_app_preference(notification_type)
                logger.info(f"Created default preferences for {user.email}. {notification_type}_in_app: {preference_enabled}")
            
            if preference_enabled:
                notification = create_notification(
                    user=user,
                    title=title,
                    message=message,
                    notification_type=notification_type,
                    related_object_id=loan.id,
                    related_object_type='active_loan'
                )
                if notification:
                    notifications_created += 1
                    logger.info(f"Created notification for user {user.email}: {notification.id}")
                else:
                    logger.warning(f"Failed to create notification for user {user.email}")
            else:
                logger.info(f"Skipping notification for user {user.email} - preference disabled for {notification_type}")
        
        # Log the notification
        logger.info(
            f"Immediate alert ({alert_type}) for loan {loan.id} "
            f"(App: {loan.application.reference_number}): {message}. "
            f"Created {notifications_created} notifications out of {users.count()} users."
        )
        
        return f"Sent immediate alert for loan {loan_id} - {notifications_created} notifications created"
    except ActiveLoan.DoesNotExist:
        logger.error(f"Cannot send alert: ActiveLoan with ID {loan_id} does not exist")
        return f"Error: ActiveLoan with ID {loan_id} not found"

@shared_task
def cleanup_old_active_loan_notifications():
    """
    Clean up old notifications related to active loans.
    
    This task removes notifications older than 90 days to keep the system clean.
    """
    from users.models import Notification
    
    cutoff_date = timezone.now() - timedelta(days=90)
    
    # Delete old active loan notifications
    deleted_count = Notification.objects.filter(
        notification_type__in=[
            'active_loan_payment',
            'active_loan_expiry',
            'active_loan_critical',
            'active_loan_manual'
        ],
        created_at__lt=cutoff_date
    ).delete()[0]
    
    logger.info(f"Cleaned up {deleted_count} notifications older than {cutoff_date}")
    return f"Cleaned up {deleted_count} old notifications"
