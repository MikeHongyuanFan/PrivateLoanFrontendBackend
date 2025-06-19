"""
Business Validation Functions

This module contains validators for business-related data including
ABN, ACN validation and company borrower information validation.
"""

from django.core.exceptions import ValidationError
import re


def validate_abn(abn):
    """
    Validate Australian Business Number (ABN)
    
    ABN must be 11 digits with no spaces or special characters
    """
    # Remove any spaces or special characters
    abn_cleaned = re.sub(r'[^0-9]', '', abn)
    
    if len(abn_cleaned) != 11:
        raise ValidationError('ABN must be 11 digits')
    
    # ABN validation algorithm
    # Weights for each digit
    weights = [10, 1, 3, 5, 7, 9, 11, 13, 15, 17, 19]
    
    # Subtract 1 from the first digit
    digits = [int(d) for d in abn_cleaned]
    digits[0] -= 1
    
    # Calculate the weighted sum
    total = sum(w * d for w, d in zip(weights, digits))
    
    # Valid ABN should be divisible by 89
    if total % 89 != 0:
        raise ValidationError('Invalid ABN checksum')
    
    return abn_cleaned


def validate_acn(acn):
    """
    Validate Australian Company Number (ACN)
    
    ACN must be 9 digits with no spaces or special characters
    """
    # Remove any spaces or special characters
    acn_cleaned = re.sub(r'[^0-9]', '', acn)
    
    if len(acn_cleaned) != 9:
        raise ValidationError('ACN must be 9 digits')
    
    # ACN validation algorithm
    # Weights for each digit
    weights = [8, 7, 6, 5, 4, 3, 2, 1]
    
    # Calculate the weighted sum
    digits = [int(d) for d in acn_cleaned[:-1]]  # Exclude the check digit
    total = sum(w * d for w, d in zip(weights, digits))
    
    # Calculate the check digit
    remainder = total % 10
    check_digit = (10 - remainder) % 10
    
    # Verify the check digit
    if check_digit != int(acn_cleaned[-1]):
        raise ValidationError('Invalid ACN checksum')
    
    return acn_cleaned


def validate_company_borrower(company_data):
    """
    Validate company borrower information
    """
    errors = {}
    
    # Validate required fields and identifiers
    errors.update(_validate_required_fields(company_data))
    errors.update(_validate_identifiers(company_data))
    
    # Validate business type and years
    errors.update(_validate_business_details(company_data))
    
    # Validate financial information
    errors.update(_validate_financial_info(company_data))
    
    # Validate address information
    errors.update(_validate_address(company_data))
    
    # Validate directors information
    errors.update(_validate_directors(company_data))
    
    return errors


def _validate_required_fields(company_data):
    """Validate optional company fields - no fields are required anymore"""
    errors = {}
    # All fields are now optional - no validation needed
    return errors


def _validate_identifiers(company_data):
    """Validate ABN and ACN"""
    errors = {}
    
    # ABN validation
    if company_data.get('company_abn'):
        try:
            validate_abn(company_data['company_abn'])
        except ValidationError as e:
            errors['company_abn'] = str(e)
    
    # ACN validation
    if company_data.get('company_acn'):
        try:
            validate_acn(company_data['company_acn'])
        except ValidationError as e:
            errors['company_acn'] = str(e)
            
    return errors


def _validate_business_details(company_data):
    """Validate business type and years in business"""
    errors = {}
    
    # Industry type validation
    from borrowers.models import Borrower
    valid_industry_types = [choice[0] for choice in Borrower.INDUSTRY_TYPE_CHOICES]
    if company_data.get('industry_type') and company_data['industry_type'] not in valid_industry_types:
        errors['industry_type'] = 'Invalid industry type'
    
    # Annual company income validation
    if company_data.get('annual_company_income'):
        try:
            income = float(company_data['annual_company_income'])
            if income < 0:
                errors['annual_company_income'] = 'Annual company income cannot be negative'
        except (ValueError, TypeError):
            errors['annual_company_income'] = 'Annual company income must be a number'
            
    return errors


def _validate_financial_info(company_data):
    """Validate financial information"""
    errors = {}
    
    financial_fields = ['annual_revenue', 'net_profit', 'assets', 'liabilities']
    if 'financial_info' in company_data:
        for field in financial_fields:
            if field in company_data['financial_info'] and company_data['financial_info'][field]:
                try:
                    amount = float(company_data['financial_info'][field])
                    if field != 'net_profit' and amount < 0:
                        errors[f'financial_info.{field}'] = f'{field.replace("_", " ").title()} cannot be negative'
                except (ValueError, TypeError):
                    errors[f'financial_info.{field}'] = f'{field.replace("_", " ").title()} must be a number'
                    
    return errors


def _validate_address(company_data):
    """Validate company address"""
    errors = {}
    
    # Check if at least street name, suburb, state, and postcode are provided
    address_fields = ['registered_address_street_name', 'registered_address_suburb', 
                     'registered_address_state', 'registered_address_postcode']
    
    for field in address_fields:
        if not company_data.get(field):
            errors[field] = f'{field.replace("registered_address_", "").replace("_", " ").title()} is required'
    
    # Postal code validation for Australia
    if company_data.get('registered_address_state', '').lower() in ['nsw', 'vic', 'qld', 'sa', 'wa', 'tas', 'nt', 'act'] and company_data.get('registered_address_postcode'):
        if not re.match(r'^\d{4}$', str(company_data['registered_address_postcode'])):
            errors['registered_address_postcode'] = 'Australian postal code must be 4 digits'
                
    return errors


def _validate_directors(company_data):
    """Validate company directors"""
    errors = {}
    
    if 'directors' in company_data and company_data['directors']:
        for i, director in enumerate(company_data['directors']):
            if not director.get('name'):
                errors[f'directors[{i}].name'] = 'Director name is required'
            
            # Validate roles
            if director.get('roles'):
                valid_roles = ['director', 'secretary', 'public_officer', 'shareholder']
                roles = director['roles'].split(',')
                for role in roles:
                    role = role.strip().lower()
                    if role and role not in valid_roles:
                        errors[f'directors[{i}].roles'] = f'Invalid role: {role}'
                
    return errors 