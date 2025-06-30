"""
Tests for PDF Field Mapping Utility

This module tests the PDF field mapping function to ensure it correctly
maps application data to PDF field IDs according to the specification.
"""

import pytest
from decimal import Decimal
from applications.utils.pdf_field_mapping import generate_pdf_field_mapping_from_json


class TestPDFFieldMapping:
    """Test the PDF field mapping function."""
    
    def test_empty_data_returns_empty_mapping(self):
        """Test that empty data returns empty mapping."""
        data = {}
        mapping = generate_pdf_field_mapping_from_json(data)
        assert isinstance(mapping, dict)
        assert len(mapping) == 0
    
    def test_company_borrower_details_mapping(self):
        """Test company borrower details mapping."""
        data = {
            'company_borrowers': [{
                'company_name': 'Test Company Pty Ltd',
                'company_abn': '12345678901',
                'industry_type': 'Technology',
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
                'registered_address_postcode': '2000'
            }]
        }
        
        mapping = generate_pdf_field_mapping_from_json(data)
        
        # Company basic details
        assert mapping['text1'] == 'Test Company Pty Ltd'
        assert mapping['text2'] == '12345678901'
        assert mapping['text3'] == 'Technology'
        assert mapping['text4'] == '0412345678'
        assert mapping['text5'] == '500,000.00'
        
        # Trustee information
        assert mapping['checkbox20'] is True
        assert mapping['checkbox21'] is False
        assert mapping['checkbox22'] is False
        assert mapping['checkbox23'] is True
        assert mapping['text6'] == 'John Smith'
        
        # Director details
        assert mapping['text7'] == 'John Smith'
        assert mapping['checkbox24'] is True
        assert mapping['checkbox25'] is True
        assert mapping['checkbox26'] is False
        
        # Director ID (split into individual digits)
        assert mapping['text8'] == '1'
        assert mapping['text9'] == '2'
        assert mapping['text10'] == '3'
        assert mapping['text11'] == '4'
        assert mapping['text12'] == '5'
        assert mapping['text13'] == '6'
        assert mapping['text14'] == '7'
        assert mapping['text15'] == '8'
        assert mapping['text16'] == '9'
        assert mapping['text17'] == '0'
        assert mapping['text18'] == '1'
        assert mapping['text19'] == '2'
        
        # Registered address
        assert mapping['text43'] == 'Unit 1'
        assert mapping['text44'] == '123'
        assert mapping['text45'] == 'Main Street'
        assert mapping['text46'] == 'Sydney'
        assert mapping['text47'] == 'NSW'
        assert mapping['text48'] == '2000'
    
    def test_company_assets_liabilities_mapping(self):
        """Test company assets and liabilities mapping."""
        data = {
            'company_borrowers': [{
                'assets': [
                    {
                        'asset_type': 'property',
                        'address': '123 Property St',
                        'value': '800000.00',
                        'amount_owing': '400000.00',
                        'to_be_refinanced': True
                    },
                    {
                        'asset_type': 'vehicle',
                        'value': '50000.00',
                        'amount_owing': '20000.00',
                        'to_be_refinanced': False
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
            }]
        }
        
        mapping = generate_pdf_field_mapping_from_json(data)
        
        # Property assets
        assert mapping['text49'] == '123 Property St'
        assert mapping['text50'] == '800,000.00'
        assert mapping['text51'] == '400,000.00'
        assert mapping['checkbox52'] is True
        
        # Vehicle assets
        assert mapping['text65'] == '50,000.00'
        assert mapping['text66'] == '20,000.00'
        assert mapping['checkbox86'] is False
        
        # Savings assets
        assert mapping['text67'] == '100,000.00'
        assert mapping['text68'] == '0.00'
        assert mapping['checkbox87'] is False
        
        # Credit card liabilities
        assert mapping['text71'] == '15,000.00'
        assert mapping['text72'] == '15,000.00'
        assert mapping['checkbox89'] is True
    
    def test_solvency_enquiries_mapping(self):
        """Test solvency enquiries mapping."""
        data = {
            'application': {
                'has_pending_litigation': True,
                'has_unsatisfied_judgements': False,
                'has_been_bankrupt': True,
                'has_been_refused_credit': False,
                'has_outstanding_ato_debt': True,
                'has_outstanding_tax_returns': False,
                'has_payment_arrangements': True
            }
        }
        
        mapping = generate_pdf_field_mapping_from_json(data)
        
        # Solvency questions
        assert mapping['checkbox92'] is True
        assert mapping['checkbox93'] is False
        assert mapping['checkbox94'] is False
        assert mapping['checkbox95'] is True
        assert mapping['checkbox96'] is True
        assert mapping['checkbox97'] is False
        assert mapping['checkbox98'] is False
        assert mapping['checkbox99'] is True
        assert mapping['checkbox100'] is True
        assert mapping['checkbox101'] is False
        assert mapping['checkbox102'] is False
        assert mapping['checkbox103'] is True
        assert mapping['checkbox104'] is True
        assert mapping['checkbox105'] is False
    
    def test_individual_details_mapping(self):
        """Test individual borrower/guarantor details mapping."""
        data = {
            'borrowers': [{
                'title': 'Mr',
                'first_name': 'John',
                'last_name': 'Doe',
                'date_of_birth': '1985-05-15',
                'drivers_licence_no': 'DL123456',
                'home_phone': '0298765432',
                'mobile': '0412345678',
                'email': 'john.doe@email.com',
                'address_unit': 'Unit 2',
                'address_street_no': '456',
                'address_street_name': 'Oak Avenue',
                'address_suburb': 'Melbourne',
                'address_state': 'VIC',
                'address_postcode': '3000',
                'occupation': 'Engineer',
                'employer_name': 'Tech Corp',
                'employment_type': 'full_time',
                'annual_income': '120000.00'
            }]
        }
        
        mapping = generate_pdf_field_mapping_from_json(data)
        
        # Personal details
        assert mapping['text106'] == 'Mr'
        assert mapping['text107'] == 'John'
        assert mapping['text108'] == 'Doe'
        assert mapping['text109'] == '15'
        assert mapping['text110'] == '05'
        assert mapping['text111'] == '1985'
        assert mapping['text112'] == 'DL123456'
        assert mapping['text113'] == '0298765432'
        assert mapping['text114'] == '0412345678'
        assert mapping['text115'] == 'john.doe@email.com'
        
        # Address
        assert mapping['text116'] == 'Unit 2'
        assert mapping['text117'] == '456'
        assert mapping['text118'] == 'Oak Avenue'
        assert mapping['text119'] == 'Melbourne'
        assert mapping['text120'] == 'VIC'
        assert mapping['text121'] == '3000'
        
        # Employment
        assert mapping['text122'] == 'Engineer'
        assert mapping['text123'] == 'Tech Corp'
        assert mapping['checkbox124'] is True
        assert mapping['checkbox125'] is False
        assert mapping['checkbox126'] is False
        assert mapping['checkbox127'] is False
        assert mapping['text128'] == '120,000.00'
    
    def test_guarantor_assets_liabilities_mapping(self):
        """Test guarantor assets and liabilities mapping."""
        data = {
            'guarantors': [{
                'assets': [
                    {
                        'asset_type': 'property',
                        'address': '789 Guarantor St',
                        'value': '600000.00',
                        'amount_owing': '300000.00',
                        'bg_type': 'BG1'
                    },
                    {
                        'asset_type': 'vehicle',
                        'value': '30000.00',
                        'amount_owing': '10000.00',
                        'bg_type': 'BG2'
                    }
                ],
                'liabilities': [
                    {
                        'liability_type': 'credit_card',
                        'amount': '8000.00',
                        'bg_type': 'BG1'
                    }
                ]
            }]
        }
        
        mapping = generate_pdf_field_mapping_from_json(data)
        
        # Property assets
        assert mapping['text152'] == '789 Guarantor St'
        assert mapping['text153'] == '600,000.00'
        assert mapping['text154'] == '300,000.00'
        assert mapping['checkbox155'] is True
        assert mapping['checkbox156'] is False
        
        # Vehicle assets
        assert mapping['text166'] == '30,000.00'
        assert mapping['text167'] == '10,000.00'
        assert mapping['checkbox186'] is False
        assert mapping['checkbox187'] is True
        
        # Credit card liabilities
        assert mapping['text172'] == '8,000.00'
        assert mapping['text173'] == '8,000.00'
        assert mapping['checkbox192'] is True
        assert mapping['checkbox193'] is False
    
    def test_security_properties_mapping(self):
        """Test security properties mapping."""
        data = {
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
            }]
        }
        
        mapping = generate_pdf_field_mapping_from_json(data)
        
        # Address
        assert mapping['text198'] == 'Unit 3'
        assert mapping['text199'] == '789'
        assert mapping['text200'] == 'Security Street'
        assert mapping['text201'] == 'Brisbane'
        assert mapping['text202'] == 'QLD'
        assert mapping['text203'] == '4000'
        
        # Mortgage details
        assert mapping['text204'] == '500,000.00'
        assert mapping['text205'] == '100,000.00'
        assert mapping['text206'] == '450,000.00'
        assert mapping['text207'] == '90,000.00'
        
        # Valuation
        assert mapping['checkbox208'] is True
        assert mapping['text210'] == '900,000.00'
        assert mapping['checkbox209'] is True
        assert mapping['text211'] == '750,000.00'
        
        # Property type
        assert mapping['checkbox212'] is True  # Residential
        assert mapping['checkbox213'] is False  # Commercial
        assert mapping['checkbox214'] is False  # Rural
        assert mapping['checkbox215'] is False  # Industrial
        assert mapping['checkbox216'] is False  # Vacant Land
        assert mapping['checkbox217'] is False  # Other
        
        # Description
        assert mapping['text219'] == '4'
        assert mapping['text220'] == '2'
        assert mapping['text221'] == '2'
        assert mapping['text222'] == '200.00'
        assert mapping['text223'] == '500.00'
        
        # Property features
        assert mapping['checkbox224'] is True  # Single Story
        assert mapping['checkbox225'] is False  # Double Story
        assert mapping['checkbox226'] is True  # Garage
        assert mapping['checkbox227'] is False  # Carport
        assert mapping['checkbox228'] is True  # Off-Street
        
        # Owner type
        assert mapping['checkbox229'] is True  # Owner Occupied
        assert mapping['checkbox230'] is False  # Investment Property
    
    def test_loan_details_mapping(self):
        """Test loan details and purpose mapping."""
        data = {
            'application': {
                'loan_amount': '750000.00',
                'loan_term': 24,
                'estimated_settlement_date': '2024-06-15',
                'interest_rate': '9.50',
                'loan_purpose': 'purchase',
                'additional_comments': 'Property purchase for investment',
                'has_other_credit_providers': True,
                'other_credit_providers_details': 'Applied to ABC Bank',
                'exit_strategy': 'refinance',
                'exit_strategy_details': 'Refinance to conventional lender'
            },
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
        
        mapping = generate_pdf_field_mapping_from_json(data)
        
        # Loan details
        assert mapping['text297'] == '750,000.00'
        assert mapping['text298'] == '24'
        assert mapping['text299'] == '15'
        assert mapping['text300'] == '06'
        assert mapping['text301'] == '2024'
        assert mapping['text302'] == '9.50'
        
        # Loan purpose
        assert mapping['checkbox303'] is True  # Purchase
        assert mapping['checkbox304'] is False  # Seed Capital
        assert mapping['checkbox305'] is False  # Settlement Shortfall
        assert mapping['checkbox306'] is False  # Equity Venture
        assert mapping['checkbox307'] is False  # Cash Out
        assert mapping['checkbox308'] is False  # Refinance
        assert mapping['checkbox309'] is False  # Construction
        assert mapping['checkbox310'] is False  # Payout Existing Debt
        assert mapping['checkbox311'] is False  # Other
        
        assert mapping['text312'] == 'Property purchase for investment'
        
        # Other submissions
        assert mapping['checkbox313'] is True
        assert mapping['checkbox314'] is False
        assert mapping['text315'] == 'Applied to ABC Bank'
        
        # Loan requirements
        assert mapping['text316'] == 'Property purchase'
        assert mapping['text317'] == '700,000.00'
        assert mapping['text318'] == 'Legal fees'
        assert mapping['text319'] == '25,000.00'
        assert mapping['text320'] == 'Stamp duty'
        assert mapping['text321'] == '25,000.00'
        
        # Total amount
        assert mapping['text328'] == '750,000.00'
        
        # Exit strategy
        assert mapping['checkbox329'] is True  # Refinance
        assert mapping['checkbox330'] is False  # Sale of Security
        assert mapping['checkbox331'] is False  # Cash-flow
        assert mapping['checkbox332'] is False  # Other
        
        assert mapping['text333'] == 'Refinance to conventional lender'
    
    def test_multiple_security_properties_mapping(self):
        """Test mapping of multiple security properties."""
        data = {
            'security_properties': [
                {
                    'address_street_no': '123',
                    'address_street_name': 'First Property',
                    'address_suburb': 'Sydney',
                    'address_state': 'NSW',
                    'address_postcode': '2000',
                    'property_type': 'residential',
                    'occupancy': 'owner_occupied'
                },
                {
                    'address_street_no': '456',
                    'address_street_name': 'Second Property',
                    'address_suburb': 'Melbourne',
                    'address_state': 'VIC',
                    'address_postcode': '3000',
                    'property_type': 'commercial',
                    'occupancy': 'investment'
                },
                {
                    'address_street_no': '789',
                    'address_street_name': 'Third Property',
                    'address_suburb': 'Brisbane',
                    'address_state': 'QLD',
                    'address_postcode': '4000',
                    'property_type': 'rural',
                    'occupancy': 'investment'
                }
            ]
        }
        
        mapping = generate_pdf_field_mapping_from_json(data)
        
        # Property 1 (base 198)
        assert mapping['text199'] == '123'
        assert mapping['text200'] == 'First Property'
        assert mapping['text201'] == 'Sydney'
        assert mapping['text202'] == 'NSW'
        assert mapping['text203'] == '2000'
        assert mapping['checkbox212'] is True  # Residential
        assert mapping['checkbox229'] is True  # Owner Occupied
        
        # Property 2 (base 231)
        assert mapping['text232'] == '456'
        assert mapping['text233'] == 'Second Property'
        assert mapping['text234'] == 'Melbourne'
        assert mapping['text235'] == 'VIC'
        assert mapping['text236'] == '3000'
        assert mapping['checkbox246'] is True  # Commercial
        assert mapping['checkbox263'] is True  # Investment Property
        
        # Property 3 (base 264)
        assert mapping['text265'] == '789'
        assert mapping['text266'] == 'Third Property'
        assert mapping['text267'] == 'Brisbane'
        assert mapping['text268'] == 'QLD'
        assert mapping['text269'] == '4000'
        assert mapping['checkbox280'] is True  # Rural
        assert mapping['checkbox296'] is True  # Investment Property
    
    def test_currency_formatting(self):
        """Test currency formatting for various input types."""
        data = {
            'application': {
                'loan_amount': Decimal('1234567.89'),
                'interest_rate': Decimal('9.75')
            },
            'borrowers': [{
                'annual_income': '85000.50'
            }],
            'company_borrowers': [{
                'annual_company_income': 500000
            }]
        }
        
        mapping = generate_pdf_field_mapping_from_json(data)
        
        assert mapping['text297'] == '1,234,567.89'
        assert mapping['text302'] == '9.75'
        assert mapping['text128'] == '85,000.50'
        assert mapping['text5'] == '500,000.00'
    
    def test_date_formatting(self):
        """Test date formatting for various date inputs."""
        data = {
            'borrowers': [{
                'date_of_birth': '1990-12-25'
            }],
            'application': {
                'estimated_settlement_date': '2024-03-01'
            }
        }
        
        mapping = generate_pdf_field_mapping_from_json(data)
        
        # Date of birth
        assert mapping['text109'] == '25'
        assert mapping['text110'] == '12'
        assert mapping['text111'] == '1990'
        
        # Settlement date
        assert mapping['text299'] == '01'
        assert mapping['text300'] == '03'
        assert mapping['text301'] == '2024'
    
    def test_empty_and_null_values(self):
        """Test handling of empty and null values."""
        data = {
            'borrowers': [{
                'first_name': '',
                'last_name': None,
                'date_of_birth': '',
                'annual_income': None
            }],
            'application': {
                'loan_amount': '',
                'interest_rate': None
            }
        }
        
        mapping = generate_pdf_field_mapping_from_json(data)
        
        # Should handle empty/null values gracefully
        assert mapping['text107'] == ''
        assert mapping['text108'] == ''
        assert mapping['text109'] == ''
        assert mapping['text110'] == ''
        assert mapping['text111'] == ''
        assert mapping['text128'] == ''
        assert mapping['text297'] == ''
        assert mapping['text302'] == ''
    
    def test_error_handling(self):
        """Test error handling with malformed data."""
        # Test with non-dictionary data
        mapping = generate_pdf_field_mapping_from_json("invalid data")
        assert isinstance(mapping, dict)
        assert len(mapping) == 0
        
        # Test with missing nested data
        data = {
            'borrowers': None,
            'company_borrowers': "not a list",
            'application': []
        }
        
        mapping = generate_pdf_field_mapping_from_json(data)
        assert isinstance(mapping, dict)
        # Should not raise exceptions, just return empty values 