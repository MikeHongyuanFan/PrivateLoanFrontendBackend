"""
Property Validation Functions

This module contains validators for security property data including
address validation, property type validation, and financial value validation.
"""

from django.core.exceptions import ValidationError
from decimal import Decimal, InvalidOperation
import re


def validate_security_property(property_data):
    """
    Validate security property information
    
    Args:
        property_data: Dictionary containing property data
        
    Returns:
        Dictionary of field errors (empty if valid)
    """
    errors = {}
    
    # Validate address information
    errors.update(_validate_property_address(property_data))
    
    # Validate property type and classification
    errors.update(_validate_property_type(property_data))
    
    # Validate financial values
    errors.update(_validate_property_values(property_data))
    
    # Validate property description
    errors.update(_validate_property_description(property_data))
    
    # Validate mortgage details
    errors.update(_validate_mortgage_details(property_data))
    
    return errors


def _validate_property_address(property_data):
    """Validate property address fields"""
    errors = {}
    
    # Address components validation
    street_name = property_data.get('address_street_name', '').strip()
    suburb = property_data.get('address_suburb', '').strip()
    state = property_data.get('address_state', '').strip()
    postcode = property_data.get('address_postcode', '').strip()
    
    # If any address field is provided, validate the complete address
    address_fields = [street_name, suburb, state, postcode]
    if any(address_fields):
        # Basic address validation - street name and suburb are most important
        if not street_name:
            errors['address_street_name'] = 'Street name is required when providing address'
        if not suburb:
            errors['address_suburb'] = 'Suburb is required when providing address'
        if not state:
            errors['address_state'] = 'State is required when providing address'
        if not postcode:
            errors['address_postcode'] = 'Postcode is required when providing address'
    
    # Australian state validation
    if state:
        valid_states = ['NSW', 'VIC', 'QLD', 'SA', 'WA', 'TAS', 'NT', 'ACT', 
                       'nsw', 'vic', 'qld', 'sa', 'wa', 'tas', 'nt', 'act']
        if state not in valid_states:
            errors['address_state'] = 'Please provide a valid Australian state/territory'
    
    # Australian postcode validation
    if postcode:
        if not re.match(r'^\d{4}$', str(postcode)):
            errors['address_postcode'] = 'Australian postcode must be 4 digits'
        else:
            # State-specific postcode validation
            postcode_int = int(postcode)
            state_upper = state.upper() if state else ''
            
            # Basic postcode range validation for major states
            postcode_ranges = {
                'NSW': [(1000, 2999), (2000, 2999)],
                'ACT': [(200, 299), (2600, 2699)],
                'VIC': [(3000, 3999), (8000, 8999)],
                'QLD': [(4000, 4999), (9000, 9999)],
                'SA': [(5000, 5999)],
                'WA': [(6000, 6999)],
                'TAS': [(7000, 7999)],
                'NT': [(800, 899)]
            }
            
            if state_upper in postcode_ranges:
                valid_range = False
                for start, end in postcode_ranges[state_upper]:
                    if start <= postcode_int <= end:
                        valid_range = True
                        break
                if not valid_range:
                    errors['address_postcode'] = f'Postcode {postcode} is not valid for {state_upper}'
    
    # Street number validation
    street_no = property_data.get('address_street_no', '').strip()
    if street_no and not re.match(r'^[\d\-/A-Za-z\s]+$', street_no):
        errors['address_street_no'] = 'Street number contains invalid characters'
    
    # Unit validation
    unit = property_data.get('address_unit', '').strip()
    if unit and not re.match(r'^[\d\-/A-Za-z\s]+$', unit):
        errors['address_unit'] = 'Unit number contains invalid characters'
    
    return errors


def _validate_property_type(property_data):
    """Validate property type and classification"""
    errors = {}
    
    # Property type validation
    property_type = property_data.get('property_type')
    if property_type:
        valid_types = ['residential', 'commercial', 'industrial', 'retail', 'land', 'rural', 'other']
        if property_type not in valid_types:
            errors['property_type'] = f'Invalid property type. Must be one of: {", ".join(valid_types)}'
    
    # Occupancy validation
    occupancy = property_data.get('occupancy')
    if occupancy:
        valid_occupancy = ['owner_occupied', 'investment']
        if occupancy not in valid_occupancy:
            errors['occupancy'] = f'Invalid occupancy type. Must be one of: {", ".join(valid_occupancy)}'
    
    return errors


