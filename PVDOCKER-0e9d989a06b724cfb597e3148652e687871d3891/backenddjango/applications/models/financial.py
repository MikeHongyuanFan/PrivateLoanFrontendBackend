"""
Financial tracking models for loan applications.

This module contains models for financial aspects of loan applications:
- Fee tracking and management
- Repayment scheduling and recording
- Funding calculation history and auditing
"""

from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator
from django.db.models import JSONField
from .base import TimestampedModel, BaseApplicationModel


class Fee(TimestampedModel):
    """
    Model for application fees.
    
    Tracks various fees associated with loan applications including
    application fees, valuation fees, legal fees, etc.
    """
    
    # Fee type choices
    FEE_TYPE_CHOICES = [
        ('application', 'Application Fee'),
        ('valuation', 'Valuation Fee'),
        ('legal', 'Legal Fee'),
        ('broker', 'Broker Commission'),
        ('settlement', 'Settlement Fee'),
        ('other', 'Other Fee'),
    ]
    
    # Status choices
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('waived', 'Waived'),
        ('refunded', 'Refunded'),
    ]
    
    # ============================================================================
    # RELATIONSHIPS
    # ============================================================================
    
    application = models.ForeignKey(
        'applications.Application',
        on_delete=models.CASCADE,
        related_name='app_fees',
        null=True,
        blank=True,
        help_text="The application this fee belongs to"
    )
    
    # ============================================================================
    # FEE DETAILS
    # ============================================================================
    
    fee_type = models.CharField(
        max_length=20,
        choices=FEE_TYPE_CHOICES,
        default='other',
        help_text="Type of fee"
    )
    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(0)],
        help_text="Fee amount"
    )
    due_date = models.DateField(
        null=True,
        blank=True,
        help_text="When the fee is due"
    )
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='pending',
        help_text="Current status of the fee"
    )
    invoice = models.FileField(
        upload_to='invoices/',
        null=True,
        blank=True,
        help_text="Invoice document for this fee"
    )
    notes = models.TextField(
        null=True,
        blank=True,
        help_text="Additional notes about this fee"
    )
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = "Fee"
        verbose_name_plural = "Fees"
        indexes = [
            models.Index(fields=['application']),
            models.Index(fields=['fee_type']),
            models.Index(fields=['status']),
            models.Index(fields=['due_date']),
        ]
    
    def __str__(self):
        """Return a readable representation of the fee."""
        fee_type = self.get_fee_type_display()
        amount_str = f"${self.amount:,.2f}" if self.amount else "No amount"
        status = self.get_status_display()
        return f"{fee_type} - {amount_str} ({status})"


class Repayment(TimestampedModel):
    """
    Model for loan repayments.
    
    Tracks scheduled and actual repayments for loan applications,
    including payment dates, amounts, and status.
    """
    
    # Status choices
    STATUS_CHOICES = [
        ('scheduled', 'Scheduled'),
        ('paid', 'Paid'),
        ('missed', 'Missed'),
        ('partial', 'Partial Payment'),
    ]
    
    # ============================================================================
    # RELATIONSHIPS
    # ============================================================================
    
    application = models.ForeignKey(
        'applications.Application',
        on_delete=models.CASCADE,
        related_name='app_repayments',
        null=True,
        blank=True,
        help_text="The application this repayment belongs to"
    )
    
    # ============================================================================
    # REPAYMENT DETAILS
    # ============================================================================
    
    due_date = models.DateField(
        null=True,
        blank=True,
        help_text="When this repayment is due"
    )
    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(0)],
        help_text="Scheduled repayment amount"
    )
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='scheduled',
        help_text="Current status of this repayment"
    )
    paid_date = models.DateField(
        null=True,
        blank=True,
        help_text="When the repayment was actually paid"
    )
    payment_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(0)],
        help_text="Actual amount paid"
    )
    invoice = models.FileField(
        upload_to='repayment_invoices/',
        null=True,
        blank=True,
        help_text="Invoice or receipt for this repayment"
    )
    notes = models.TextField(
        null=True,
        blank=True,
        help_text="Additional notes about this repayment"
    )
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = "Repayment"
        verbose_name_plural = "Repayments"
        indexes = [
            models.Index(fields=['application']),
            models.Index(fields=['status']),
            models.Index(fields=['due_date']),
            models.Index(fields=['paid_date']),
        ]
    
    def __str__(self):
        """Return a readable representation of the repayment."""
        amount_str = f"${self.amount:,.2f}" if self.amount else "No amount"
        status = self.get_status_display()
        date_str = self.due_date.strftime('%Y-%m-%d') if self.due_date else "No date"
        return f"Repayment {amount_str} due {date_str} ({status})"
    
    @property
    def is_overdue(self):
        """Check if this repayment is overdue."""
        if not self.due_date or self.status in ['paid', 'partial']:
            return False
        from django.utils import timezone
        return timezone.now().date() > self.due_date
    
    @property
    def payment_variance(self):
        """Calculate difference between scheduled and actual payment."""
        if self.amount and self.payment_amount:
            return self.payment_amount - self.amount
        return None


