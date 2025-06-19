"""
Property and Loan Requirement Serializers

This module contains serializers for security properties and loan requirements
related to loan applications.
"""

from rest_framework import serializers
from ..models import SecurityProperty, LoanRequirement


class SecurityPropertySerializer(serializers.ModelSerializer):
    """
    Serializer for security properties
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


class LoanRequirementSerializer(serializers.ModelSerializer):
    """
    Serializer for loan requirements
    """
    class Meta:
        model = LoanRequirement
        fields = ['id', 'description', 'amount'] 