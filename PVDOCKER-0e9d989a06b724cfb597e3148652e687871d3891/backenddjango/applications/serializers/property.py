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
            'id', 'property_type', 'description_if_applicable', 'occupancy',
            'address_unit', 'address_street_no', 'address_street_name', 
            'address_suburb', 'address_state', 'address_postcode', 
            'estimated_value', 'purchase_price', 'current_debt_position', 
            'first_mortgage_debt', 'second_mortgage_debt',
            'current_mortgagee', 'first_mortgage', 'second_mortgage', 
            'bedrooms', 'bathrooms', 'car_spaces', 'building_size', 'land_size',
            'is_single_story', 'has_garage', 'has_carport', 'has_off_street_parking'
        ]
        extra_kwargs = {
            # Make most fields optional and allow null/blank values for minimal data creation
            'property_type': {'required': False, 'allow_null': True, 'allow_blank': True},
            'description_if_applicable': {'required': False, 'allow_null': True, 'allow_blank': True},
            'occupancy': {'required': False, 'allow_null': True, 'allow_blank': True},
            'address_unit': {'required': False, 'allow_null': True, 'allow_blank': True},
            'address_street_no': {'required': False, 'allow_null': True, 'allow_blank': True},
            'address_street_name': {'required': False, 'allow_null': True, 'allow_blank': True},
            'address_suburb': {'required': False, 'allow_null': True, 'allow_blank': True},
            'address_state': {'required': False, 'allow_null': True, 'allow_blank': True},
            'address_postcode': {'required': False, 'allow_null': True, 'allow_blank': True},
            'estimated_value': {'required': False, 'allow_null': True},
            'purchase_price': {'required': False, 'allow_null': True},
            'current_debt_position': {'required': False, 'allow_null': True},
            'first_mortgage_debt': {'required': False, 'allow_null': True},
            'second_mortgage_debt': {'required': False, 'allow_null': True},
            'current_mortgagee': {'required': False, 'allow_null': True, 'allow_blank': True},
            'first_mortgage': {'required': False, 'allow_null': True},
            'second_mortgage': {'required': False, 'allow_null': True},
            'bedrooms': {'required': False, 'allow_null': True},
            'bathrooms': {'required': False, 'allow_null': True},
            'car_spaces': {'required': False, 'allow_null': True},
            'building_size': {'required': False, 'allow_null': True},
            'land_size': {'required': False, 'allow_null': True},
            'is_single_story': {'required': False, 'default': False},
            'has_garage': {'required': False, 'default': False},
            'has_carport': {'required': False, 'default': False},
            'has_off_street_parking': {'required': False, 'default': False},
        }
        
    def to_internal_value(self, data):
        """
        Transform incoming data to ensure numeric fields are properly converted.
        This handles the case where frontend sends string values that need to be integers.
        """
        # Create a copy of the data to avoid modifying the original
        data = dict(data)
        
        # Convert bedrooms, bathrooms, car_spaces from string to integer or null
        for field in ['bedrooms', 'bathrooms', 'car_spaces']:
            if field in data:
                value = data[field]
                if value == "" or value is None:
                    data[field] = None
                elif isinstance(value, str):
                    try:
                        data[field] = int(value) if value.strip() else None
                    except (ValueError, AttributeError):
                        # Let the parent validation handle the error
                        pass
        
        # Convert decimal fields from string to decimal or null
        for field in ['estimated_value', 'purchase_price', 'current_debt_position', 'first_mortgage_debt', 'second_mortgage_debt', 'first_mortgage', 'second_mortgage', 'building_size', 'land_size']:
            if field in data:
                value = data[field]
                if value == "" or value is None:
                    data[field] = None
                elif isinstance(value, str):
                    try:
                        data[field] = float(value) if value.strip() else None
                    except (ValueError, AttributeError):
                        # Let the parent validation handle the error
                        pass
        
        # Convert boolean fields from string to boolean or null
        for field in ['is_single_story', 'has_garage', 'has_carport', 'has_off_street_parking']:
            if field in data:
                value = data[field]
                if value == "" or value is None:
                    data[field] = None
                elif isinstance(value, str):
                    if value.lower() in ['true', '1', 'yes']:
                        data[field] = True
                    elif value.lower() in ['false', '0', 'no']:
                        data[field] = False
                    # Otherwise let parent validation handle it
        
        return super().to_internal_value(data)

    def validate(self, data):
        """
        Validate security property data
        """
        # Validate description_if_applicable when property_type is "other"
        if data.get('property_type') == 'other':
            if not data.get('description_if_applicable'):
                raise serializers.ValidationError({
                    'description_if_applicable': 'This field is required when property type is "other".'
                })
        
        return data


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