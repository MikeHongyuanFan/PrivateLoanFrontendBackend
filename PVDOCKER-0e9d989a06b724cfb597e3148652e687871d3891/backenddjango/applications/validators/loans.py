"""
Loan Validation Functions

This module contains validators for loan-related data including
loan requirements, guarantor information, and loan terms validation.
"""

from django.core.exceptions import ValidationError
from decimal import Decimal, InvalidOperation
import re


def validate_loan_requirement(loan_data):
    """
    Validate loan requirement information
    
    Args:
        loan_data: Dictionary containing loan requirement data
        
    Returns:
        Dictionary of field errors (empty if valid)
    """
    errors = {}
    
    # Validate loan amount
    errors.update(_validate_loan_amount(loan_data))
    
    # Validate loan description
    errors.update(_validate_loan_description(loan_data))
    
    return errors


def validate_guarantor(guarantor_data):
    """
    Validate guarantor information
    
    Args:
        guarantor_data: Dictionary containing guarantor data
        
    Returns:
        Dictionary of field errors (empty if valid)
    """
    errors = {}
    
    # Validate personal information
    errors.update(_validate_guarantor_personal_info(guarantor_data))
    
    # Validate contact information
    errors.update(_validate_guarantor_contact_info(guarantor_data))
    
    # Validate address information
    errors.update(_validate_guarantor_address(guarantor_data))
    
    # Validate financial information
    errors.update(_validate_guarantor_financial_info(guarantor_data))
    
    return errors


def _validate_loan_amount(loan_data):
    """Validate loan amount and financial fields"""
    errors = {}
    
    # Validate loan amount
    amount = loan_data.get('amount')
    if amount is not None:
        try:
            decimal_amount = Decimal(str(amount))
            if decimal_amount <= 0:
                errors['amount'] = 'Loan amount must be greater than 0'
            elif decimal_amount < Decimal('1000'):
                errors['amount'] = 'Loan amount must be at least $1,000'
            elif decimal_amount > Decimal('100000000'):  # $100M limit
                errors['amount'] = 'Loan amount cannot exceed $100,000,000'
        except (ValueError, TypeError, InvalidOperation):
            errors['amount'] = 'Loan amount must be a valid number'
    
    return errors


def _validate_loan_description(loan_data):
    """Validate loan description and purpose"""
    errors = {}
    
    description = loan_data.get('description', '').strip()
    if description:
        if len(description) < 3:
            errors['description'] = 'Loan description must be at least 3 characters'
        elif len(description) > 255:
            errors['description'] = 'Loan description cannot exceed 255 characters'
        
        # Check for meaningful content (not just whitespace or common fillers)
        if re.match(r'^[\s\.\-_]*$', description):
            errors['description'] = 'Please provide a meaningful loan description'
    
    return errors


def _validate_guarantor_personal_info(guarantor_data):
    """Validate guarantor personal information"""
    errors = {}
    
    # Validate first name
    first_name = guarantor_data.get('first_name', '').strip()
    if first_name:
        if len(first_name) < 1:
            errors['first_name'] = 'First name is required'
        elif len(first_name) > 50:
            errors['first_name'] = 'First name cannot exceed 50 characters'
        elif not re.match(r'^[a-zA-Z\s\'\-\.]+$', first_name):
            errors['first_name'] = 'First name contains invalid characters'
    
    # Validate last name
    last_name = guarantor_data.get('last_name', '').strip()
    if last_name:
        if len(last_name) < 1:
            errors['last_name'] = 'Last name is required'
        elif len(last_name) > 50:
            errors['last_name'] = 'Last name cannot exceed 50 characters'
        elif not re.match(r'^[a-zA-Z\s\'\-\.]+$', last_name):
            errors['last_name'] = 'Last name contains invalid characters'
    
    # Validate date of birth
    date_of_birth = guarantor_data.get('date_of_birth')
    if date_of_birth:
        from datetime import date, datetime
        try:
            if isinstance(date_of_birth, str):
                # Try to parse string date
                birth_date = datetime.strptime(date_of_birth, '%Y-%m-%d').date()
            else:
                birth_date = date_of_birth
            
            # Check age (must be at least 18)
            today = date.today()
            age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
            
            if age < 18:
                errors['date_of_birth'] = 'Guarantor must be at least 18 years old'
            elif age > 120:
                errors['date_of_birth'] = 'Please provide a valid date of birth'
        except (ValueError, TypeError):
            errors['date_of_birth'] = 'Please provide a valid date in YYYY-MM-DD format'
    
    return errors


def _validate_guarantor_contact_info(guarantor_data):
    """Validate guarantor contact information"""
    errors = {}
    
    # Validate email
    email = guarantor_data.get('email', '').strip()
    if email:
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, email):
            errors['email'] = 'Please provide a valid email address'
        elif len(email) > 254:
            errors['email'] = 'Email address is too long'
    
    # Validate phone number
    phone = guarantor_data.get('phone', '').strip()
    if phone:
        # Remove common separators for validation
        phone_clean = re.sub(r'[\s\-\(\)\+]', '', phone)
        
        # Australian phone number validation
        if not re.match(r'^(\+?61)?[0-9]{8,10}$', phone_clean):
            errors['phone'] = 'Please provide a valid Australian phone number'
        elif len(phone_clean) < 8:
            errors['phone'] = 'Phone number is too short'
        elif len(phone_clean) > 15:
            errors['phone'] = 'Phone number is too long'
    
    # Validate mobile number
    mobile = guarantor_data.get('mobile', '').strip()
    if mobile:
        # Remove common separators for validation
        mobile_clean = re.sub(r'[\s\-\(\)\+]', '', mobile)
        
        # Australian mobile number validation (starts with 04 or 614)
        if not re.match(r'^(\+?61)?4[0-9]{8}$', mobile_clean):
            errors['mobile'] = 'Please provide a valid Australian mobile number'
    
    return errors


