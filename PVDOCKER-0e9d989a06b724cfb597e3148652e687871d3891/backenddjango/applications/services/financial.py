"""
Financial Services

This module contains services related to financial calculations, fee management,
repayment schedules, and funding calculations for loan applications.
"""

from datetime import datetime, timedelta
from decimal import Decimal, InvalidOperation
from django.utils import timezone

from ..models import Application, FundingCalculationHistory
from documents.models import Fee, Repayment, Note


def safe_decimal(value, default=0):
    """
    Safely convert a value to Decimal, handling None, empty strings, and invalid values
    
    Args:
        value: The value to convert
        default: Default value to return if conversion fails
        
    Returns:
        Decimal value or default
    """
    if value is None:
        return Decimal(str(default))
    
    # Convert to string and strip whitespace
    str_value = str(value).strip()
    
    # Handle empty strings
    if not str_value:
        return Decimal(str(default))
    
    try:
        return Decimal(str_value)
    except (InvalidOperation, ValueError, TypeError):
        return Decimal(str(default))


def make_json_serializable(data):
    """
    Convert a dictionary containing Decimal objects to JSON-serializable format
    
    Args:
        data: Dictionary that may contain Decimal objects
        
    Returns:
        Dictionary with Decimal objects converted to floats
    """
    if isinstance(data, dict):
        return {key: make_json_serializable(value) for key, value in data.items()}
    elif isinstance(data, list):
        return [make_json_serializable(item) for item in data]
    elif isinstance(data, Decimal):
        return float(data)
    else:
        return data


