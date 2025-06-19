#!/usr/bin/env python
import os
import django
from datetime import datetime, timedelta

# Django setup
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'crm_backend.settings')
django.setup()

from reminders.models import Reminder
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.conf import settings

User = get_user_model()

def create_and_send_reminder():
    try:
        # Get the existing user
        user = User.objects.get(email='fanhongyuan897@gmail.com')
        print(f"Using user: {user.email}")
        
        # Create a reminder
        reminder = Reminder.objects.create(
            recipient_type='custom',
            recipient_email='fanhongyuan897@gmail.com',
            send_datetime=datetime.now() + timedelta(minutes=1),
            email_body="This is a test email sent via the reminder API. The system is working correctly!",
            subject="Test Email from Reminder API - Success!",
            created_by=user
        )
        
        print(f"Created reminder: {reminder}")
        
        # Send the email immediately
        try:
            send_mail(
                subject=reminder.subject,
                message=reminder.email_body,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[reminder.recipient_email],
                fail_silently=False,
            )
            
            print("✅ Email sent successfully!")
            
            # Update the reminder status
            reminder.is_sent = True
            reminder.sent_at = datetime.now()
            reminder.save()
            
            print("✅ Reminder updated as sent.")
            return True
            
        except Exception as email_error:
            print(f"❌ Email sending failed: {str(email_error)}")
            return False
        
    except User.DoesNotExist:
        print("❌ User not found")
        return False
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

if __name__ == "__main__":
    create_and_send_reminder() 