class FundingCalculationHistory(BaseApplicationModel):
    """
    Model for storing funding calculation history.
    
    Provides audit trail and compliance tracking for funding calculations,
    storing both input parameters and calculated results.
    """
    
    # ============================================================================
    # RELATIONSHIPS
    # ============================================================================
    
    application = models.ForeignKey(
        'applications.Application',
        on_delete=models.CASCADE,
        related_name='funding_calculations',
        help_text="The application this calculation belongs to"
    )
    
    # ============================================================================
    # CALCULATION DATA
    # ============================================================================
    
    calculation_input = JSONField(
        help_text="Full set of manual input fields used during calculation"
    )
    calculation_result = JSONField(
        help_text="Computed funding breakdown (all fees, funds available)"
    )
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = "Funding Calculation History"
        verbose_name_plural = "Funding Calculation Histories"
        indexes = [
            models.Index(fields=['application']),
        ]
    
    def __str__(self):
        """Return a readable representation of the calculation."""
        date_str = self.created_at.strftime('%Y-%m-%d %H:%M') if self.created_at else "Unknown date"
        return f"Funding calculation for {self.application} at {date_str}"
    
    @property
    def total_fees(self):
        """Get total fees from calculation result."""
        try:
            return self.calculation_result.get('total_fees', 0)
        except (AttributeError, TypeError):
            return 0
    
    @property
    def funds_available(self):
        """Get available funds from calculation result."""
        try:
            return self.calculation_result.get('funds_available', 0)
        except (AttributeError, TypeError):
            return 0


