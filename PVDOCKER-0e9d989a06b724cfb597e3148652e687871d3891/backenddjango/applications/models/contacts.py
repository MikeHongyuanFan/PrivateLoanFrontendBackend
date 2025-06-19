"""
Contact models for professional services related to loan applications.

This module contains models for external contacts and service providers:
- Valuer: Property valuation contacts
- QuantitySurveyor: Construction assessment contacts

These models provide reusable contact information that can be
associated with applications.
"""

from django.db import models
from django.core.validators import EmailValidator
from .base import BaseApplicationModel


class ProfessionalContact(BaseApplicationModel):
    """
    Abstract base model for professional service contacts.
    
    Provides common fields for external service providers like
    valuers, quantity surveyors, etc.
    """
    company_name = models.CharField(
        max_length=255,
        help_text="Name of the company/firm"
    )
    contact_name = models.CharField(
        max_length=255,
        help_text="Name of the primary contact person"
    )
    phone = models.CharField(
        max_length=20,
        help_text="Primary contact phone number"
    )
    email = models.EmailField(
        validators=[EmailValidator()],
        help_text="Primary contact email address"
    )
    address = models.TextField(
        null=True,
        blank=True,
        help_text="Business address"
    )
    notes = models.TextField(
        null=True,
        blank=True,
        help_text="Additional notes about this contact"
    )
    is_active = models.BooleanField(
        default=True,
        help_text="Whether this contact is currently active"
    )
    
    class Meta:
        abstract = True
        ordering = ['company_name', 'contact_name']
    
    def __str__(self):
        return f"{self.company_name} - {self.contact_name}"


class Valuer(ProfessionalContact):
    """
    Model for property valuation contacts.
    
    Stores reusable valuer information that can be selected
    for property valuations across multiple applications.
    
    Fields inherited from ProfessionalContact:
    - company_name, contact_name, phone, email
    - address, notes, is_active
    - created_by, created_at, updated_at
    """
    
    class Meta:
        ordering = ['company_name', 'contact_name']
        verbose_name = "Valuer"
        verbose_name_plural = "Valuers"
        indexes = [
            models.Index(fields=['company_name']),
            models.Index(fields=['is_active']),
        ]
    
    def get_application_count(self):
        """Get the number of applications using this valuer."""
        return self.valuer_applications.count()


class QuantitySurveyor(ProfessionalContact):
    """
    Model for quantity surveyor contacts.
    
    Stores reusable quantity surveyor information that can be
    selected for construction assessments across multiple applications.
    
    Fields inherited from ProfessionalContact:
    - company_name, contact_name, phone, email
    - address, notes, is_active
    - created_by, created_at, updated_at
    """
    
    class Meta:
        ordering = ['company_name', 'contact_name']
        verbose_name = "Quantity Surveyor"
        verbose_name_plural = "Quantity Surveyors"
        indexes = [
            models.Index(fields=['company_name']),
            models.Index(fields=['is_active']),
        ]
    
    def get_application_count(self):
        """Get the number of applications using this quantity surveyor."""
        return self.qs_applications.count() 