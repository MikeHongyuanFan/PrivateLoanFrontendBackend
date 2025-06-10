import os
import sys
import django
from datetime import datetime, timedelta

# Set up Django environment
sys.path.append('./PVDOCKER-0e9d989a06b724cfb597e3148652e687871d3891/backenddjango')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'crm_backend.settings')
django.setup()

# Now import Django models
from reminders.models import Reminder
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.conf import settings

User = get_user_model()

try:
    # Get or create a user to be the creator
    user, created = User.objects.get_or_create(
        email='fanhongyuan897@gmail.com',
        defaults={
            'first_name': 'Test',
            'last_name': 'User',
            'is_staff': True,
            'is_active': True
        }
    )
    
    if created:
        user.set_password('testpassword123')
        user.save()
        print(f"Created new user: {user.email}")
    else:
        print(f"Using existing user: {user.email}")
    
    # Create a reminder
    reminder = Reminder.objects.create(
        recipient_type='custom',
        recipient_email='fanhongyuan897@gmail.com',
        send_datetime=datetime.now() + timedelta(minutes=1),
        email_body="This is a test email sent via the reminder API. The email configuration has been updated successfully.",
        subject="Test Email from Reminder API",
        created_by=user
    )
    
    print(f"Created reminder: {reminder}")
    
    # Send the email directly
    send_mail(
        subject=reminder.subject,
        message=reminder.email_body,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[reminder.recipient_email],
        fail_silently=False,
    )
    
    print("Email sent successfully!")
    
    # Update the reminder status
    reminder.is_sent = True
    reminder.sent_at = datetime.now()
    reminder.save()
    
    print("Reminder updated as sent.")
    
except Exception as e:
    print(f"Error: {str(e)}")
