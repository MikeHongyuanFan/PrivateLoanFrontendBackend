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