def _validate_property_values(property_data):
    """Validate financial property values"""
    errors = {}
    
    # Validate estimated value
    estimated_value = property_data.get('estimated_value')
    if estimated_value is not None:
        try:
            value = Decimal(str(estimated_value))
            if value <= 0:
                errors['estimated_value'] = 'Estimated value must be greater than 0'
            elif value > Decimal('100000000'):  # $100M limit
                errors['estimated_value'] = 'Estimated value cannot exceed $100,000,000'
        except (ValueError, TypeError, InvalidOperation):
            errors['estimated_value'] = 'Estimated value must be a valid number'
    
    # Validate purchase price
    purchase_price = property_data.get('purchase_price')
    if purchase_price is not None:
        try:
            price = Decimal(str(purchase_price))
            if price <= 0:
                errors['purchase_price'] = 'Purchase price must be greater than 0'
            elif price > Decimal('100000000'):  # $100M limit
                errors['purchase_price'] = 'Purchase price cannot exceed $100,000,000'
        except (ValueError, TypeError, InvalidOperation):
            errors['purchase_price'] = 'Purchase price must be a valid number'
    
    # Validate current debt position
    current_debt = property_data.get('current_debt_position')
    if current_debt is not None:
        try:
            debt = Decimal(str(current_debt))
            if debt < 0:
                errors['current_debt_position'] = 'Current debt cannot be negative'
            elif debt > Decimal('100000000'):  # $100M limit
                errors['current_debt_position'] = 'Current debt cannot exceed $100,000,000'
        except (ValueError, TypeError, InvalidOperation):
            errors['current_debt_position'] = 'Current debt must be a valid number'
    
    # Cross-validation: debt should not exceed property value
    if (estimated_value is not None and current_debt is not None and 
        estimated_value > 0 and current_debt > 0):
        try:
            value = Decimal(str(estimated_value))
            debt = Decimal(str(current_debt))
            if debt > value:
                errors['current_debt_position'] = 'Current debt cannot exceed estimated property value'
        except (ValueError, TypeError, InvalidOperation):
            pass  # Already caught above
    
    # Validate building and land sizes
    building_size = property_data.get('building_size')
    if building_size is not None:
        try:
            size = Decimal(str(building_size))
            if size <= 0:
                errors['building_size'] = 'Building size must be greater than 0'
            elif size > 10000:  # 10,000 sqm limit
                errors['building_size'] = 'Building size cannot exceed 10,000 square meters'
        except (ValueError, TypeError, InvalidOperation):
            errors['building_size'] = 'Building size must be a valid number'
    
    land_size = property_data.get('land_size')
    if land_size is not None:
        try:
            size = Decimal(str(land_size))
            if size <= 0:
                errors['land_size'] = 'Land size must be greater than 0'
            elif size > 1000000:  # 1,000,000 sqm limit (100 hectares)
                errors['land_size'] = 'Land size cannot exceed 1,000,000 square meters'
        except (ValueError, TypeError, InvalidOperation):
            errors['land_size'] = 'Land size must be a valid number'
    
    return errors


