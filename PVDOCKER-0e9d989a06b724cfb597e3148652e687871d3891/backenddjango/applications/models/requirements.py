"""
Loan requirement models for applications.

This module contains models for loan requirements and related
financial specifications that are part of loan applications.
"""

from django.db import models
from django.core.validators import MinValueValidator
from .base import BaseApplicationModel


class LoanRequirement(BaseApplicationModel):
    """
    Model for loan requirements within an application.
    
    Each application can have multiple loan requirements that specify
    different components or purposes for the requested loan amount.
    This allows for detailed breakdown of how loan funds will be used.
    """
    
    # ============================================================================
    # RELATIONSHIPS
    # ============================================================================
    
    application = models.ForeignKey(
        'applications.Application',
        on_delete=models.CASCADE,
        related_name='loan_requirements',
        help_text="The application this requirement belongs to"
    )
    
    # ============================================================================
    # REQUIREMENT DETAILS
    # ============================================================================
    
    description = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        help_text="Description of what this requirement covers"
    )
    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(0)],
        help_text="Amount required for this specific purpose"
    )
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = "Loan Requirement"
        verbose_name_plural = "Loan Requirements"
        indexes = [
            models.Index(fields=['application']),
        ]
    
    def __str__(self):
        """Return a readable representation of the loan requirement."""
        amount_str = f"${self.amount:,.2f}" if self.amount else "No amount"
        description = self.description or "Loan Requirement"
        return f"{description} - {amount_str}" 