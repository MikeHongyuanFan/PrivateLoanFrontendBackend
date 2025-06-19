"""
Property and Loan Requirement Serializers

This module contains serializers for security properties and loan requirements
related to loan applications.
"""

from rest_framework import serializers
from ..models import SecurityProperty, LoanRequirement


class SecurityPropertySerializer(serializers.ModelSerializer):
    """
    Serializer for security properties with null/blank handling for minimal data creation
    """
    class Meta:
        model = SecurityProperty
        fields = [
            'id', 'property_type', 'address_unit', 'address_street_no', 'address_street_name', 
            'address_suburb', 'address_state', 'address_postcode', 'estimated_value',
            'purchase_price', 'current_debt_position', 'current_mortgagee',
            'first_mortgage', 'second_mortgage', 'bedrooms', 'bathrooms', 'car_spaces', 'building_size',
            'land_size'
        ]
        extra_kwargs = {
            # Make most fields optional and allow null/blank values for minimal data creation
            'property_type': {'required': False, 'allow_null': True, 'allow_blank': True},
            'address_unit': {'required': False, 'allow_null': True, 'allow_blank': True},
            'address_street_no': {'required': False, 'allow_null': True, 'allow_blank': True},
            'address_street_name': {'required': False, 'allow_null': True, 'allow_blank': True},
            'address_suburb': {'required': False, 'allow_null': True, 'allow_blank': True},
            'address_state': {'required': False, 'allow_null': True, 'allow_blank': True},
            'address_postcode': {'required': False, 'allow_null': True, 'allow_blank': True},
            'estimated_value': {'required': False, 'allow_null': True},
            'purchase_price': {'required': False, 'allow_null': True},
            'current_debt_position': {'required': False, 'allow_null': True},
            'current_mortgagee': {'required': False, 'allow_null': True, 'allow_blank': True},
            'first_mortgage': {'required': False, 'allow_null': True},
            'second_mortgage': {'required': False, 'allow_null': True},
            'bedrooms': {'required': False, 'allow_null': True},
            'bathrooms': {'required': False, 'allow_null': True},
            'car_spaces': {'required': False, 'allow_null': True},
            'building_size': {'required': False, 'allow_null': True},
            'land_size': {'required': False, 'allow_null': True},
        }


class LoanRequirementSerializer(serializers.ModelSerializer):
    """
    Serializer for loan requirements with null/blank handling for minimal data creation
    """
    class Meta:
        model = LoanRequirement
        fields = ['id', 'description', 'amount']
        extra_kwargs = {
            # Make most fields optional and allow null/blank values for minimal data creation
            'description': {'required': False, 'allow_null': True, 'allow_blank': True},
            'amount': {'required': False, 'allow_null': True},
        } 