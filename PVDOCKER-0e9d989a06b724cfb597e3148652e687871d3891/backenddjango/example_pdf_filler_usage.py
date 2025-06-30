#!/usr/bin/env python3
"""
Example usage of the PDF Filler Utility

This script demonstrates how to use the PDF filler function to generate
filled PDF forms from application data.
"""

import os
import sys
import django
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'crm_backend.settings')
django.setup()

from applications.utils.pdf_filler import fill_pdf_form, get_field_mapping_summary
from applications.utils.pdf_field_mapping import generate_pdf_field_mapping_from_json


def example_usage():
    """Example of how to use the PDF filler utility."""
    
    # Sample application data (similar to what would come from the cascade API)
    sample_data = {
        'application': {
            'loan_amount': '750000.00',
            'loan_term': 24,
            'estimated_settlement_date': '2024-06-15',
            'interest_rate': '9.50',
            'loan_purpose': 'purchase',
            'additional_comments': 'Property purchase for investment purposes',
            'has_pending_litigation': False,
            'has_unsatisfied_judgements': False,
            'has_been_bankrupt': False,
            'has_been_refused_credit': False,
            'has_outstanding_ato_debt': False,
            'has_outstanding_tax_returns': False,
            'has_payment_arrangements': False,
            'has_other_credit_providers': True,
            'other_credit_providers_details': 'Applied to ABC Bank for comparison',
            'exit_strategy': 'refinance',
            'exit_strategy_details': 'Refinance to conventional lender after 12 months'
        },
        'borrowers': [{
            'title': 'Mr',
            'first_name': 'John',
            'last_name': 'Smith',
            'date_of_birth': '1985-05-15',
            'drivers_licence_no': 'DL123456789',
            'home_phone': '0298765432',
            'mobile': '0412345678',
            'email': 'john.smith@email.com',
            'address_unit': 'Unit 2',
            'address_street_no': '456',
            'address_street_name': 'Oak Avenue',
            'address_suburb': 'Melbourne',
            'address_state': 'VIC',
            'address_postcode': '3000',
            'occupation': 'Software Engineer',
            'employer_name': 'Tech Solutions Pty Ltd',
            'employment_type': 'full_time',
            'annual_income': '120000.00'
        }],
        'company_borrowers': [{
            'company_name': 'Smith Investments Pty Ltd',
            'company_abn': '12345678901',
            'industry_type': 'Property Investment',
            'contact_number': '0412345678',
            'annual_company_income': '500000.00',
            'is_trustee': True,
            'is_smsf_trustee': False,
            'trustee_name': 'John Smith',
            'directors': [{
                'first_name': 'John',
                'last_name': 'Smith',
                'roles': ['director', 'secretary'],
                'director_id': '123456789012'
            }],
            'registered_address_unit': 'Unit 1',
            'registered_address_street_no': '123',
            'registered_address_street_name': 'Main Street',
            'registered_address_suburb': 'Sydney',
            'registered_address_state': 'NSW',
            'registered_address_postcode': '2000',
            'assets': [
                {
                    'asset_type': 'property',
                    'address': '123 Investment St, Sydney NSW 2000',
                    'value': '800000.00',
                    'amount_owing': '400000.00',
                    'to_be_refinanced': True
                },
                {
                    'asset_type': 'savings',
                    'value': '100000.00',
                    'amount_owing': '0.00',
                    'to_be_refinanced': False
                }
            ],
            'liabilities': [
                {
                    'liability_type': 'credit_card',
                    'amount': '15000.00',
                    'to_be_refinanced': True
                }
            ]
        }],
        'guarantors': [{
            'title': 'Mrs',
            'first_name': 'Jane',
            'last_name': 'Smith',
            'date_of_birth': '1987-08-20',
            'drivers_licence_no': 'DL987654321',
            'home_phone': '0298765433',
            'mobile': '0412345679',
            'email': 'jane.smith@email.com',
            'address_unit': 'Unit 2',
            'address_street_no': '456',
            'address_street_name': 'Oak Avenue',
            'address_suburb': 'Melbourne',
            'address_state': 'VIC',
            'address_postcode': '3000',
            'occupation': 'Accountant',
            'employer_name': 'Financial Services Ltd',
            'employment_type': 'full_time',
            'annual_income': '95000.00',
            'assets': [
                {
                    'asset_type': 'property',
                    'address': '789 Guarantor St, Melbourne VIC 3000',
                    'value': '600000.00',
                    'amount_owing': '300000.00',
                    'bg_type': 'BG1'
                }
            ],
            'liabilities': [
                {
                    'liability_type': 'credit_card',
                    'amount': '8000.00',
                    'bg_type': 'BG1'
                }
            ]
        }],
        'security_properties': [{
            'address_unit': 'Unit 3',
            'address_street_no': '789',
            'address_street_name': 'Security Street',
            'address_suburb': 'Brisbane',
            'address_state': 'QLD',
            'address_postcode': '4000',
            'first_mortgage': '500000.00',
            'second_mortgage': '100000.00',
            'first_mortgage_debt': '450000.00',
            'second_mortgage_debt': '90000.00',
            'estimated_value': '900000.00',
            'purchase_price': '750000.00',
            'property_type': 'residential',
            'bedrooms': 4,
            'bathrooms': 2,
            'car_spaces': 2,
            'building_size': '200.00',
            'land_size': '500.00',
            'is_single_story': True,
            'has_garage': True,
            'has_carport': False,
            'has_off_street_parking': True,
            'occupancy': 'owner_occupied'
        }],
        'loan_requirements': [
            {
                'description': 'Property purchase',
                'amount': '700000.00'
            },
            {
                'description': 'Legal fees',
                'amount': '25000.00'
            },
            {
                'description': 'Stamp duty',
                'amount': '25000.00'
            }
        ]
    }
    
    print("=== PDF Filler Utility Example ===\n")
    
    # Step 1: Generate field mapping
    print("1. Generating PDF field mapping...")
    field_mapping = generate_pdf_field_mapping_from_json(sample_data)
    print(f"   Generated {len(field_mapping)} field mappings")
    
    # Step 2: Get mapping summary
    print("\n2. Field mapping summary:")
    summary = get_field_mapping_summary(field_mapping)
    for key, value in summary.items():
        if key not in ['sample_text_fields', 'sample_checkbox_fields']:
            print(f"   {key}: {value}")
    
    print("\n3. Sample text fields:")
    for field_id, value in summary['sample_text_fields'].items():
        print(f"   {field_id}: {value}")
    
    print("\n4. Sample checkbox fields:")
    for field_id, value in summary['sample_checkbox_fields'].items():
        print(f"   {field_id}: {value}")
    
    # Step 3: Show some key mappings
    print("\n5. Key field mappings:")
    key_fields = [
        ('text1', 'Company Name'),
        ('text5', 'Annual Company Income'),
        ('text107', 'Borrower First Name'),
        ('text108', 'Borrower Last Name'),
        ('text297', 'Loan Amount'),
        ('text298', 'Loan Term'),
        ('text302', 'Interest Rate'),
        ('checkbox20', 'Is Trustee'),
        ('checkbox303', 'Loan Purpose - Purchase')
    ]
    
    for field_id, description in key_fields:
        value = field_mapping.get(field_id, 'Not mapped')
        print(f"   {field_id} ({description}): {value}")
    
    print("\n=== Example completed successfully! ===")
    print("\nTo actually fill a PDF, you would:")
    print("1. Have a real Application instance")
    print("2. Call fill_pdf_form(application, output_path)")
    print("3. The function would use the field mapping to fill the PDF template")


if __name__ == "__main__":
    example_usage() 