class ActiveLoan(TimestampedModel):
    """
    Model for managing active loans that have been settled.
    
    This model tracks active loans and manages repayment schedules,
    interest payment tracking, and expiry alerts.
    """
    
    INTEREST_PAYMENT_FREQUENCY_CHOICES = [
        ('monthly', 'Monthly'),
        ('quarterly', 'Quarterly'),
        ('semi_annually', 'Semi-Annually'),
        ('annually', 'Annually'),
    ]
    
    # ============================================================================
    # RELATIONSHIPS
    # ============================================================================
    
    application = models.OneToOneField(
        'applications.Application',
        on_delete=models.CASCADE,
        related_name='active_loan',
        help_text="Application that has been settled and become an active loan"
    )
    
    # ============================================================================
    # LOAN DETAILS
    # ============================================================================
    
    settlement_date = models.DateField(
        help_text="Date when the loan was settled"
    )
    capitalised_interest_months = models.PositiveIntegerField(
        default=0,
        help_text="Number of months for capitalised interest"
    )
    interest_payments_required = models.BooleanField(
        default=False,
        help_text="Whether interest payments are required during the loan term"
    )
    interest_payment_frequency = models.CharField(
        max_length=20,
        choices=INTEREST_PAYMENT_FREQUENCY_CHOICES,
        null=True,
        blank=True,
        help_text="Frequency of interest payments (if required)"
    )
    interest_payment_due_dates = JSONField(
        default=list,
        help_text="List of dates when interest payments are due"
    )
    loan_expiry_date = models.DateField(
        help_text="Date when the loan expires"
    )
    is_active = models.BooleanField(
        default=True,
        help_text="Whether this loan is currently active"
    )
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = "Active Loan"
        verbose_name_plural = "Active Loans"
        indexes = [
            models.Index(fields=['application']),
            models.Index(fields=['settlement_date']),
            models.Index(fields=['loan_expiry_date']),
            models.Index(fields=['is_active']),
        ]
    
    def __str__(self):
        return f"Active Loan - {self.application.reference_number}"
    
    def save(self, *args, **kwargs):
        """
        Override save to ensure the application stage is 'settled'.
        """
        if self.application and self.application.stage != 'settled':
            self.application.stage = 'settled'
            self.application.save()
        super().save(*args, **kwargs)
    
    @property
    def days_until_expiry(self):
        """Calculate days until loan expiry."""
        from django.utils import timezone
        if self.loan_expiry_date:
            delta = self.loan_expiry_date - timezone.now().date()
            return delta.days
        return None
    
    @property
    def next_interest_payment_date(self):
        """Get the next interest payment due date."""
        from django.utils import timezone
        from datetime import datetime
        today = timezone.now().date()
        
        for date_str in self.interest_payment_due_dates:
            try:
                due_date = datetime.strptime(date_str, '%Y-%m-%d').date()
                if due_date >= today:
                    return due_date
            except (ValueError, TypeError):
                continue
        return None
    
    @property
    def days_until_next_payment(self):
        """Calculate days until next interest payment."""
        next_payment = self.next_interest_payment_date
        if next_payment:
            from django.utils import timezone
            delta = next_payment - timezone.now().date()
            return delta.days
        return None

    def get_next_payment_amount(self):
        """Get the amount for the next interest payment."""
        if not self.interest_payments_required:
            return 0
        
        # For now, return a default amount based on loan amount
        # In a real implementation, this would calculate based on interest rate and frequency
        if hasattr(self.application, 'loan_amount') and self.application.loan_amount:
            # Simple calculation: 1% of loan amount per month
            return float(self.application.loan_amount) * 0.01
        return 0


class ActiveLoanRepayment(TimestampedModel):
    """
    Model for tracking repayments against active loans.
    
    This model specifically tracks repayments for active loans,
    including interest payments and principal reductions.
    """
    
    REPAYMENT_TYPE_CHOICES = [
        ('interest', 'Interest Payment'),
        ('principal', 'Principal Payment'),
        ('principal_interest', 'Principal + Interest'),
        ('penalty', 'Penalty Payment'),
        ('early_settlement', 'Early Settlement'),
    ]
    
    # ============================================================================
    # RELATIONSHIPS
    # ============================================================================
    
    active_loan = models.ForeignKey(
        ActiveLoan,
        on_delete=models.CASCADE,
        related_name='repayments',
        help_text="Active loan this repayment is for"
    )
    
    # ============================================================================
    # REPAYMENT DETAILS
    # ============================================================================
    
    repayment_type = models.CharField(
        max_length=20,
        choices=REPAYMENT_TYPE_CHOICES,
        help_text="Type of repayment"
    )
    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        help_text="Repayment amount"
    )
    payment_date = models.DateField(
        help_text="Date the payment was made"
    )
    due_date = models.DateField(
        null=True,
        blank=True,
        help_text="Original due date for this payment"
    )
    reference_number = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        help_text="Bank reference or transaction number"
    )
    notes = models.TextField(
        null=True,
        blank=True,
        help_text="Additional notes about this repayment"
    )
    is_late = models.BooleanField(
        default=False,
        help_text="Whether this payment was made after the due date"
    )
    
    class Meta:
        ordering = ['-payment_date']
        verbose_name = "Active Loan Repayment"
        verbose_name_plural = "Active Loan Repayments"
        indexes = [
            models.Index(fields=['active_loan']),
            models.Index(fields=['payment_date']),
            models.Index(fields=['due_date']),
            models.Index(fields=['repayment_type']),
        ]
    
    def __str__(self):
        return f"${self.amount} - {self.payment_date} ({self.active_loan.application.reference_number})"
    
    def save(self, *args, **kwargs):
        """
        Override save to automatically determine if payment is late.
        """
        if self.due_date and self.payment_date > self.due_date:
            self.is_late = True
        super().save(*args, **kwargs) 