def _validate_property_description(property_data):
    """Validate property description fields"""
    errors = {}
    
    # Validate bedrooms
    bedrooms = property_data.get('bedrooms')
    if bedrooms is not None:
        try:
            bed_count = int(bedrooms)
            if bed_count < 0:
                errors['bedrooms'] = 'Number of bedrooms cannot be negative'
            elif bed_count > 50:  # Reasonable upper limit
                errors['bedrooms'] = 'Number of bedrooms cannot exceed 50'
        except (ValueError, TypeError):
            errors['bedrooms'] = 'Number of bedrooms must be a whole number'
    
    # Validate bathrooms
    bathrooms = property_data.get('bathrooms')
    if bathrooms is not None:
        try:
            bath_count = int(bathrooms)
            if bath_count < 0:
                errors['bathrooms'] = 'Number of bathrooms cannot be negative'
            elif bath_count > 50:  # Reasonable upper limit
                errors['bathrooms'] = 'Number of bathrooms cannot exceed 50'
        except (ValueError, TypeError):
            errors['bathrooms'] = 'Number of bathrooms must be a whole number'
    
    # Validate car spaces
    car_spaces = property_data.get('car_spaces')
    if car_spaces is not None:
        try:
            car_count = int(car_spaces)
            if car_count < 0:
                errors['car_spaces'] = 'Number of car spaces cannot be negative'
            elif car_count > 100:  # Reasonable upper limit
                errors['car_spaces'] = 'Number of car spaces cannot exceed 100'
        except (ValueError, TypeError):
            errors['car_spaces'] = 'Number of car spaces must be a whole number'
    
    # Logical validation: bathrooms should generally not exceed bedrooms + 2
    if (bedrooms is not None and bathrooms is not None and 
        bedrooms >= 0 and bathrooms >= 0):
        try:
            if int(bathrooms) > int(bedrooms) + 3:
                errors['bathrooms'] = 'Number of bathrooms seems unusually high compared to bedrooms'
        except (ValueError, TypeError):
            pass  # Already validated above
    
    return errors


def _validate_mortgage_details(property_data):
    """Validate mortgage and debt information"""
    errors = {}
    
    # Validate mortgagee names
    current_mortgagee = property_data.get('current_mortgagee', '').strip()
    if current_mortgagee and len(current_mortgagee) < 2:
        errors['current_mortgagee'] = 'Mortgagee name must be at least 2 characters'
    
    first_mortgage = property_data.get('first_mortgage', '').strip()
    if first_mortgage and len(first_mortgage) < 2:
        errors['first_mortgage'] = 'First mortgage details must be at least 2 characters'
    
    second_mortgage = property_data.get('second_mortgage', '').strip()
    if second_mortgage and len(second_mortgage) < 2:
        errors['second_mortgage'] = 'Second mortgage details must be at least 2 characters'
    
    return errors


def validate_australian_postcode(postcode, state=None):
    """
    Standalone function to validate Australian postcodes
    
    Args:
        postcode: The postcode to validate
        state: Optional state to validate against
        
    Raises:
        ValidationError: If postcode is invalid
    """
    if not postcode:
        return
    
    if not re.match(r'^\d{4}$', str(postcode)):
        raise ValidationError('Australian postcode must be 4 digits')
    
    if state:
        postcode_int = int(postcode)
        state_upper = state.upper()
        
        postcode_ranges = {
            'NSW': [(1000, 2999)],
            'ACT': [(200, 299), (2600, 2699)],
            'VIC': [(3000, 3999), (8000, 8999)],
            'QLD': [(4000, 4999), (9000, 9999)],
            'SA': [(5000, 5999)],
            'WA': [(6000, 6999)],
            'TAS': [(7000, 7999)],
            'NT': [(800, 899)]
        }
        
        if state_upper in postcode_ranges:
            valid_range = False
            for start, end in postcode_ranges[state_upper]:
                if start <= postcode_int <= end:
                    valid_range = True
                    break
            if not valid_range:
                raise ValidationError(f'Postcode {postcode} is not valid for {state_upper}')


def validate_property_value_range(value, field_name="value"):
    """
    Standalone function to validate property value ranges
    
    Args:
        value: The value to validate
        field_name: Name of the field for error messages
        
    Raises:
        ValidationError: If value is invalid
    """
    if value is None:
        return
    
    try:
        decimal_value = Decimal(str(value))
        if decimal_value <= 0:
            raise ValidationError(f'{field_name} must be greater than 0')
        elif decimal_value > Decimal('100000000'):
            raise ValidationError(f'{field_name} cannot exceed $100,000,000')
    except (ValueError, TypeError, InvalidOperation):
        raise ValidationError(f'{field_name} must be a valid number') 