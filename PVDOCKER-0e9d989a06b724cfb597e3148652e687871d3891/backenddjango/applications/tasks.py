"""
Celery tasks for Active Loan management.

This module contains periodic tasks for automated alerts and notifications
for active loans, including payment reminders and expiry warnings.
"""

from celery import shared_task
from django.utils import timezone
from django.db.models import Q
from datetime import timedelta
from django.contrib.auth import get_user_model
from applications.models import ActiveLoan, ActiveLoanRepayment
from notifications.models import Notification
import logging

User = get_user_model()


@shared_task
def send_active_loan_payment_reminders():
    """
    Send payment reminders 14 days before interest payments are due.
    
    This task runs daily and checks for loans with payments due within 14 days.
    """
    today = timezone.now().date()
    reminder_date = today + timedelta(days=14)
    
    # Get all active loans with interest payments required
    active_loans = ActiveLoan.objects.filter(
        is_active=True,
        interest_payments_required=True
    ).select_related('application')
    
    notifications_created = 0
    
    for loan in active_loans:
        # Check each payment due date
        for date_str in loan.interest_payment_due_dates:
            try:
                due_date = timezone.datetime.strptime(date_str, '%Y-%m-%d').date()
                
                # If payment is due in exactly 14 days
                if due_date == reminder_date:
                    # Get admin users
                    admin_users = User.objects.filter(
                        Q(is_superuser=True) | 
                        Q(role__in=['admin', 'super_user'])
                    )
                    
                    for admin_user in admin_users:
                        # Create notification
                        Notification.objects.create(
                            user=admin_user,
                            title="Interest Payment Reminder",
                            message=f"Interest payment of ${loan.get_next_payment_amount()} is due in 14 days for loan {loan.application.reference_number}.",
                            notification_type="active_loan_payment",
                            related_object_type="ActiveLoan",
                            related_object_id=loan.id,
                            priority="medium"
                        )
                        notifications_created += 1
                        
            except (ValueError, TypeError):
                continue
    
    return f"Created {notifications_created} payment reminder notifications"


@shared_task
def send_active_loan_expiry_warnings():
    """
    Send expiry warnings 30 days before loan expiry.
    
    This task runs daily and checks for loans expiring within 30 days.
    """
    today = timezone.now().date()
    warning_date = today + timedelta(days=30)
    
    # Get active loans expiring in 30 days
    expiring_loans = ActiveLoan.objects.filter(
        is_active=True,
        loan_expiry_date=warning_date
    ).select_related('application')
    
    notifications_created = 0
    
    for loan in expiring_loans:
        # Get admin users
        admin_users = User.objects.filter(
            Q(is_superuser=True) | 
            Q(role__in=['admin', 'super_user'])
        )
        
        for admin_user in admin_users:
            # Create notification
            Notification.objects.create(
                user=admin_user,
                title="Loan Expiry Warning",
                message=f"Loan {loan.application.reference_number} expires in 30 days. Please review and take necessary action.",
                notification_type="active_loan_expiry",
                related_object_type="ActiveLoan",
                related_object_id=loan.id,
                priority="high"
            )
            notifications_created += 1
    
    return f"Created {notifications_created} expiry warning notifications"


@shared_task
def send_critical_expiry_alerts():
    """
    Send critical alerts 7 days before loan expiry.
    
    This task runs daily and checks for loans expiring within 7 days.
    """
    today = timezone.now().date()
    critical_date = today + timedelta(days=7)
    
    # Get active loans expiring in 7 days
    critical_loans = ActiveLoan.objects.filter(
        is_active=True,
        loan_expiry_date=critical_date
    ).select_related('application')
    
    notifications_created = 0
    
    for loan in critical_loans:
        # Get admin users
        admin_users = User.objects.filter(
            Q(is_superuser=True) | 
            Q(role__in=['admin', 'super_user'])
        )
        
        for admin_user in admin_users:
            # Create notification
            Notification.objects.create(
                user=admin_user,
                title="CRITICAL: Loan Expiry Alert",
                message=f"URGENT: Loan {loan.application.reference_number} expires in 7 days. Immediate action required.",
                notification_type="active_loan_critical",
                related_object_type="ActiveLoan",
                related_object_id=loan.id,
                priority="critical"
            )
            notifications_created += 1
    
    return f"Created {notifications_created} critical expiry notifications"


@shared_task
def cleanup_old_active_loan_notifications():
    """
    Clean up old active loan notifications (older than 90 days).
    
    This task runs weekly to keep the notification table clean.
    """
    cutoff_date = timezone.now() - timedelta(days=90)
    
    deleted_count = Notification.objects.filter(
        notification_type__startswith='active_loan_',
        created_at__lt=cutoff_date
    ).delete()[0]
    
    return f"Deleted {deleted_count} old active loan notifications" 