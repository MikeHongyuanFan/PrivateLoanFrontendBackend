from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from .managers import UserManager


class User(AbstractUser):
    """
    Custom User model with role-based permissions
    """
    ROLE_CHOICES = [
        ('accounts', 'Accounts'),
        ('admin', 'Admin'),
        ('business_development_manager', 'Business Development Manager'),
        ('business_development_associate', 'Business Development Associate'),
        ('credit_manager', 'Credit Manager'),
        ('super_user', 'Super User'),
        # Keep legacy roles for backward compatibility during migration
        ('broker', 'Broker'),
        ('bd', 'Business Development'),
        ('client', 'Client'),
    ]
    
    email = models.EmailField(_('email address'), unique=True)
    role = models.CharField(max_length=30, choices=ROLE_CHOICES, default='client')
    phone = models.CharField(max_length=20, blank=True, null=True)
    username = models.CharField(max_length=150, blank=True, null=True, default='')
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    
    objects = UserManager()
    
    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
    
    def __str__(self):
        return self.email
    
    def is_super_user_or_accounts(self):
        """
        Check if user has super user or accounts role
        """
        return self.role in ['super_user', 'accounts']
    
    def can_modify_commission_account(self):
        """
        Check if user can modify commission account
        Only super user and accounts can modify commission accounts
        """
        return self.role in ['super_user', 'accounts']


class Notification(models.Model):
    """
    Model for user notifications
    """
    NOTIFICATION_TYPE_CHOICES = [
        ('application_status', 'Application Status Change'),
        ('stage_change', 'Stage Change'),
        ('repayment_upcoming', 'Repayment Upcoming'),
        ('repayment_overdue', 'Repayment Overdue'),
        ('note_reminder', 'Note Reminder'),
        ('document_uploaded', 'Document Uploaded'),
        ('signature_required', 'Signature Required'),
        ('system', 'System Notification'),
        # Active Loan notification types
        ('active_loan_payment', 'Active Loan Payment Alert'),
        ('active_loan_expiry', 'Active Loan Expiry Alert'),
        ('active_loan_critical', 'Active Loan Critical Alert'),
        ('active_loan_manual', 'Active Loan Manual Alert'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    title = models.CharField(max_length=255)
    message = models.TextField()
    notification_type = models.CharField(max_length=50, choices=NOTIFICATION_TYPE_CHOICES)
    related_object_id = models.IntegerField(null=True, blank=True)
    related_object_type = models.CharField(max_length=50, null=True, blank=True)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    read_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.notification_type}: {self.title}"
    
    def mark_as_read(self):
        """
        Mark the notification as read
        """
        self.is_read = True
        self.read_at = timezone.now()
        self.save()


class EmailLog(models.Model):
    """
    Model for tracking email sending history
    """
    STATUS_CHOICES = [
        ('sent', 'Sent'),
        ('delivered', 'Delivered'),
        ('opened', 'Opened'),
        ('clicked', 'Clicked'),
        ('bounced', 'Bounced'),
        ('failed', 'Failed')
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='email_logs')
    subject = models.CharField(max_length=255)
    sent_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='sent')
    notification = models.ForeignKey(Notification, on_delete=models.SET_NULL, null=True, blank=True)
    message_body = models.TextField(null=True, blank=True)
    email_type = models.CharField(max_length=100, null=True, blank=True)
    
    class Meta:
        ordering = ['-sent_at']
        verbose_name = 'Email Log'
        verbose_name_plural = 'Email Logs'
    
    def __str__(self):
        return f"Email to {self.user.email}: {self.subject} ({self.status})"


class NotificationPreference(models.Model):
    """
    Model for user notification preferences
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='notification_preferences')
    
    # In-app notification preferences
    application_status_in_app = models.BooleanField(default=True)
    stage_change_in_app = models.BooleanField(default=True)
    repayment_upcoming_in_app = models.BooleanField(default=True)
    repayment_overdue_in_app = models.BooleanField(default=True)
    note_reminder_in_app = models.BooleanField(default=True)
    document_uploaded_in_app = models.BooleanField(default=True)
    signature_required_in_app = models.BooleanField(default=True)
    system_in_app = models.BooleanField(default=True)
    
    # Active loan notification preferences
    active_loan_payment_in_app = models.BooleanField(default=True)
    active_loan_expiry_in_app = models.BooleanField(default=True)
    active_loan_critical_in_app = models.BooleanField(default=True)
    active_loan_manual_in_app = models.BooleanField(default=True)
    
    # Email notification preferences
    application_status_email = models.BooleanField(default=True)
    stage_change_email = models.BooleanField(default=True)
    repayment_upcoming_email = models.BooleanField(default=True)
    repayment_overdue_email = models.BooleanField(default=True)
    note_reminder_email = models.BooleanField(default=True)
    document_uploaded_email = models.BooleanField(default=False)
    signature_required_email = models.BooleanField(default=True)
    system_email = models.BooleanField(default=False)
    
    # Active loan email preferences
    active_loan_payment_email = models.BooleanField(default=True)
    active_loan_expiry_email = models.BooleanField(default=True)
    active_loan_critical_email = models.BooleanField(default=True)
    active_loan_manual_email = models.BooleanField(default=True)
    
    # Email digest preferences
    daily_digest = models.BooleanField(default=False)
    weekly_digest = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Notification Preferences for {self.user.email}"
    
    def get_in_app_preference(self, notification_type):
        """
        Get in-app notification preference for a specific notification type
        """
        preference_map = {
            'application_status': self.application_status_in_app,
            'stage_change': self.stage_change_in_app,
            'repayment_upcoming': self.repayment_upcoming_in_app,
            'repayment_overdue': self.repayment_overdue_in_app,
            'note_reminder': self.note_reminder_in_app,
            'document_uploaded': self.document_uploaded_in_app,
            'signature_required': self.signature_required_in_app,
            'system': self.system_in_app,
            'active_loan_payment': self.active_loan_payment_in_app,
            'active_loan_expiry': self.active_loan_expiry_in_app,
            'active_loan_critical': self.active_loan_critical_in_app,
            'active_loan_manual': self.active_loan_manual_in_app,
        }
        return preference_map.get(notification_type, True)
    
    def get_email_preference(self, notification_type):
        """
        Get email notification preference for a specific notification type
        """
        preference_map = {
            'application_status': self.application_status_email,
            'stage_change': self.stage_change_email,
            'repayment_upcoming': self.repayment_upcoming_email,
            'repayment_overdue': self.repayment_overdue_email,
            'note_reminder': self.note_reminder_email,
            'document_uploaded': self.document_uploaded_email,
            'signature_required': self.signature_required_email,
            'system': self.system_email,
            'active_loan_payment': self.active_loan_payment_email,
            'active_loan_expiry': self.active_loan_expiry_email,
            'active_loan_critical': self.active_loan_critical_email,
            'active_loan_manual': self.active_loan_manual_email,
        }
        return preference_map.get(notification_type, False)
