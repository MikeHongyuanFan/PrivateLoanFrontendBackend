# Application Tasks Package
# This file aggregates all tasks for easy importing

# Notification tasks
from .notifications import (
    check_stagnant_applications,
    check_stale_applications,
    check_note_reminders,
    check_repayment_reminders
)

# Active loan tasks
from .active_loans import (
    send_active_loan_payment_reminders,
    send_active_loan_expiry_warnings,
    send_critical_expiry_alerts,
    send_immediate_active_loan_alert,
    cleanup_old_active_loan_notifications
)

# For backward compatibility - keep all the old imports working
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