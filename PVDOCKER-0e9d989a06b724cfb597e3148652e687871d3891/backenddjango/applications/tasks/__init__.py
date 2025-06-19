# Application Tasks Package
# This file aggregates all tasks for easy importing

# Notification tasks
from .notifications import (
    check_stagnant_applications,
    check_stale_applications,
    check_note_reminders,
    check_repayment_reminders
)

# For backward compatibility - keep all the old imports working
__all__ = [
    'check_stagnant_applications',
    'check_stale_applications', 
    'check_note_reminders',
    'check_repayment_reminders',
] 