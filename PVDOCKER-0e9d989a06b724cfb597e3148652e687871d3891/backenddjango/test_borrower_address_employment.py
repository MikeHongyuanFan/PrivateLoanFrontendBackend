#!/usr/bin/env python
"""
Test script to verify that borrower address and employment information
is properly saved and retrieved after Issue 2 fix.

Run this script from the Django project root:
python test_borrower_address_employment.py
"""

import os
import sys
import django

# Setup Django environment
sys.path.append('/app')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backenddjango.settings')
django.setup()

from borrowers.models import Borrower
from applications.serializers.borrowers import BorrowerSerializer
from django.contrib.auth import get_user_model

User = get_user_model()

def test_borrower_address_employment_fix():
    """Test that address and employment data is properly handled"""
    
    print("🧪 Testing Borrower Address & Employment Fix")
    print("=" * 50)
    
    # Get or create a test user
    test_user, created = User.objects.get_or_create(
        username='test_user',
        defaults={'email': 'test@example.com'}
    )
    
    # Test 1: Create borrower with structured address data
    print("\n📝 Test 1: Creating borrower with structured address data")
    
    borrower_data = {
        'first_name': 'John',
        'last_name': 'Doe',
        'email': 'john.doe@example.com',
        'phone': '+61 400 123 456',
        
        # Structured address data
        'address': {
            'street': '123 Main Street',
            'city': 'Sydney',
            'state': 'NSW',
            'postal_code': '2000',
            'country': 'Australia'
        },
        'mailing_address': 'PO Box 456, Sydney NSW 2001',
        
        # Employment fields
        'employment_type': 'full_time',
        'employer_name': 'Tech Corp Pty Ltd',
        'job_title': 'Software Engineer',
        'annual_income': 95000.00,
        'employment_duration': 24,
        'employer_address': '456 Business Ave, Sydney NSW 2000',
        
        # Financial fields
        'other_income': 5000.00,
        'monthly_expenses': 3500.00,
    }
    
    # Create borrower using serializer
    context = {'request': type('MockRequest', (), {'user': test_user})()}
    serializer = BorrowerSerializer(data=borrower_data, context={'request': context})
    
    if serializer.is_valid():
        borrower = serializer.save()
        print(f"✅ Borrower created successfully: {borrower.id}")
        
        # Verify data was saved
        print(f"   📍 Residential Address: {borrower.residential_address}")
        print(f"   📮 Mailing Address: {borrower.mailing_address}")
        print(f"   💼 Employer: {borrower.employer_name}")
        print(f"   👔 Job Title: {borrower.job_title}")
        print(f"   💰 Annual Income: {borrower.annual_income}")
        print(f"   📅 Employment Duration: {borrower.employment_duration} months")
        print(f"   🏢 Employer Address: {borrower.employer_address}")
        print(f"   💵 Other Income: {borrower.other_income}")
        print(f"   📊 Monthly Expenses: {borrower.monthly_expenses}")
        
        # Verify the residential_address was properly formatted from structured data
        expected_address = "123 Main Street, Sydney, NSW, 2000, Australia"
        if borrower.residential_address == expected_address:
            print(f"   ✅ Address properly formatted: {borrower.residential_address}")
        else:
            print(f"   ⚠️  Address formatting issue. Expected: {expected_address}, Got: {borrower.residential_address}")
        
    else:
        print(f"❌ Serializer validation failed: {serializer.errors}")
        return False
    
    # Test 2: Retrieve and serialize borrower data
    print("\n📖 Test 2: Retrieving borrower data via serializer")
    
    retrieved_serializer = BorrowerSerializer(borrower)
    retrieved_data = retrieved_serializer.data
    
    # Check address info (should be properly parsed back)
    address_info = retrieved_data.get('address', {})
    print(f"   📍 Address Info: {address_info}")
    
    # Check employment info  
    employment_info = retrieved_data.get('employment_info', {})
    print(f"   💼 Employment Info: {employment_info}")
    
    # Verify structured address parsing worked
    expected_street = "123 Main Street"
    expected_city = "Sydney"
    expected_state = "NSW"
    if (address_info.get('street') == expected_street and 
        address_info.get('city') == expected_city and 
        address_info.get('state') == expected_state):
        print(f"   ✅ Address parsing successful")
    else:
        print(f"   ⚠️  Address parsing issue")
    
    # Test 3: Update borrower with nested data
    print("\n🔄 Test 3: Updating borrower with nested address/employment data")
    
    update_data = {
        'address': {
            'street': '789 Updated Street, Melbourne VIC 3000'
        },
        'employment_info': {
            'employer': 'New Company Ltd',
            'position': 'Senior Developer',
            'income': 110000.00,
            'years_employed': 36
        }
    }
    
    update_serializer = BorrowerSerializer(borrower, data=update_data, partial=True)
    if update_serializer.is_valid():
        updated_borrower = update_serializer.save()
        print(f"✅ Borrower updated successfully")
        
        # Verify nested data was properly saved to model fields
        print(f"   📍 Updated Residential Address: {updated_borrower.residential_address}")
        print(f"   💼 Updated Employer: {updated_borrower.employer_name}")
        print(f"   👔 Updated Job Title: {updated_borrower.job_title}")
        print(f"   💰 Updated Annual Income: {updated_borrower.annual_income}")
        print(f"   📅 Updated Employment Duration: {updated_borrower.employment_duration}")
        
    else:
        print(f"❌ Update serializer validation failed: {update_serializer.errors}")
        return False
    
    # Test 4: Final verification - serialize updated data
    print("\n🔍 Test 4: Final verification - serialize updated data")
    
    final_serializer = BorrowerSerializer(updated_borrower)
    final_data = final_serializer.data
    
    final_address = final_data.get('address', {})
    final_employment = final_data.get('employment_info', {})
    
    print(f"   📍 Final Address: {final_address}")
    print(f"   💼 Final Employment: {final_employment}")
    
    # Check that nested data reflects the model updates
    address_matches = final_address.get('street') == updated_borrower.residential_address
    employer_matches = final_employment.get('employer') == updated_borrower.employer_name
    position_matches = final_employment.get('position') == updated_borrower.job_title
    income_matches = final_employment.get('income') == updated_borrower.annual_income
    
    print(f"\n✅ Address data consistency: {'PASS' if address_matches else 'FAIL'}")
    print(f"✅ Employer data consistency: {'PASS' if employer_matches else 'FAIL'}")
    print(f"✅ Position data consistency: {'PASS' if position_matches else 'FAIL'}")
    print(f"✅ Income data consistency: {'PASS' if income_matches else 'FAIL'}")
    
    # Cleanup
    borrower.delete()
    if created:
        test_user.delete()
    
    all_tests_passed = all([address_matches, employer_matches, position_matches, income_matches])
    
    print(f"\n{'🎉 ALL TESTS PASSED!' if all_tests_passed else '❌ SOME TESTS FAILED!'}")
    print("=" * 50)
    
    return all_tests_passed

if __name__ == '__main__':
    success = test_borrower_address_employment_fix()
    sys.exit(0 if success else 1) 