#!/usr/bin/env python3
"""
Test script for PDF field mapping with mock data

This script creates mock application data to test the PDF field mapping
and identify issues with company borrower assets/liabilities and
individual borrower/guarantor assets/liabilities.
"""

import os
import sys
import django
from pathlib import Path
from decimal import Decimal

# Add the project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'crm_backend.settings')
django.setup()

from applications.utils.pdf_field_mapping import generate_pdf_field_mapping_from_json


def create_mock_application_data():
    """Create mock application data for testing"""
    
    mock_data = {
        # Application fields
        'loan_amount': '750000.00',
        'loan_term': 24,
        'interest_rate': '9.50',
        'estimated_settlement_date': '2024-06-15',
        'loan_purpose': 'purchase',
        'additional_comments': 'Test application',
        'has_pending_litigation': False,
        'has_unsatisfied_judgements': False,
        'has_been_bankrupt': False,
        'has_been_refused_credit': False,
        'has_outstanding_ato_debt': False,
        'has_outstanding_tax_returns': False,
        'has_payment_arrangements': False,
        'has_other_credit_providers': False,
        'other_credit_providers_details': '',
        'exit_strategy': 'refinance',
        'exit_strategy_details': 'Refinance to lower rate',
        
        # Company Borrowers
        'company_borrowers': [
            {
                'company_name': 'Test Company Pty Ltd',
                'company_abn': '12345678901',
                'company_acn': '123456789',
                'industry_type': 'real_estate',
                'contact_number': '0412345678',
                'annual_company_income': '500000.00',
                'is_trustee': False,
                'is_smsf_trustee': False,
                'trustee_name': '',
                'registered_address_unit': '1',
                'registered_address_street_no': '123',
                'registered_address_street_name': 'Test Street',
                'registered_address_suburb': 'Test Suburb',
                'registered_address_state': 'NSW',
                'registered_address_postcode': '2000',
                'directors': [
                    {
                        'name': 'John Smith',
                        'roles': 'director, secretary',
                        'director_id': '123456789012'
                    },
                    {
                        'name': 'Jane Doe',
                        'roles': 'director',
                        'director_id': '987654321098'
                    }
                ],
                'assets': [
                    {
                        'asset_type': 'Property',
                        'address': '123 Test Property Street, Test Suburb NSW 2000',
                        'value': '800000.00',
                        'amount_owing': '400000.00',
                        'to_be_refinanced': True
                    },
                    {
                        'asset_type': 'Vehicle',
                        'value': '50000.00',
                        'amount_owing': '20000.00',
                        'to_be_refinanced': False
                    },
                    {
                        'asset_type': 'Savings',
                        'value': '100000.00',
                        'amount_owing': '0.00',
                        'to_be_refinanced': False
                    },
                    {
                        'asset_type': 'Investment Shares',
                        'value': '75000.00',
                        'amount_owing': '0.00',
                        'to_be_refinanced': False
                    }
                ],
                'liabilities': [
                    {
                        'liability_type': 'credit_card',
                        'amount': '15000.00',
                        'to_be_refinanced': True
                    },
                    {
                        'liability_type': 'other_creditor',
                        'amount': '25000.00',
                        'to_be_refinanced': False
                    }
                ]
            }
        ],
        
        # Individual Borrowers
        'borrowers': [
            {
                'title': 'mr',
                'first_name': 'John',
                'last_name': 'Smith',
                'date_of_birth': '1980-01-15',
                'drivers_licence_no': '123456789',
                'home_phone': '0298765432',
                'mobile': '0412345678',
                'email': 'john.smith@email.com',
                'address_unit': '2',
                'address_street_no': '456',
                'address_street_name': 'Home Street',
                'address_suburb': 'Home Suburb',
                'address_state': 'NSW',
                'address_postcode': '2001',
                'occupation': 'Manager',
                'employer_name': 'Test Employer',
                'employment_type': 'full_time',
                'annual_income': '120000.00',
                'assets': [
                    {
                        'asset_type': 'Property',
                        'address': '456 Home Property Street, Home Suburb NSW 2001',
                        'value': '600000.00',
                        'amount_owing': '300000.00',
                        'bg_type': 'BG1'
                    },
                    {
                        'asset_type': 'Vehicle',
                        'value': '35000.00',
                        'amount_owing': '15000.00',
                        'bg_type': 'BG1'
                    },
                    {
                        'asset_type': 'Savings',
                        'value': '50000.00',
                        'amount_owing': '0.00',
                        'bg_type': 'BG1'
                    }
                ],
                'liabilities': [
                    {
                        'liability_type': 'credit_card',
                        'amount': '8000.00',
                        'bg_type': 'bg1'
                    },
                    {
                        'liability_type': 'personal_loan',
                        'amount': '12000.00',
                        'bg_type': 'bg1'
                    }
                ]
            }
        ],
        
        # Guarantors
        'guarantors': [
            {
                'guarantor_type': 'individual',
                'title': 'mrs',
                'first_name': 'Jane',
                'last_name': 'Doe',
                'date_of_birth': '1982-05-20',
                'drivers_licence_no': '987654321',
                'home_phone': '0298765433',
                'mobile': '0498765432',
                'email': 'jane.doe@email.com',
                'address_unit': '3',
                'address_street_no': '789',
                'address_street_name': 'Guarantor Street',
                'address_suburb': 'Guarantor Suburb',
                'address_state': 'NSW',
                'address_postcode': '2002',
                'occupation': 'Accountant',
                'employer_name': 'Test Accounting',
                'employment_type': 'full_time',
                'annual_income': '90000.00',
                'assets': [
                    {
                        'asset_type': 'Property',
                        'address': '789 Guarantor Property Street, Guarantor Suburb NSW 2002',
                        'value': '450000.00',
                        'amount_owing': '200000.00',
                        'bg_type': 'BG2'
                    },
                    {
                        'asset_type': 'Investment Shares',
                        'value': '25000.00',
                        'amount_owing': '0.00',
                        'bg_type': 'BG2'
                    }
                ],
                'liabilities': [
                    {
                        'liability_type': 'credit_card',
                        'amount': '5000.00',
                        'bg_type': 'bg2'
                    }
                ]
            }
        ],
        
        # Security Properties
        'security_properties': [
            {
                'address_unit': '1',
                'address_street_no': '100',
                'address_street_name': 'Security Street',
                'address_suburb': 'Security Suburb',
                'address_state': 'NSW',
                'address_postcode': '2003',
                'first_mortgage': '500000.00',
                'second_mortgage': '0.00',
                'first_mortgage_debt': '450000.00',
                'second_mortgage_debt': '0.00',
                'estimated_value': '750000.00',
                'purchase_price': '600000.00',
                'property_type': 'residential',
                'bedrooms': 3,
                'bathrooms': 2,
                'car_spaces': 2,
                'building_size': '200.00',
                'land_size': '500.00',
                'is_single_story': True,
                'has_garage': True,
                'has_carport': False,
                'has_off_street_parking': True,
                'occupancy': 'owner_occupied'
            }
        ],
        
        # Loan Requirements
        'loan_requirements': [
            {
                'description': 'Property Purchase',
                'amount': '500000.00'
            },
            {
                'description': 'Stamp Duty',
                'amount': '25000.00'
            },
            {
                'description': 'Legal Costs',
                'amount': '5000.00'
            }
        ]
    }
    
    return mock_data