def _validate_guarantor_address(guarantor_data):
    """Validate guarantor address information"""
    errors = {}
    
    # Similar to property address validation but for guarantor
    street_name = guarantor_data.get('address_street_name', '').strip()
    suburb = guarantor_data.get('address_suburb', '').strip()
    state = guarantor_data.get('address_state', '').strip()
    postcode = guarantor_data.get('address_postcode', '').strip()
    
    # If any address field is provided, validate complete address
    address_fields = [street_name, suburb, state, postcode]
    if any(address_fields):
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
    
    return errors


def _validate_guarantor_financial_info(guarantor_data):
    """Validate guarantor financial information"""
    errors = {}
    
    # Validate annual income
    annual_income = guarantor_data.get('annual_income')
    if annual_income is not None:
        try:
            income = Decimal(str(annual_income))
            if income < 0:
                errors['annual_income'] = 'Annual income cannot be negative'
            elif income > Decimal('10000000'):  # $10M limit
                errors['annual_income'] = 'Annual income cannot exceed $10,000,000'
        except (ValueError, TypeError, InvalidOperation):
            errors['annual_income'] = 'Annual income must be a valid number'
    
    # Validate net worth
    net_worth = guarantor_data.get('net_worth')
    if net_worth is not None:
        try:
            worth = Decimal(str(net_worth))
            # Net worth can be negative
            if worth < Decimal('-100000000'):  # -$100M limit
                errors['net_worth'] = 'Net worth cannot be less than -$100,000,000'
            elif worth > Decimal('1000000000'):  # $1B limit
                errors['net_worth'] = 'Net worth cannot exceed $1,000,000,000'
        except (ValueError, TypeError, InvalidOperation):
            errors['net_worth'] = 'Net worth must be a valid number'
    
    # Validate assets and liabilities
    total_assets = guarantor_data.get('total_assets')
    if total_assets is not None:
        try:
            assets = Decimal(str(total_assets))
            if assets < 0:
                errors['total_assets'] = 'Total assets cannot be negative'
            elif assets > Decimal('1000000000'):  # $1B limit
                errors['total_assets'] = 'Total assets cannot exceed $1,000,000,000'
        except (ValueError, TypeError, InvalidOperation):
            errors['total_assets'] = 'Total assets must be a valid number'
    
    total_liabilities = guarantor_data.get('total_liabilities')
    if total_liabilities is not None:
        try:
            liabilities = Decimal(str(total_liabilities))
            if liabilities < 0:
                errors['total_liabilities'] = 'Total liabilities cannot be negative'
            elif liabilities > Decimal('1000000000'):  # $1B limit
                errors['total_liabilities'] = 'Total liabilities cannot exceed $1,000,000,000'
        except (ValueError, TypeError, InvalidOperation):
            errors['total_liabilities'] = 'Total liabilities must be a valid number'
    
    # Cross-validation: net worth should equal assets - liabilities (if all provided)
    if (total_assets is not None and total_liabilities is not None and net_worth is not None):
        try:
            assets = Decimal(str(total_assets))
            liabilities = Decimal(str(total_liabilities))
            worth = Decimal(str(net_worth))
            calculated_net_worth = assets - liabilities
            
            # Allow small differences due to rounding
            if abs(calculated_net_worth - worth) > Decimal('1000'):
                errors['net_worth'] = 'Net worth should equal total assets minus total liabilities'
        except (ValueError, TypeError, InvalidOperation):
            pass  # Already validated above
    
    return errors


def validate_loan_term(term_months):
    """
    Standalone function to validate loan terms
    
    Args:
        term_months: Loan term in months
        
    Raises:
        ValidationError: If term is invalid
    """
    if term_months is None:
        return
    
    try:
        term = int(term_months)
        if term <= 0:
            raise ValidationError('Loan term must be greater than 0 months')
        elif term > 480:  # 40 years maximum
            raise ValidationError('Loan term cannot exceed 40 years (480 months)')
        elif term < 1:
            raise ValidationError('Loan term must be at least 1 month')
    except (ValueError, TypeError):
        raise ValidationError('Loan term must be a whole number of months')


def validate_interest_rate(rate):
    """
    Standalone function to validate interest rates
    
    Args:
        rate: Interest rate as percentage
        
    Raises:
        ValidationError: If rate is invalid
    """
    if rate is None:
        return
    
    try:
        interest_rate = Decimal(str(rate))
        if interest_rate < 0:
            raise ValidationError('Interest rate cannot be negative')
        elif interest_rate > Decimal('50'):
            raise ValidationError('Interest rate cannot exceed 50%')
        elif interest_rate == 0:
            raise ValidationError('Interest rate must be greater than 0%')
    except (ValueError, TypeError, InvalidOperation):
        raise ValidationError('Interest rate must be a valid number')


def validate_repayment_frequency(frequency):
    """
    Standalone function to validate repayment frequency
    
    Args:
        frequency: Repayment frequency string
        
    Raises:
        ValidationError: If frequency is invalid
    """
    if not frequency:
        return
    
    valid_frequencies = [
        'weekly', 'fortnightly', 'monthly', 'quarterly', 
        'semi-annually', 'annually', 'interest-only'
    ]
    
    if frequency.lower() not in valid_frequencies:
        raise ValidationError(f'Invalid repayment frequency. Must be one of: {", ".join(valid_frequencies)}') 