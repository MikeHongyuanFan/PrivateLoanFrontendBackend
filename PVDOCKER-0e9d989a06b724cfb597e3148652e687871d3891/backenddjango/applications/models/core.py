"""
Core application models.

This module contains the main Application model that serves as the central
entity for loan applications. It maintains all existing functionality while
providing better organization and documentation.
"""

from django.db import models
from django.conf import settings
from django.utils.crypto import get_random_string
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models import JSONField
from .base import BaseApplicationModel


def generate_reference_number():
    """Generate a unique reference number for applications."""
    prefix = "APP"
    random_suffix = get_random_string(
        length=8, 
        allowed_chars='ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
    )
    return f"{prefix}-{random_suffix}"


class Application(BaseApplicationModel):
    """
    Model for loan applications.
    
    This is the central model that represents a complete loan application.
    It contains all the core information including borrower details, loan
    requirements, security information, and application workflow state.
    
    Key Features:
    - Stage-based workflow tracking
    - Comprehensive loan and borrower information
    - Security property relationships
    - Solvency enquiries compliance
    - Legacy field support for backward compatibility
    """
    
    # ============================================================================
    # STAGE AND APPLICATION TYPE CHOICES
    # ============================================================================
    
    STAGE_CHOICES = [
        ('inquiry', 'Inquiry'),
        ('sent_to_lender', 'Sent to Lender'),
        ('funding_table_issued', 'Funding Table Issued'),
        ('iloo_issued', 'ILOO Issued'),
        ('iloo_signed', 'ILOO Signed'),
        ('commitment_fee_paid', 'Commitment Fee Paid'),
        ('app_submitted', 'App Submitted'),
        ('valuation_ordered', 'Valuation Ordered'),
        ('valuation_received', 'Valuation Received'),
        ('more_info_required', 'More Info Required'),
        ('formal_approval', 'Formal Approval'),
        ('loan_docs_instructed', 'Loan Docs Instructed'),
        ('loan_docs_issued', 'Loan Docs Issued'),
        ('loan_docs_signed', 'Loan Docs Signed'),
        ('settlement_conditions', 'Settlement Conditions'),
        ('settled', 'Settled'),
        ('closed', 'Closed'),
        ('declined', 'Declined'),
        ('withdrawn', 'Withdrawn'),
    ]
    
    APPLICATION_TYPE_CHOICES = [
        ('acquisition', 'Acquisition'),
        ('refinance', 'Refinance'),
        ('equity_release', 'Equity Release'),
        ('refinance_equity_release', 'Refinance & Equity Release'),
        ('second_mortgage', '2nd Mortgage'),
        ('caveat', 'Caveat'),
        ('other', 'Other'),
    ]
    
    REPAYMENT_FREQUENCY_CHOICES = [
        ('weekly', 'Weekly'),
        ('fortnightly', 'Fortnightly'),
        ('monthly', 'Monthly'),
        ('quarterly', 'Quarterly'),
        ('annually', 'Annually'),
    ]
    
    LOAN_PURPOSE_CHOICES = [
        ('purchase', 'Purchase'),
        ('refinance', 'Refinance'),
        ('construction', 'Construction'),
        ('equity_release', 'Equity Release'),
        ('debt_consolidation', 'Debt Consolidation'),
        ('business_expansion', 'Business Expansion'),
        ('working_capital', 'Working Capital'),
        ('other', 'Other'),
    ]
    
    EXIT_STRATEGY_CHOICES = [
        ('sale', 'Sale of Property'),
        ('refinance', 'Refinance'),
        ('income', 'Income/Cash Flow'),
        ('other', 'Other'),
    ]
    
    # ============================================================================
    # BASIC APPLICATION DETAILS
    # ============================================================================
    
    reference_number = models.CharField(
        max_length=20,
        unique=True,
        default=generate_reference_number,
        help_text="Unique reference number for this application"
    )
    stage = models.CharField(
        max_length=25,
        choices=STAGE_CHOICES,
        default='inquiry',
        help_text="Current stage of the application"
    )
    stage_last_updated = models.DateTimeField(
        default=timezone.now,
        help_text="When the stage was last updated"
    )
    application_type = models.CharField(
        max_length=30,
        choices=APPLICATION_TYPE_CHOICES,
        null=True,
        blank=True,
        help_text="Type of loan application"
    )
    application_type_other = models.TextField(
        null=True,
        blank=True,
        help_text="Details for 'Other' application type"
    )
    purpose = models.TextField(
        null=True,
        blank=True,
        default='',
        help_text="General purpose of the application"
    )
    
    # ============================================================================
    # LOAN DETAILS
    # ============================================================================
    
    loan_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(0)],
        help_text="Requested loan amount"
    )
    loan_term = models.PositiveIntegerField(
        null=True,
        blank=True,
        help_text="Loan term in months"
    )
    capitalised_interest_term = models.PositiveIntegerField(
        null=True,
        blank=True,
        help_text="Capitalised interest term in months"
    )
    interest_rate = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        help_text="Interest rate as percentage"
    )
    repayment_frequency = models.CharField(
        max_length=20,
        choices=REPAYMENT_FREQUENCY_CHOICES,
        default='monthly',
        help_text="How often repayments are made"
    )
    product_id = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        help_text="Product identifier"
    )
    estimated_settlement_date = models.DateField(
        null=True,
        blank=True,
        help_text="Expected settlement date"
    )
    
    # ============================================================================
    # LOAN PURPOSE DETAILS
    # ============================================================================
    
    loan_purpose = models.CharField(
        max_length=50,
        choices=LOAN_PURPOSE_CHOICES,
        null=True,
        blank=True,
        help_text="Specific purpose of the loan"
    )
    additional_comments = models.TextField(
        null=True,
        blank=True,
        help_text="Additional comments about the loan"
    )
    prior_application = models.BooleanField(
        default=False,
        help_text="Whether there was a prior application"
    )
    prior_application_details = models.TextField(
        null=True,
        blank=True,
        help_text="Details about prior applications"
    )
    
    # ============================================================================
    # EXIT STRATEGY
    # ============================================================================
    
    exit_strategy = models.CharField(
        max_length=50,
        choices=EXIT_STRATEGY_CHOICES,
        null=True,
        blank=True,
        help_text="Planned exit strategy for the loan"
    )
    exit_strategy_details = models.TextField(
        null=True,
        blank=True,
        help_text="Additional details about exit strategy"
    )
    
    # ============================================================================
    # SOLVENCY ENQUIRIES
    # ============================================================================
    
    has_pending_litigation = models.BooleanField(
        null=True,
        blank=True,
        default=None,
        help_text="Do the Borrower(s) and Guarantor(s) have any pending or past litigation matters (within the last 2 years)?"
    )
    has_unsatisfied_judgements = models.BooleanField(
        null=True,
        blank=True,
        default=None,
        help_text="Are there any unsatisfied judgements against the Borrower(s) and Guarantor(s)?"
    )
    has_been_bankrupt = models.BooleanField(
        null=True,
        blank=True,
        default=None,
        help_text="Have the Borrower(s) and Guarantor(s) been bankrupt or insolvent in the past 5 years?"
    )
    has_been_refused_credit = models.BooleanField(
        null=True,
        blank=True,
        default=None,
        help_text="Has the Borrower(s) and Guarantor(s) been refused credit by a credit provider in the last 1 year?"
    )
    has_outstanding_ato_debt = models.BooleanField(
        null=True,
        blank=True,
        default=None,
        help_text="Are there any outstanding debts current or otherwise due to the ATO by the Borrower(s) and Guarantor(s)?"
    )
    has_outstanding_tax_returns = models.BooleanField(
        null=True,
        blank=True,
        default=None,
        help_text="Does the Borrower(s) and Guarantor(s) have outstanding Tax or BAS returns due to be lodged with the ATO?"
    )
    has_payment_arrangements = models.BooleanField(
        null=True,
        blank=True,
        default=None,
        help_text="Has the Borrower(s) and Guarantor(s) made payment arrangements with a creditor to payout debt that is still current?"
    )
    solvency_enquiries_details = models.TextField(
        null=True,
        blank=True,
        help_text="Additional details for any 'Yes' answers to solvency enquiries"
    )
    
    # ============================================================================
    # FUNDING CALCULATION
    # ============================================================================
    
    funding_result = JSONField(
        null=True,
        blank=True,
        help_text="Stores the current funding calculation result"
    )
    
    # ============================================================================
    # RELATIONSHIPS
    # ============================================================================
    
    broker = models.ForeignKey(
        'brokers.Broker',
        on_delete=models.SET_NULL,
        null=True,
        related_name='broker_applications',
        help_text="Broker handling this application"
    )
    branch = models.ForeignKey(
        'brokers.Branch',
        on_delete=models.SET_NULL,
        null=True,
        related_name='branch_applications',
        help_text="Branch associated with this application"
    )
    bd = models.ForeignKey(
        'brokers.BDM',
        on_delete=models.SET_NULL,
        null=True,
        related_name='bdm_applications',
        help_text="Business Development Manager for this application"
    )
    assigned_bd = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='assigned_applications',
        help_text="Assigned BD user for this application"
    )
    borrowers = models.ManyToManyField(
        'borrowers.Borrower',
        related_name='borrower_applications',
        blank=True,
        help_text="Borrowers associated with this application"
    )
    guarantors = models.ManyToManyField(
        'borrowers.Guarantor',
        related_name='guaranteed_applications',
        blank=True,
        help_text="Guarantors for this application"
    )
    
    # ============================================================================
    # PROFESSIONAL SERVICE CONTACTS
    # ============================================================================
    
    valuer = models.ForeignKey(
        'applications.Valuer',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='valuer_applications',
        help_text="Selected valuer for this application"
    )
    quantity_surveyor = models.ForeignKey(
        'applications.QuantitySurveyor',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='qs_applications',
        help_text="Selected quantity surveyor for this application"
    )
    
    # ============================================================================
    # SIGNATURE AND DOCUMENT INFO
    # ============================================================================
    
    signed_by = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        help_text="Name of person who signed the application"
    )
    signature_date = models.DateField(
        null=True,
        blank=True,
        help_text="Date the application was signed"
    )
    uploaded_pdf_path = models.FileField(
        upload_to='applications/signed_forms/',
        null=True,
        blank=True,
        help_text="Uploaded signed application form"
    )
    
    # ============================================================================
    # LEGACY VALUER INFORMATION (FLAT FIELDS)
    # ============================================================================
    
    valuer_company_name = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        help_text="[Legacy] Valuer company name"
    )
    valuer_contact_name = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        help_text="[Legacy] Valuer contact person name"
    )
    valuer_phone = models.CharField(
        max_length=20,
        null=True,
        blank=True,
        help_text="[Legacy] Valuer phone number"
    )
    valuer_email = models.EmailField(
        null=True,
        blank=True,
        help_text="[Legacy] Valuer email address"
    )
    valuation_date = models.DateField(
        null=True,
        blank=True,
        help_text="Date of property valuation"
    )
    valuation_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(0)],
        help_text="Valuation amount"
    )
    
    # ============================================================================
    # LEGACY QUANTITY SURVEYOR INFORMATION (FLAT FIELDS)
    # ============================================================================
    
    qs_company_name = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        help_text="[Legacy] QS company name"
    )
    qs_contact_name = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        help_text="[Legacy] QS contact person name"
    )
    qs_phone = models.CharField(
        max_length=20,
        null=True,
        blank=True,
        help_text="[Legacy] QS phone number"
    )
    qs_email = models.EmailField(
        null=True,
        blank=True,
        help_text="[Legacy] QS email address"
    )
    qs_report_date = models.DateField(
        null=True,
        blank=True,
        help_text="Date of QS report"
    )
    
    # ============================================================================
    # LEGACY SECURITY PROPERTY DETAILS (FLAT FIELDS)
    # ============================================================================
    
    security_address = models.TextField(
        null=True,
        blank=True,
        help_text="[Legacy] Security property address"
    )
    security_type = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        help_text="[Legacy] Security property type"
    )
    security_value = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(0)],
        help_text="[Legacy] Security property value"
    )
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = "Application"
        verbose_name_plural = "Applications"
        indexes = [
            models.Index(fields=['reference_number']),
            models.Index(fields=['stage']),
            models.Index(fields=['broker']),
            models.Index(fields=['bd']),
            models.Index(fields=['created_at']),
            models.Index(fields=['estimated_settlement_date']),
        ]
    
    def __str__(self):
        """Return a readable representation of the application."""
        return f"{self.reference_number} - {self.get_stage_display()}"
    
    def save(self, *args, **kwargs):
        """Override save to handle reference number generation and stage tracking."""
        # Generate reference number if not provided
        if not self.reference_number:
            self.reference_number = generate_reference_number()
        
        # Track stage changes
        if self.pk:
            try:
                old_instance = Application.objects.get(pk=self.pk)
                if old_instance.stage != self.stage:
                    self.stage_last_updated = timezone.now()
            except Application.DoesNotExist:
                pass
        
        super().save(*args, **kwargs)
    
    # ============================================================================
    # BUSINESS LOGIC PROPERTIES
    # ============================================================================
    
    @property
    def has_solvency_issues(self):
        """Check if any solvency issues are flagged."""
        solvency_fields = [
            'has_pending_litigation', 'has_unsatisfied_judgements', 'has_been_bankrupt',
            'has_been_refused_credit', 'has_outstanding_ato_debt', 'has_outstanding_tax_returns',
            'has_payment_arrangements'
        ]
        return any(getattr(self, field, False) for field in solvency_fields)
    
    @property
    def solvency_issues_count(self):
        """Count the number of solvency issues flagged."""
        solvency_fields = [
            'has_pending_litigation', 'has_unsatisfied_judgements', 'has_been_bankrupt',
            'has_been_refused_credit', 'has_outstanding_ato_debt', 'has_outstanding_tax_returns',
            'has_payment_arrangements'
        ]
        return sum(1 for field in solvency_fields if getattr(self, field, False))
    
    @property
    def total_security_value(self):
        """Calculate total value of all security properties."""
        return self.security_properties.aggregate(
            total=models.Sum('estimated_value')
        )['total'] or 0
    
    @property
    def loan_to_value_ratio(self):
        """Calculate loan-to-value ratio."""
        if self.loan_amount and self.total_security_value:
            return (self.loan_amount / self.total_security_value) * 100
        return 0
    
    def get_primary_borrower(self):
        """Get the first borrower (primary borrower)."""
        return self.borrowers.first()
    
    def get_primary_security_property(self):
        """Get the first security property."""
        return self.security_properties.first() 