def test_pdf_mapping():
    """Test the PDF field mapping with mock data"""
    
    print("Testing PDF Field Mapping with Mock Data")
    print("=" * 80)
    
    # Create mock data
    mock_data = create_mock_application_data()
    
    print("MOCK DATA STRUCTURE:")
    print("=" * 40)
    
    # Check company borrowers
    company_borrowers = mock_data.get('company_borrowers', [])
    print(f"Company Borrowers Count: {len(company_borrowers)}")
    
    for i, company in enumerate(company_borrowers):
        print(f"\nCompany Borrower {i+1}:")
        print(f"  Company Name: {company.get('company_name', 'N/A')}")
        print(f"  ABN/ACN: {company.get('company_abn', 'N/A')} / {company.get('company_acn', 'N/A')}")
        print(f"  Industry Type: {company.get('industry_type', 'N/A')}")
        print(f"  Annual Income: {company.get('annual_company_income', 'N/A')}")
        
        # Check directors
        directors = company.get('directors', [])
        print(f"  Directors Count: {len(directors)}")
        for j, director in enumerate(directors):
            print(f"    Director {j+1}: {director.get('name', 'N/A')} - {director.get('roles', 'N/A')} - ID: {director.get('director_id', 'N/A')}")
        
        # Check assets
        assets = company.get('assets', [])
        print(f"  Assets Count: {len(assets)}")
        for j, asset in enumerate(assets):
            print(f"    Asset {j+1}: {asset.get('asset_type', 'N/A')} - Value: {asset.get('value', 'N/A')} - Owing: {asset.get('amount_owing', 'N/A')}")
        
        # Check liabilities
        liabilities = company.get('liabilities', [])
        print(f"  Liabilities Count: {len(liabilities)}")
        for j, liability in enumerate(liabilities):
            print(f"    Liability {j+1}: {liability.get('liability_type', 'N/A')} - Amount: {liability.get('amount', 'N/A')}")
    
    # Check individual borrowers
    borrowers = mock_data.get('borrowers', [])
    print(f"\nIndividual Borrowers Count: {len(borrowers)}")
    
    for i, borrower in enumerate(borrowers):
        print(f"\nBorrower {i+1}:")
        print(f"  Name: {borrower.get('first_name', 'N/A')} {borrower.get('last_name', 'N/A')}")
        print(f"  Email: {borrower.get('email', 'N/A')}")
        print(f"  Annual Income: {borrower.get('annual_income', 'N/A')}")
        
        # Check assets
        assets = borrower.get('assets', [])
        print(f"  Assets Count: {len(assets)}")
        for j, asset in enumerate(assets):
            print(f"    Asset {j+1}: {asset.get('asset_type', 'N/A')} - Value: {asset.get('value', 'N/A')} - Owing: {asset.get('amount_owing', 'N/A')} - BG Type: {asset.get('bg_type', 'N/A')}")
        
        # Check liabilities
        liabilities = borrower.get('liabilities', [])
        print(f"  Liabilities Count: {len(liabilities)}")
        for j, liability in enumerate(liabilities):
            print(f"    Liability {j+1}: {liability.get('liability_type', 'N/A')} - Amount: {liability.get('amount', 'N/A')} - BG Type: {liability.get('bg_type', 'N/A')}")
    
    # Check guarantors
    guarantors = mock_data.get('guarantors', [])
    print(f"\nGuarantors Count: {len(guarantors)}")
    
    for i, guarantor in enumerate(guarantors):
        print(f"\nGuarantor {i+1}:")
        print(f"  Name: {guarantor.get('first_name', 'N/A')} {guarantor.get('last_name', 'N/A')}")
        print(f"  Type: {guarantor.get('guarantor_type', 'N/A')}")
        print(f"  Email: {guarantor.get('email', 'N/A')}")
        print(f"  Annual Income: {guarantor.get('annual_income', 'N/A')}")
        
        # Check assets
        assets = guarantor.get('assets', [])
        print(f"  Assets Count: {len(assets)}")
        for j, asset in enumerate(assets):
            print(f"    Asset {j+1}: {asset.get('asset_type', 'N/A')} - Value: {asset.get('value', 'N/A')} - Owing: {asset.get('amount_owing', 'N/A')} - BG Type: {asset.get('bg_type', 'N/A')}")
        
        # Check liabilities
        liabilities = guarantor.get('liabilities', [])
        print(f"  Liabilities Count: {len(liabilities)}")
        for j, liability in enumerate(liabilities):
            print(f"    Liability {j+1}: {liability.get('liability_type', 'N/A')} - Amount: {liability.get('amount', 'N/A')} - BG Type: {liability.get('bg_type', 'N/A')}")
    
    print("\n" + "=" * 80)
    print("GENERATING PDF FIELD MAPPING:")
    print("=" * 40)
    
    # Generate the PDF field mapping
    field_mapping = generate_pdf_field_mapping_from_json(mock_data)
    
    # Check specific fields that should be populated
    print("\nCOMPANY BORROWER FIELDS:")
    company_fields = [
        ('text1', 'Company Name'),
        ('text2', 'ABN/ACN'),
        ('text3', 'Industry Type'),
        ('text4', 'Contact Number'),
        ('text5', 'Annual Company Income'),
        ('text7', 'Director 1 Name'),
        ('text30', 'Director 2 Name'),
    ]
    
    for field_id, description in company_fields:
        value = field_mapping.get(field_id, 'NOT MAPPED')
        print(f"  {field_id} ({description}): {value}")
    
    print("\nCOMPANY ASSETS & LIABILITIES:")
    company_asset_fields = [
        ('text49', 'Property 1 Address'),
        ('text50', 'Property 1 Value'),
        ('text51', 'Property 1 Amount Owing'),
        ('text65', 'Vehicle Value'),
        ('text66', 'Vehicle Amount Owing'),
        ('text67', 'Savings Value'),
        ('text68', 'Savings Amount Owing'),
        ('text69', 'Investment Shares Value'),
        ('text70', 'Investment Shares Amount Owing'),
        ('text71', 'Credit Card Value'),
        ('text72', 'Credit Card Amount Owing'),
        ('text77', 'Total Assets'),
        ('text78', 'Total Liabilities'),
    ]
    
    for field_id, description in company_asset_fields:
        value = field_mapping.get(field_id, 'NOT MAPPED')
        print(f"  {field_id} ({description}): {value}")
    
    print("\nINDIVIDUAL BORROWER/GUARANTOR FIELDS:")
    individual_fields = [
        ('text106', 'Individual 1 Title'),
        ('text107', 'Individual 1 First Name'),
        ('text108', 'Individual 1 Last Name'),
        ('text129', 'Individual 2 Title'),
        ('text130', 'Individual 2 First Name'),
        ('text131', 'Individual 2 Last Name'),
    ]
    
    for field_id, description in individual_fields:
        value = field_mapping.get(field_id, 'NOT MAPPED')
        print(f"  {field_id} ({description}): {value}")
    
    print("\nINDIVIDUAL ASSETS & LIABILITIES:")
    individual_asset_fields = [
        ('text152', 'Property 1 Address (Individual)'),
        ('text153', 'Property 1 Value (Individual)'),
        ('text154', 'Property 1 Amount Owing (Individual)'),
        ('text166', 'Vehicle Value (Individual)'),
        ('text167', 'Vehicle Amount Owing (Individual)'),
        ('text168', 'Savings Value (Individual)'),
        ('text169', 'Savings Amount Owing (Individual)'),
        ('text178', 'Total Individual Assets'),
        ('text179', 'Total Individual Liabilities'),
    ]
    
    for field_id, description in individual_asset_fields:
        value = field_mapping.get(field_id, 'NOT MAPPED')
        print(f"  {field_id} ({description}): {value}")
    
    print("\n" + "=" * 80)
    print("SUMMARY:")
    print("=" * 40)
    
    # Count mapped fields
    total_fields = len(field_mapping)
    non_empty_fields = len([v for v in field_mapping.values() if v and str(v).strip()])
    
    print(f"Total fields mapped: {total_fields}")
    print(f"Non-empty fields: {non_empty_fields}")
    print(f"Empty fields: {total_fields - non_empty_fields}")
    
    # Show sample of mapped fields
    print(f"\nSample mapped fields (first 10):")
    for i, (field_id, value) in enumerate(list(field_mapping.items())[:10]):
        print(f"  {field_id}: {value}")

    print("================================================================================")
    print("DEBUGGING SPECIFIC ISSUES:")
    print("================================================================================")

    # Debug director data structure
    if mock_data['company_borrowers']:
        company = mock_data['company_borrowers'][0]
        directors = company.get('directors', [])
        print(f"Company directors data structure:")
        for i, director in enumerate(directors):
            print(f"  Director {i+1}: {director}")
            print(f"    name: '{director.get('name', 'NOT_FOUND')}'")
            print(f"    director_id: '{director.get('director_id', 'NOT_FOUND')}'")
            print(f"    roles: '{director.get('roles', 'NOT_FOUND')}'")

    # Debug guarantor assets/liabilities data structure
    if mock_data['guarantors']:
        guarantor = mock_data['guarantors'][0]
        print(f"\nGuarantor assets data structure:")
        for i, asset in enumerate(guarantor.get('assets', [])):
            print(f"  Asset {i+1}: {asset}")
        
        print(f"\nGuarantor liabilities data structure:")
        for i, liability in enumerate(guarantor.get('liabilities', [])):
            print(f"  Liability {i+1}: {liability}")

    # Debug the exact data being passed to mapping function
    print(f"\nExact data structure passed to mapping function:")
    print(f"Company borrowers count: {len(mock_data.get('company_borrowers', []))}")
    print(f"Individual borrowers count: {len(mock_data.get('borrowers', []))}")
    print(f"Guarantors count: {len(mock_data.get('guarantors', []))}")


if __name__ == "__main__":
    test_pdf_mapping() 