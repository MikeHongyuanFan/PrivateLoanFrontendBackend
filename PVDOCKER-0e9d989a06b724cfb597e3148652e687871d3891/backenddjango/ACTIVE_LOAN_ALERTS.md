# Active Loan Alert System Documentation

## Overview

The Active Loan Alert System provides automated and manual notification capabilities for managing active loans. It includes periodic tasks for payment reminders and expiry warnings, as well as immediate alert functionality for urgent notifications.

## Features

### 1. Automated Periodic Alerts

#### Payment Reminders (14 days before due)
- **Task**: `send_active_loan_payment_reminders`
- **Schedule**: Daily at 9:00 AM
- **Trigger**: Interest payments due in exactly 14 days
- **Recipients**: Admin users and Super Users
- **Priority**: Medium

#### Expiry Warnings (30 days before expiry)
- **Task**: `send_active_loan_expiry_warnings`
- **Schedule**: Daily at 9:30 AM
- **Trigger**: Loans expiring in exactly 30 days
- **Recipients**: Admin users and Super Users
- **Priority**: High

#### Critical Expiry Alerts (7 days before expiry)
- **Task**: `send_critical_expiry_alerts`
- **Schedule**: Daily at 10:00 AM
- **Trigger**: Loans expiring in exactly 7 days
- **Recipients**: Admin users and Super Users
- **Priority**: Critical

#### Cleanup Task (Weekly)
- **Task**: `cleanup_old_active_loan_notifications`
- **Schedule**: Weekly on Monday at 2:00 AM
- **Purpose**: Remove notifications older than 90 days

### 2. Immediate Manual Alerts

#### API Endpoint
```
POST /api/applications/active-loans/{id}/send_alert/
```

#### Request Body
```json
{
    "alert_type": "payment|expiry|manual",
    "message": "Custom message (optional)",
    "user_id": "Specific user ID (optional)"
}
```

#### Alert Types
- **payment**: Interest payment alerts
- **expiry**: Loan expiry alerts
- **manual**: Custom manual alerts

### 3. Frontend Integration

#### Alert Form Component
The Active Loan Details component includes an alert form with:
- Alert type selection dropdown
- Custom message textarea
- Priority indicator
- Send and Reset buttons

#### Notification Display
Alerts are displayed in the existing notification system with:
- Priority-based styling
- Click-through to related loan
- Mark as read functionality

## Technical Implementation

### Backend Components

#### 1. Celery Tasks (`applications/tasks.py`)
```python
@shared_task
def send_active_loan_payment_reminders():
    # Sends payment reminders 14 days before due

@shared_task
def send_active_loan_expiry_warnings():
    # Sends expiry warnings 30 days before expiry

@shared_task
def send_critical_expiry_alerts():
    # Sends critical alerts 7 days before expiry

@shared_task
def send_immediate_active_loan_alert(loan_id, alert_type, message=None, user_id=None):
    # Sends immediate alerts for specific loans

@shared_task
def cleanup_old_active_loan_notifications():
    # Cleans up old notifications
```

#### 2. API Views (`applications/views/active_loan_views.py`)
```python
@action(detail=True, methods=['post'])
def send_alert(self, request, pk=None):
    # Handles immediate alert requests
```

#### 3. Celery Beat Schedule (`loan_management/settings.py`)
```python
CELERY_BEAT_SCHEDULE = {
    'send-active-loan-payment-reminders': {
        'task': 'applications.tasks.send_active_loan_payment_reminders',
        'schedule': crontab(hour=9, minute=0),
    },
    # ... other scheduled tasks
}
```

### Frontend Components

#### 1. Active Loan Details Component (`activeloandetails.vue`)
- Alert form with type selection
- Custom message input
- Priority indicators
- Send/Reset functionality

