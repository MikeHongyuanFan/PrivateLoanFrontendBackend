from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.http import HttpResponse
from django.urls import path
from django.utils.html import format_html
from .models import User, Notification, NotificationPreference, EmailLog
from crm_backend.tasks import export_email_logs_to_docx

class CustomUserAdmin(UserAdmin):
    list_display = ('email', 'first_name', 'last_name', 'role', 'is_staff', 'is_active', 'date_joined')
    list_filter = ('role', 'is_staff', 'is_active', 'date_joined')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'phone')}),
        ('Permissions', {'fields': ('role', 'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'role', 'first_name', 'last_name', 'is_staff', 'is_active'),
        }),
    )
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)
    readonly_fields = ('date_joined', 'last_login')

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('title', 'notification_type', 'user', 'is_read', 'created_at', 'read_at')
    list_filter = ('notification_type', 'is_read', 'created_at')
    search_fields = ('title', 'message', 'user__email')
    raw_id_fields = ('user',)
    readonly_fields = ('created_at', 'read_at')
    fieldsets = (
        ('Notification Information', {
            'fields': ('title', 'message', 'notification_type', 'is_read')
        }),
        ('Related Object', {
            'fields': ('related_object_id', 'related_object_type')
        }),
        ('User Information', {
            'fields': ('user',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'read_at')
        }),
    )
    actions = ['mark_as_read', 'mark_as_unread']
    
    def mark_as_read(self, request, queryset):
        for notification in queryset:
            notification.mark_as_read()
        self.message_user(request, f"{queryset.count()} notifications marked as read.")
    mark_as_read.short_description = "Mark selected notifications as read"
    
    def mark_as_unread(self, request, queryset):
        queryset.update(is_read=False, read_at=None)
        self.message_user(request, f"{queryset.count()} notifications marked as unread.")
    mark_as_unread.short_description = "Mark selected notifications as unread"

@admin.register(NotificationPreference)
class NotificationPreferenceAdmin(admin.ModelAdmin):
    list_display = ('user', 'daily_digest', 'weekly_digest', 'updated_at')
    list_filter = ('daily_digest', 'weekly_digest', 'application_status_in_app', 'application_status_email')
    search_fields = ('user__email',)
    raw_id_fields = ('user',)
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('User', {
            'fields': ('user',)
        }),
        ('In-App Notifications', {
            'fields': (
                'application_status_in_app', 'repayment_upcoming_in_app', 'repayment_overdue_in_app',
                'note_reminder_in_app', 'document_uploaded_in_app', 'signature_required_in_app', 'system_in_app'
            )
        }),
        ('Email Notifications', {
            'fields': (
                'application_status_email', 'repayment_upcoming_email', 'repayment_overdue_email',
                'note_reminder_email', 'document_uploaded_email', 'signature_required_email', 'system_email'
            )
        }),
        ('Digest Settings', {
            'fields': ('daily_digest', 'weekly_digest')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )

@admin.register(EmailLog)
class EmailLogAdmin(admin.ModelAdmin):
    list_display = ('subject', 'user_email', 'email_type', 'status', 'sent_at')
    list_filter = ('status', 'email_type', 'sent_at')
    search_fields = ('subject', 'user__email', 'message_body')
    raw_id_fields = ('user', 'notification')
    readonly_fields = ('sent_at',)
    fieldsets = (
        ('Email Information', {
            'fields': ('subject', 'message_body', 'email_type', 'status')
        }),
        ('Related Information', {
            'fields': ('user', 'notification')
        }),
        ('Timestamps', {
            'fields': ('sent_at',)
        }),
    )
    actions = ['export_to_docx']
    
    def user_email(self, obj):
        return obj.user.email
    user_email.short_description = 'Recipient'
    
    def export_to_docx(self, request, queryset):
        log_ids = list(queryset.values_list('id', flat=True))
        if not log_ids:
            self.message_user(request, "No email logs selected for export.")
            return
            
        # Use the task to generate the DOCX file
        output = export_email_logs_to_docx(log_ids)
        
        # Create response with the DOCX file
        response = HttpResponse(
            output.getvalue(),
            content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document'
        )
        response['Content-Disposition'] = 'attachment; filename="email_logs_export.docx"'
        return response
    export_to_docx.short_description = "Export selected logs to DOCX"
    
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                'export-docx/',
                self.admin_site.admin_view(self.export_docx_view),
                name='users_emaillog_export_docx',
            ),
        ]
        return custom_urls + urls
    
    def export_docx_view(self, request):
        # Get selected IDs from request
        log_ids = request.GET.getlist('ids')
        if not log_ids:
            self.message_user(request, "No email logs selected for export.")
            return HttpResponse("No logs selected", status=400)
            
        # Convert string IDs to integers
        log_ids = [int(log_id) for log_id in log_ids]
        
        # Use the task to generate the DOCX file
        output = export_email_logs_to_docx(log_ids)
        
        # Create response with the DOCX file
        response = HttpResponse(
            output.getvalue(),
            content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document'
        )
        response['Content-Disposition'] = 'attachment; filename="email_logs_export.docx"'
        return response

admin.site.register(User, CustomUserAdmin)
