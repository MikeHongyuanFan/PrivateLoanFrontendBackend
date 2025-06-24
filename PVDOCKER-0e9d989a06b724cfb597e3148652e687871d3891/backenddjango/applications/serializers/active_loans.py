"""
Serializers for Active Loan management.

This module contains serializers for managing active loans, including
loan details, repayment schedules, and payment tracking.
"""

from rest_framework import serializers
from django.utils import timezone
from datetime import datetime, timedelta
from applications.models import ActiveLoan, ActiveLoanRepayment, Application


class ActiveLoanRepaymentSerializer(serializers.ModelSerializer):
    """
    Serializer for ActiveLoanRepayment model.
    
    Handles serialization of repayment data including validation
    and automatic calculation of late payment status.
    """
    
    days_late = serializers.SerializerMethodField()
    is_upcoming = serializers.SerializerMethodField()
    
    class Meta:
        model = ActiveLoanRepayment
        fields = [
            'id',
            'repayment_type',
            'amount',
            'payment_date',
            'due_date',
            'reference_number',
            'notes',
            'is_late',
            'days_late',
            'is_upcoming',
            'created_at',
            'updated_at'
        ]
        read_only_fields = ['is_late', 'created_at', 'updated_at']
    
    def get_days_late(self, obj):
        """Calculate how many days late the payment was."""
        if obj.due_date and obj.payment_date:
            delta = obj.payment_date - obj.due_date
            return delta.days if delta.days > 0 else 0
        return 0
    
    def get_is_upcoming(self, obj):
        """Check if this is an upcoming payment (within 14 days)."""
        if obj.due_date and not obj.payment_date:
            today = timezone.now().date()
            delta = obj.due_date - today
            return 0 <= delta.days <= 14
        return False


class ActiveLoanSerializer(serializers.ModelSerializer):
    """
    Serializer for ActiveLoan model.
    
    Handles active loan data including repayment schedules,
    interest payment tracking, and expiry management.
    """
    
    # Read-only computed fields
    days_until_expiry = serializers.ReadOnlyField()
    days_until_next_payment = serializers.ReadOnlyField()
    next_interest_payment_date = serializers.ReadOnlyField()
    
    # Application details
    application_reference = serializers.CharField(source='application.reference_number', read_only=True)
    application_stage = serializers.CharField(source='application.stage', read_only=True)
    
    # Related repayments
    repayments = ActiveLoanRepaymentSerializer(many=True, read_only=True)
    
    # Computed fields for UI display
    expiry_alert_level = serializers.SerializerMethodField()
    payment_alert_level = serializers.SerializerMethodField()
    total_payments_made = serializers.SerializerMethodField()
    upcoming_payments = serializers.SerializerMethodField()
    
    class Meta:
        model = ActiveLoan
        fields = [
            'id',
            'application',
            'application_reference',
            'application_stage',
            'settlement_date',
            'capitalised_interest_months',
            'interest_payments_required',
            'interest_payment_frequency',
            'interest_payment_due_dates',
            'loan_expiry_date',
            'is_active',
            'days_until_expiry',
            'days_until_next_payment',
            'next_interest_payment_date',
            'expiry_alert_level',
            'payment_alert_level',
            'total_payments_made',
            'upcoming_payments',
            'repayments',
            'created_at',
            'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']
    
    def get_expiry_alert_level(self, obj):
        """Determine alert level for loan expiry."""
        days_until_expiry = obj.days_until_expiry
        if days_until_expiry is None:
            return 'none'
        elif days_until_expiry <= 7:
            return 'critical'
        elif days_until_expiry <= 30:
            return 'warning'
        elif days_until_expiry <= 60:
            return 'info'
        return 'none'
    
    def get_payment_alert_level(self, obj):
        """Determine alert level for next interest payment."""
        if not obj.interest_payments_required:
            return 'none'
        
        days_until_payment = obj.days_until_next_payment
        if days_until_payment is None:
            return 'none'
        elif days_until_payment <= 3:
            return 'critical'
        elif days_until_payment <= 14:
            return 'warning'
        elif days_until_payment <= 30:
            return 'info'
        return 'none'
    
    def get_total_payments_made(self, obj):
        """Calculate total amount of payments made."""
        return sum(repayment.amount for repayment in obj.repayments.all())
    
    def get_upcoming_payments(self, obj):
        """Get list of upcoming payment dates."""
        if not obj.interest_payments_required:
            return []
        
        today = timezone.now().date()
        upcoming = []
        
        for date_str in obj.interest_payment_due_dates:
            try:
                due_date = datetime.strptime(date_str, '%Y-%m-%d').date()
                if due_date >= today:
                    days_until = (due_date - today).days
                    upcoming.append({
                        'due_date': due_date.strftime('%Y-%m-%d'),
                        'days_until': days_until,
                        'alert_level': 'critical' if days_until <= 3 else 'warning' if days_until <= 14 else 'info'
                    })
            except (ValueError, TypeError):
                continue
        
        return sorted(upcoming, key=lambda x: x['due_date'])[:5]  # Return next 5 payments
    
    def validate_interest_payment_due_dates(self, value):
        """Validate that interest payment dates are in correct format."""
        if not isinstance(value, list):
            raise serializers.ValidationError("Interest payment due dates must be a list.")
        
        validated_dates = []
        for date_str in value:
            try:
                # Validate date format
                parsed_date = datetime.strptime(date_str, '%Y-%m-%d')
                validated_dates.append(date_str)
            except (ValueError, TypeError):
                raise serializers.ValidationError(f"Invalid date format: {date_str}. Use YYYY-MM-DD format.")
        
        return validated_dates
    
    def validate(self, attrs):
        """Cross-field validation for active loan data."""
        # Validate that loan expiry date is after settlement date
        settlement_date = attrs.get('settlement_date')
        loan_expiry_date = attrs.get('loan_expiry_date')
        
        if settlement_date and loan_expiry_date and loan_expiry_date <= settlement_date:
            raise serializers.ValidationError({
                'loan_expiry_date': 'Loan expiry date must be after settlement date.'
            })
        
        # Validate interest payment requirements
        interest_payments_required = attrs.get('interest_payments_required', False)
        interest_payment_frequency = attrs.get('interest_payment_frequency')
        interest_payment_due_dates = attrs.get('interest_payment_due_dates', [])
        
        if interest_payments_required:
            if not interest_payment_frequency:
                raise serializers.ValidationError({
                    'interest_payment_frequency': 'Payment frequency is required when interest payments are required.'
                })
            
            if not interest_payment_due_dates:
                raise serializers.ValidationError({
                    'interest_payment_due_dates': 'Payment due dates are required when interest payments are required.'
                })
        
        return attrs


class ActiveLoanCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating new ActiveLoan instances.
    
    Includes additional validation and automatic field population
    for new active loans.
    """
    
    application = serializers.PrimaryKeyRelatedField(queryset=Application.objects.all())
    
    class Meta:
        model = ActiveLoan
        fields = [
            'application',
            'settlement_date',
            'capitalised_interest_months',
            'interest_payments_required',
            'interest_payment_frequency',
            'interest_payment_due_dates',
            'loan_expiry_date'
        ]
    
    def validate_application(self, value):
        """Validate that the application can be converted to an active loan."""
        if value.stage != 'settled':
            raise serializers.ValidationError(
                "Only applications with 'settled' status can be converted to active loans."
            )
        
        # Check if an active loan already exists for this application
        if ActiveLoan.objects.filter(application=value).exists():
            raise serializers.ValidationError(
                "This application already has an active loan associated with it."
            )
        
        return value
    
    def create(self, validated_data):
        """Create an active loan and update application stage if needed."""
        active_loan = super().create(validated_data)
        
        # Ensure application stage is set to 'settled'
        if active_loan.application.stage != 'settled':
            active_loan.application.stage = 'settled'
            active_loan.application.save()
        
        return active_loan


class ActiveLoanSummarySerializer(serializers.ModelSerializer):
    """
    Lightweight serializer for active loan summaries and listings.
    
    Used for dashboard views and lists where full detail is not needed.
    """
    
    application_reference = serializers.CharField(source='application.reference_number', read_only=True)
    borrower_name = serializers.SerializerMethodField()
    loan_amount = serializers.DecimalField(source='application.loan_amount', max_digits=12, decimal_places=2, read_only=True)
    days_until_expiry = serializers.ReadOnlyField()
    days_until_next_payment = serializers.ReadOnlyField()
    alert_status = serializers.SerializerMethodField()
    
    class Meta:
        model = ActiveLoan
        fields = [
            'id',
            'application_reference',
            'borrower_name',
            'loan_amount',
            'settlement_date',
            'loan_expiry_date',
            'days_until_expiry',
            'days_until_next_payment',
            'interest_payments_required',
            'alert_status',
            'is_active'
        ]
    
    def get_borrower_name(self, obj):
        """Get the primary borrower name for display."""
        if obj.application.borrowers.exists():
            primary_borrower = obj.application.borrowers.first()
            return f"{primary_borrower.first_name} {primary_borrower.last_name}"
        elif obj.application.company_borrowers.exists():
            primary_company = obj.application.company_borrowers.first()
            return primary_company.company_name
        return "Unknown Borrower"
    
    def get_alert_status(self, obj):
        """Get overall alert status for this loan."""
        expiry_days = obj.days_until_expiry
        payment_days = obj.days_until_next_payment if obj.interest_payments_required else None
        
        # Critical alerts (red)
        if (expiry_days is not None and expiry_days <= 7) or \
           (payment_days is not None and payment_days <= 3):
            return 'critical'
        
        # Warning alerts (yellow)
        if (expiry_days is not None and expiry_days <= 30) or \
           (payment_days is not None and payment_days <= 14):
            return 'warning'
        
        # Info alerts (blue)
        if (expiry_days is not None and expiry_days <= 60) or \
           (payment_days is not None and payment_days <= 30):
            return 'info'
        
        return 'none' 