#### 2. API Integration (`activeloans/index.js`)
```javascript
export function sendActiveLoanAlert(id, alertType = 'manual', message = null) {
    return sendRequest({
        url: `/api/applications/active-loans/${id}/send_alert/`,
        method: 'post',
        data: { 
            alert_type: alertType,
            message: message
        }
    })
}
```

## Usage Examples

### 1. Testing Celery Tasks
```bash
# Run the test script
python test_celery_tasks.py

# Or trigger tasks manually
python manage.py shell
>>> from applications.tasks import send_immediate_active_loan_alert
>>> send_immediate_active_loan_alert.delay(loan_id=1, alert_type='payment')
```

### 2. Sending Immediate Alert via API
```bash
curl -X POST \
  http://localhost:8000/api/applications/active-loans/1/send_alert/ \
  -H 'Content-Type: application/json' \
  -d '{
    "alert_type": "expiry",
    "message": "Urgent: Loan expiring soon!"
  }'
```

### 3. Frontend Usage
```javascript
// Send alert from frontend
const [error, data] = await api.sendActiveLoanAlert(
    loanId, 
    'payment', 
    'Custom payment reminder'
)
```

## Configuration

### Environment Variables
```bash
# Celery configuration
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/0

# Notification settings
NOTIFICATION_EMAIL_ENABLED=true
NOTIFICATION_PUSH_ENABLED=true
```

### Database Requirements
- `ActiveLoan` model with payment and expiry date fields
- `Notification` model for storing alerts
- `User` model with role-based permissions

## Monitoring and Debugging

### 1. Celery Task Monitoring
```bash
# Check Celery worker status
celery -A loan_management status

# Monitor task execution
celery -A loan_management events

# View task results
celery -A loan_management inspect active
```

### 2. Logging
Tasks include comprehensive logging:
- Task execution start/end
- Notification creation details
- Error handling and recovery
- Performance metrics

### 3. Testing
```bash
# Run test script
python test_celery_tasks.py

# Test specific scenarios
python manage.py shell
>>> from applications.tasks import *
>>> # Test individual tasks
```

## Troubleshooting

### Common Issues

#### 1. Tasks Not Running
- Check Celery worker is running
- Verify Celery Beat is running
- Check Redis connection
- Review task logs

#### 2. Notifications Not Appearing
- Verify user permissions
- Check notification preferences
- Review notification model fields
- Check frontend notification component

#### 3. Alert Form Not Working
- Check API endpoint availability
- Verify CSRF tokens
- Review browser console for errors
- Check network requests

### Debug Commands
```bash
# Check Celery configuration
python manage.py shell
>>> from django.conf import settings
>>> print(settings.CELERY_BEAT_SCHEDULE)

# Test notification creation
python manage.py shell
>>> from notifications.models import Notification
>>> from django.contrib.auth import get_user_model
>>> User = get_user_model()
>>> user = User.objects.first()
>>> Notification.objects.create(user=user, title="Test", message="Test message")
```

## Security Considerations

### 1. Permission Checks
- Only admin users and super users receive alerts
- User-specific alerts require proper authentication
- API endpoints require proper permissions

### 2. Data Validation
- Alert types are validated against allowed values
- Message content is sanitized
- User IDs are validated before sending

### 3. Rate Limiting
- Consider implementing rate limiting for immediate alerts
- Monitor task execution frequency
- Set appropriate cleanup schedules

## Future Enhancements

### 1. Additional Alert Types
- Document upload reminders
- Compliance alerts
- System maintenance notifications

### 2. Enhanced Scheduling
- Configurable reminder intervals
- Holiday-aware scheduling
- Timezone support

### 3. Advanced Features
- Email notifications
- SMS alerts
- Push notifications
- Alert escalation rules

### 4. Analytics
- Alert effectiveness tracking
- Response time metrics
- User engagement analytics

## Support

For issues or questions regarding the Active Loan Alert System:
1. Check the troubleshooting section
2. Review Celery and Django logs
3. Test with the provided test script
4. Contact the development team 