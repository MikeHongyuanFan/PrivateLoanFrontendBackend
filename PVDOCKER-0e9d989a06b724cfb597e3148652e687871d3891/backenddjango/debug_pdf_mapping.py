#!/usr/bin/env python3
"""
Debug script for PDF field mapping issues

This script helps identify why company borrower assets/liabilities and
individual borrower/guarantor assets/liabilities are not being filled correctly.
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

from applications.models import Application
from applications.utils.pdf_field_mapping import generate_pdf_field_mapping_from_json
from applications.serializers.application import ApplicationDetailSerializer
from rest_framework.test import APIRequestFactory
import json


def debug_pdf_mapping():
    """Debug the PDF field mapping for a specific application"""
    
    # Get the first application with data
    app = Application.objects.first()
    
    if not app:
        print("No applications found in the database.")
        return
    
    print(f"Debugging PDF mapping for Application ID: {app.id}")
    print(f"Reference Number: {app.reference_number}")
    print("=" * 80)
    
    # Create a mock request for the serializer
    factory = APIRequestFactory()
    request = factory.get('/')
    
    # Serialize the application with cascade data
    serializer = ApplicationDetailSerializer(app, context={'request': request})
    cascade_data = serializer.data
    
    print("CASCADE DATA STRUCTURE:")
    print("=" * 40)
    
    # Check company borrowers
    company_borrowers = cascade_data.get('company_borrowers', [])
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
    borrowers = cascade_data.get('borrowers', [])
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
    guarantors = cascade_data.get('guarantors', [])
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
    field_mapping = generate_pdf_field_mapping_from_json(cascade_data)
    
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


if __name__ == "__main__":
    debug_pdf_mapping() 