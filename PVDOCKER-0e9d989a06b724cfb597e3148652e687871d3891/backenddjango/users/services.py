from .models import Notification, User, NotificationPreference, EmailLog
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import json
import logging

logger = logging.getLogger(__name__)


def create_notification(user, title, message, notification_type, related_object_id=None, related_object_type=None):
    """
    Create a notification for a user
    
    Args:
        user: User to create notification for
        title: Notification title
        message: Notification message
        notification_type: Type of notification
        related_object_id: ID of related object (optional)
        related_object_type: Type of related object (optional)
        
    Returns:
        Created Notification object or None if notification preferences prevent creation
    """
    # Check if user has notification preferences
    try:
        preferences = NotificationPreference.objects.get(user=user)
        
        # Check if user wants in-app notifications for this type
        if not preferences.get_in_app_preference(notification_type):
            return None
    except NotificationPreference.DoesNotExist:
        # If no preferences exist, create default preferences
        preferences = NotificationPreference.objects.create(user=user)
    
    # Create the notification
    notification = Notification.objects.create(
        user=user,
        title=title,
        message=message,
        notification_type=notification_type,
        related_object_id=related_object_id,
        related_object_type=related_object_type
    )
    
    # Send real-time notification via WebSocket
    try:
        channel_layer = get_channel_layer()
        notification_data = {
            'id': notification.id,
            'title': notification.title,
            'message': notification.message,
            'notification_type': notification.notification_type,
            'related_object_id': notification.related_object_id,
            'related_object_type': notification.related_object_type,
            'is_read': notification.is_read,
            'created_at': notification.created_at.isoformat()
        }
        
        # Send notification to user's group
        async_to_sync(channel_layer.group_send)(
            f"user_{user.id}_notifications",
            {
                'type': 'notification_message',
                'notification': notification_data
            }
        )
        
        # Update unread count
        unread_count = Notification.objects.filter(user=user, is_read=False).count()
        async_to_sync(channel_layer.group_send)(
            f"user_{user.id}_notifications",
            {
                'type': 'notification_count',
                'count': unread_count
            }
        )
    except Exception as e:
        # Log the error but don't fail the notification creation
        logger.error(f"Error sending WebSocket notification: {str(e)}")
    
    # Check if user wants email notifications for this type
    try:
        if preferences.get_email_preference(notification_type):
            send_email_notification(
                user=user,
                subject=title,
                message=message,
                notification=notification
            )
    except Exception as e:
        # Log the error but don't fail the notification creation
        logger.error(f"Error sending email notification: {str(e)}")
    
    return notification


def create_application_notification(application, notification_type, title, message):
    """
    Create notifications for users related to an application
    
    Args:
        application: Application object
        notification_type: Type of notification
        title: Notification title
        message: Notification message
        
    Returns:
        List of created Notification objects
    """
    notifications = []
    
    # Notify broker
    if application.broker and application.broker.user:
        broker_notification = create_notification(
            user=application.broker.user,
            title=title,
            message=message,
            notification_type=notification_type,
            related_object_id=application.id,
            related_object_type='application'
        )
        if broker_notification:
            notifications.append(broker_notification)
    
    # Notify BD
    if application.bd and application.bd.user:
        bd_notification = create_notification(
            user=application.bd.user,
            title=title,
            message=message,
            notification_type=notification_type,
            related_object_id=application.id,
            related_object_type='application'
        )
        if bd_notification:
            notifications.append(bd_notification)
    
    # Notify borrowers who have user accounts
    for borrower in application.borrowers.all():
        if borrower.user:
            borrower_notification = create_notification(
                user=borrower.user,
                title=title,
                message=message,
                notification_type=notification_type,
                related_object_id=application.id,
                related_object_type='application'
            )
            if borrower_notification:
                notifications.append(borrower_notification)
    
    # Notify admin users
    admin_users = User.objects.filter(role='admin')
    for admin in admin_users:
        admin_notification = create_notification(
            user=admin,
            title=title,
            message=message,
            notification_type=notification_type,
            related_object_id=application.id,
            related_object_type='application'
        )
        if admin_notification:
            notifications.append(admin_notification)
    
    return notifications


def send_email_notification(user, subject, message, notification=None, template_name=None, context=None, email_type=None):
    """
    Send an email notification to a user
    
    Args:
        user: User to send email to
        subject: Email subject
        message: Email message (plain text)
        notification: Related Notification object (optional)
        template_name: HTML email template name (optional)
        context: Context for HTML email template (optional)
        email_type: Type of email being sent (optional)
        
    Returns:
        Boolean indicating success or failure
    """
    from crm_backend.tasks import send_email_async
    
    if not user.email:
        logger.warning(f"Cannot send email to user {user.id}: No email address")
        return False
    
    try:
        html_message = None
        
        # If template is provided, render HTML email
        if template_name and context:
            # Add user to context if not already present
            if 'user' not in context:
                context['user'] = user
                
            # Render HTML template
            html_message = render_to_string(template_name, context)
            
            # If plain text message not provided, generate from HTML
            if not message:
                message = strip_tags(html_message)
        
        # Send email asynchronously
        send_email_async.delay(
            subject=subject,
            message=message,
            recipient_list=[user.email],
            html_message=html_message,
            user_id=user.id,
            notification_id=notification.id if notification else None,
            email_type=email_type
        )
        
        return True
    except Exception as e:
        logger.exception(f"Error queuing email notification: {str(e)}")
        return False


def get_or_create_notification_preferences(user):
    """
    Get or create notification preferences for a user
    
    Args:
        user: User to get or create preferences for
        
    Returns:
        NotificationPreference object
    """
    preferences, created = NotificationPreference.objects.get_or_create(user=user)
    return preferences


def preview_email(template_name, context):
    """
    Preview an email template with the given context.
    Only available in development mode.
    
    Args:
        template_name: Name of the template file
        context: Context data for the template
        
    Returns:
        HTML content of the rendered template
    """
    if not settings.DEBUG:
        raise PermissionError("Email preview is only available in development mode")
    
    return render_to_string(template_name, context)
