"""
Celery tasks for Applications.

This module imports all tasks from the tasks subdirectory to ensure
they are properly registered with Celery.
"""

# Import all tasks from the tasks subdirectory
from .tasks.notifications import (
    check_stagnant_applications,
    check_stale_applications,
    check_note_reminders,
    check_repayment_reminders
)

from .tasks.active_loans import (
    send_active_loan_payment_reminders,
    send_active_loan_expiry_warnings,
    send_critical_expiry_alerts,
    send_immediate_active_loan_alert,
    cleanup_old_active_loan_notifications
)

# For backward compatibility and explicit registration
__all__ = [
    # Application notification tasks
    'check_stagnant_applications',
    'check_stale_applications', 
    'check_note_reminders',
    'check_repayment_reminders',
    
    # Active loan tasks
    'send_active_loan_payment_reminders',
    'send_active_loan_expiry_warnings',
    'send_critical_expiry_alerts',
    'send_immediate_active_loan_alert',
    'cleanup_old_active_loan_notifications',
] 