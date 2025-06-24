from celery.schedules import crontab

# Celery Beat Schedule
CELERY_BEAT_SCHEDULE = {
    # Active Loan Alerts
    'send-active-loan-payment-reminders': {
        'task': 'applications.tasks.send_active_loan_payment_reminders',
        'schedule': crontab(hour=9, minute=0),  # Daily at 9:00 AM
    },
    'send-active-loan-expiry-warnings': {
        'task': 'applications.tasks.send_active_loan_expiry_warnings',
        'schedule': crontab(hour=9, minute=30),  # Daily at 9:30 AM
    },
    'send-critical-expiry-alerts': {
        'task': 'applications.tasks.send_critical_expiry_alerts',
        'schedule': crontab(hour=10, minute=0),  # Daily at 10:00 AM
    },
    'cleanup-old-active-loan-notifications': {
        'task': 'applications.tasks.cleanup_old_active_loan_notifications',
        'schedule': crontab(day_of_week=1, hour=2, minute=0),  # Weekly on Monday at 2:00 AM
    },
} 