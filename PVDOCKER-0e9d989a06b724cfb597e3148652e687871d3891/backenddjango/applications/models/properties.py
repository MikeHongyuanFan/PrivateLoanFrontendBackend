"""
Property-related models for loan applications.

This module contains models for security properties and related
property information used in loan applications.
"""

from django.db import models
from django.core.validators import MinValueValidator
from .base import BaseApplicationModel


class SecurityProperty(BaseApplicationModel):
    """
    Model for security properties used as collateral for loans.
    
    Each application can have multiple security properties that serve
    as collateral for the loan. This model captures detailed property
    information including address, type, valuation, and mortgage details.
    """
    
    # Property type choices
    PROPERTY_TYPE_CHOICES = [
        ('residential', 'Residential'),
        ('commercial', 'Commercial'),
        ('industrial', 'Industrial'),
        ('retail', 'Retail'),
        ('land', 'Land'),
        ('rural', 'Rural'),
        ('other', 'Other'),
    ]
    
    # Occupancy choices
    OCCUPANCY_CHOICES = [
        ('owner_occupied', 'Owner Occupied'),
        ('investment', 'Investment Property'),
    ]
    
    # ============================================================================
    # RELATIONSHIPS
    # ============================================================================
    
    application = models.ForeignKey(
        'applications.Application',
        on_delete=models.CASCADE,
        related_name='security_properties',
        help_text="The application this property secures"
    )
    
    # ============================================================================
    # PROPERTY ADDRESS
    # ============================================================================
    
    address_unit = models.CharField(
        max_length=20,
        null=True,
        blank=True,
        help_text="Unit/apartment number"
    )
    address_street_no = models.CharField(
        max_length=20,
        null=True,
        blank=True,
        help_text="Street number"
    )
    address_street_name = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        help_text="Street name"
    )
    address_suburb = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        help_text="Suburb/city"
    )
    address_state = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        help_text="State/territory"
    )
    address_postcode = models.CharField(
        max_length=10,
        null=True,
        blank=True,
        help_text="Postal code"
    )
    
    # ============================================================================
    # MORTGAGE DETAILS
    # ============================================================================
    
    current_mortgagee = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        help_text="Current mortgage holder"
    )
    first_mortgage = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        help_text="First mortgage details"
    )
    second_mortgage = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        help_text="Second mortgage details"
    )
    current_debt_position = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(0)],
        help_text="Current outstanding debt amount"
    )
    
    # ============================================================================
    # PROPERTY TYPE AND CLASSIFICATION
    # ============================================================================
    
    property_type = models.CharField(
        max_length=20,
        choices=PROPERTY_TYPE_CHOICES,
        null=True,
        blank=True,
        help_text="Type of property"
    )
    occupancy = models.CharField(
        max_length=20,
        choices=OCCUPANCY_CHOICES,
        null=True,
        blank=True,
        help_text="How the property is occupied"
    )
    
    # ============================================================================
    # PROPERTY DESCRIPTION
    # ============================================================================
    
    bedrooms = models.PositiveIntegerField(
        null=True,
        blank=True,
        help_text="Number of bedrooms"
    )
    bathrooms = models.PositiveIntegerField(
        null=True,
        blank=True,
        help_text="Number of bathrooms"
    )
    car_spaces = models.PositiveIntegerField(
        null=True,
        blank=True,
        help_text="Number of car spaces"
    )
    building_size = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(0)],
        help_text="Building size in square meters"
    )
    land_size = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(0)],
        help_text="Land size in square meters"
    )
    
    # ============================================================================
    # PROPERTY STRUCTURE
    # ============================================================================
    
    is_single_story = models.BooleanField(
        default=True,
        help_text="Whether the property is single story"
    )
    has_garage = models.BooleanField(
        default=False,
        help_text="Whether the property has a garage"
    )
    has_carport = models.BooleanField(
        default=False,
        help_text="Whether the property has a carport"
    )
    has_off_street_parking = models.BooleanField(
        default=False,
        help_text="Whether the property has off-street parking"
    )
    
    # ============================================================================
    # VALUATION
    # ============================================================================
    
    estimated_value = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(0)],
        help_text="Estimated property value"
    )
    purchase_price = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(0)],
        help_text="Property purchase price"
    )
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = "Security Property"
        verbose_name_plural = "Security Properties"
        indexes = [
            models.Index(fields=['application']),
            models.Index(fields=['property_type']),
            models.Index(fields=['address_suburb', 'address_state']),
        ]
    
    def __str__(self):
        """Return a readable representation of the property."""
        address_parts = [
            self.address_unit,
            self.address_street_no,
            self.address_street_name,
            self.address_suburb,
            self.address_state,
            self.address_postcode
        ]
        address = " ".join(filter(None, address_parts))
        return address if address.strip() else f"Property #{self.id}"
    
    @property
    def full_address(self):
        """Get the complete formatted address."""
        return str(self)
    
    @property
    def net_equity(self):
        """Calculate net equity (estimated value - current debt)."""
        if self.estimated_value and self.current_debt_position:
            return self.estimated_value - self.current_debt_position
        return self.estimated_value or 0 