def generate_repayment_schedule(application_id, user):
    """
    Generate a repayment schedule for an application
    
    Args:
        application_id: ID of the application
        user: User generating the schedule
        
    Returns:
        List of created Repayment objects
    """
    try:
        application = Application.objects.get(id=application_id)
    except Application.DoesNotExist:
        return []
    
    # Delete existing repayments
    application.repayments.all().delete()
    
    # Calculate repayment amount and schedule
    loan_amount = application.loan_amount
    loan_term = application.loan_term  # in months
    interest_rate = application.interest_rate / 100 if application.interest_rate else 0
    
    # Simple calculation for monthly repayments
    # For a more accurate calculation, use financial formulas
    if application.repayment_frequency == 'monthly':
        monthly_interest = interest_rate / 12
        if monthly_interest > 0:
            # Using the formula for monthly payments: P = L[i(1+i)^n]/[(1+i)^n-1]
            # where P is payment, L is loan amount, i is monthly interest rate, n is number of payments
            monthly_payment = loan_amount * (monthly_interest * (1 + monthly_interest) ** loan_term) / ((1 + monthly_interest) ** loan_term - 1)
        else:
            # If no interest, simple division
            monthly_payment = loan_amount / loan_term
        
        # Create repayment schedule
        repayments = []
        start_date = application.estimated_settlement_date or datetime.now().date()
        
        for i in range(1, loan_term + 1):
            due_date = start_date.replace(month=((start_date.month + i - 1) % 12) + 1)
            if (start_date.month + i - 1) // 12 > 0:
                due_date = due_date.replace(year=due_date.year + (start_date.month + i - 1) // 12)
            
            repayment = Repayment.objects.create(
                application=application,
                amount=round(monthly_payment, 2),
                due_date=due_date,
                created_by=user
            )
            repayments.append(repayment)
        
        return repayments
    
    # Handle other frequencies as needed
    return []


def create_standard_fees(application_id, user):
    """
    Create standard fees for an application
    
    Args:
        application_id: ID of the application
        user: User creating the fees
        
    Returns:
        List of created Fee objects
    """
    try:
        application = Application.objects.get(id=application_id)
    except Application.DoesNotExist:
        return []
    
    # Define standard fees
    standard_fees = [
        {
            'fee_type': 'application',
            'description': 'Application processing fee',
            'amount': 500.00,
        },
        {
            'fee_type': 'valuation',
            'description': 'Property valuation fee',
            'amount': 800.00,
        },
        {
            'fee_type': 'legal',
            'description': 'Legal documentation fee',
            'amount': 1200.00,
        },
        {
            'fee_type': 'settlement',
            'description': 'Settlement fee',
            'amount': 300.00,
        }
    ]
    
    # Calculate due dates
    today = timezone.now().date()
    
    # Create fees
    created_fees = []
    for fee_data in standard_fees:
        # Set due date based on fee type
        if fee_data['fee_type'] == 'application':
            due_date = today
        elif fee_data['fee_type'] == 'valuation':
            due_date = today + timedelta(days=7)
        elif fee_data['fee_type'] == 'legal':
            due_date = today + timedelta(days=14)
        else:
            due_date = today + timedelta(days=30)
        
        fee = Fee.objects.create(
            application=application,
            fee_type=fee_data['fee_type'],
            description=fee_data['description'],
            amount=fee_data['amount'],
            due_date=due_date,
            created_by=user
        )
        created_fees.append(fee)
    
    return created_fees


def calculate_funding(application, calculation_input, user):
    """
    Calculate funding requirements and available funds for an application
    
    Args:
        application: Application instance
        calculation_input: Dictionary with calculation parameters
        user: User performing the calculation
        
    Returns:
        Tuple of (calculation_result, funding_history)
    """
    # Extract parameters
    loan_amount = safe_decimal(application.loan_amount)
    interest_rate = safe_decimal(application.interest_rate) / 100 if application.interest_rate else Decimal('0')
    security_value = safe_decimal(application.security_value) if application.security_value else Decimal('0')
    
    # Extract calculation input parameters
    establishment_fee_rate = safe_decimal(calculation_input.get('establishment_fee_rate', 2.0)) / 100
    capped_interest_months = int(safe_decimal(calculation_input.get('capped_interest_months', 9)))
    monthly_line_fee_rate = safe_decimal(calculation_input.get('monthly_line_fee_rate', 0.5)) / 100
    brokerage_fee_rate = safe_decimal(calculation_input.get('brokerage_fee_rate', 2.0)) / 100
    application_fee = safe_decimal(calculation_input.get('application_fee', 500))
    due_diligence_fee = safe_decimal(calculation_input.get('due_diligence_fee', 800))
    legal_fee_before_gst = safe_decimal(calculation_input.get('legal_fee_before_gst', 1200))
    valuation_fee = safe_decimal(calculation_input.get('valuation_fee', 1000))
    monthly_account_fee = safe_decimal(calculation_input.get('monthly_account_fee', 50))
    working_fee = safe_decimal(calculation_input.get('working_fee', 0))
    
    # Calculate fees
    establishment_fee = loan_amount * establishment_fee_rate
    capped_interest = loan_amount * interest_rate * capped_interest_months / 12
    line_fee = loan_amount * monthly_line_fee_rate * capped_interest_months
    brokerage_fee = loan_amount * brokerage_fee_rate
    legal_fee = legal_fee_before_gst * Decimal('1.1')  # Add 10% GST
    
    # Calculate total fees
    total_fees = (
        establishment_fee + capped_interest + line_fee + brokerage_fee +
        application_fee + due_diligence_fee + legal_fee + valuation_fee +
        (monthly_account_fee * capped_interest_months) + working_fee
    )
    
    # Calculate funds available
    funds_available = loan_amount - total_fees
    
    # Prepare calculation result
    calculation_result = {
        'establishment_fee': float(establishment_fee),
        'capped_interest': float(capped_interest),
        'line_fee': float(line_fee),
        'brokerage_fee': float(brokerage_fee),
        'legal_fee': float(legal_fee),
        'application_fee': float(application_fee),
        'due_diligence_fee': float(due_diligence_fee),
        'valuation_fee': float(valuation_fee),
        'monthly_account_fee': float(monthly_account_fee * capped_interest_months),
        'working_fee': float(working_fee),
        'total_fees': float(total_fees),
        'funds_available': float(funds_available),
    }
    
    # Convert calculation_input to JSON-serializable format
    json_serializable_input = make_json_serializable(calculation_input)
    
    # Save calculation history
    funding_history = FundingCalculationHistory.objects.create(
        application=application,
        calculation_input=json_serializable_input,
        calculation_result=calculation_result,
        created_by=user
    )
    
    # Update the application's funding_result field with the latest calculation
    application.funding_result = calculation_result
    application.save(update_fields=['funding_result'])
    
    return calculation_result, funding_history


def calculate_funding_manual(loan_amount, interest_rate, security_value, calculation_input):
    """
    Perform a manual funding calculation without saving to database
    
    Args:
        loan_amount: Loan amount as decimal
        interest_rate: Interest rate as percentage
        security_value: Security property value
        calculation_input: Dictionary with calculation parameters
        
    Returns:
        Dictionary with calculation results
    """
    # Convert to Decimal for precise calculations
    loan_amount = safe_decimal(loan_amount)
    interest_rate = safe_decimal(interest_rate) / 100
    security_value = safe_decimal(security_value)
    
    # Extract calculation input parameters
    establishment_fee_rate = safe_decimal(calculation_input.get('establishment_fee_rate', 2.0)) / 100
    capped_interest_months = int(safe_decimal(calculation_input.get('capped_interest_months', 9)))
    monthly_line_fee_rate = safe_decimal(calculation_input.get('monthly_line_fee_rate', 0.5)) / 100
    brokerage_fee_rate = safe_decimal(calculation_input.get('brokerage_fee_rate', 2.0)) / 100
    application_fee = safe_decimal(calculation_input.get('application_fee', 500))
    due_diligence_fee = safe_decimal(calculation_input.get('due_diligence_fee', 800))
    legal_fee_before_gst = safe_decimal(calculation_input.get('legal_fee_before_gst', 1200))
    valuation_fee = safe_decimal(calculation_input.get('valuation_fee', 1000))
    monthly_account_fee = safe_decimal(calculation_input.get('monthly_account_fee', 50))
    working_fee = safe_decimal(calculation_input.get('working_fee', 0))
    
    # Calculate fees
    establishment_fee = loan_amount * establishment_fee_rate
    capped_interest = loan_amount * interest_rate * capped_interest_months / 12
    line_fee = loan_amount * monthly_line_fee_rate * capped_interest_months
    brokerage_fee = loan_amount * brokerage_fee_rate
    legal_fee = legal_fee_before_gst * Decimal('1.1')  # Add 10% GST
    
    # Calculate total fees
    total_fees = (
        establishment_fee + capped_interest + line_fee + brokerage_fee +
        application_fee + due_diligence_fee + legal_fee + valuation_fee +
        (monthly_account_fee * capped_interest_months) + working_fee
    )
    
    # Calculate funds available
    funds_available = loan_amount - total_fees
    
    # Calculate LVR (Loan to Value Ratio)
    lvr = (loan_amount / security_value * 100) if security_value > 0 else 0
    
    return {
        'loan_amount': float(loan_amount),
        'interest_rate': float(interest_rate * 100),
        'security_value': float(security_value),
        'lvr': float(lvr),
        'establishment_fee': float(establishment_fee),
        'capped_interest': float(capped_interest),
        'line_fee': float(line_fee),
        'brokerage_fee': float(brokerage_fee),
        'legal_fee': float(legal_fee),
        'application_fee': float(application_fee),
        'due_diligence_fee': float(due_diligence_fee),
        'valuation_fee': float(valuation_fee),
        'monthly_account_fee': float(monthly_account_fee * capped_interest_months),
        'working_fee': float(working_fee),
        'total_fees': float(total_fees),
        'funds_available': float(funds_available),
    }


def extend_loan(application_id, new_rate, new_loan_amount, new_repayment, user):
    """
    Extend a loan with new terms
    
    Args:
        application_id: ID of the application
        new_rate: New interest rate
        new_loan_amount: New loan amount
        new_repayment: New repayment amount
        user: User performing the extension
        
    Returns:
        Updated Application object if successful, None otherwise
    """
    try:
        application = Application.objects.get(id=application_id)
    except Application.DoesNotExist:
        return None
    
    # Store old values for history
    old_rate = application.interest_rate
    old_amount = application.loan_amount
    
    # Update application with new terms
    application.interest_rate = new_rate
    application.loan_amount = new_loan_amount
    application.save()
    
    # Create a note about the loan extension
    Note.objects.create(
        application=application,
        title="Loan Extended",
        content=f"Loan extended with new terms:\n"
                f"Previous rate: {old_rate}% -> New rate: {new_rate}%\n"
                f"Previous amount: ${old_amount} -> New amount: ${new_loan_amount}\n"
                f"New repayment: ${new_repayment}",
        created_by=user
    )
    
    # Generate new repayment schedule if needed
    generate_repayment_schedule(application_id, user)
    
    return application 