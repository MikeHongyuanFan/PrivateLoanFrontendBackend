"""
Tests for PDF Filler Utility

This module tests the PDF filler function to ensure it correctly
fills PDF forms with application data.
"""

import pytest
import os
import tempfile
from decimal import Decimal
from django.test import TestCase
from applications.utils.pdf_filler import (
    fill_pdf_form, 
    fill_pdf_with_mapping, 
    get_pdf_template_path,
    validate_pdf_fields,
    get_field_mapping_summary
)
from applications.utils.pdf_field_mapping import generate_pdf_field_mapping_from_json


class TestPDFFiller(TestCase):
    """Test the PDF filler function."""
    
    def setUp(self):
        """Set up test data."""
        self.test_data = {
            'application': {
                'loan_amount': '750000.00',
                'loan_term': 24,
                'estimated_settlement_date': '2024-06-15',
                'interest_rate': '9.50',
                'loan_purpose': 'purchase',
                'additional_comments': 'Test application',
                'has_pending_litigation': False,
                'has_unsatisfied_judgements': False,
                'has_been_bankrupt': False,
                'has_been_refused_credit': False,
                'has_outstanding_ato_debt': False,
                'has_outstanding_tax_returns': False,
                'has_payment_arrangements': False
            },
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
            }]
        }
    
    def test_get_field_mapping_summary(self):
        """Test field mapping summary function."""
        field_mapping = generate_pdf_field_mapping_from_json(self.test_data)
        summary = get_field_mapping_summary(field_mapping)
        
        assert 'total_fields' in summary
        assert 'text_fields_count' in summary
        assert 'checkbox_fields_count' in summary
        assert 'filled_text_fields' in summary
        assert 'checked_checkboxes' in summary
        assert 'sample_text_fields' in summary
        assert 'sample_checkbox_fields' in summary
        
        assert summary['total_fields'] > 0
        assert summary['text_fields_count'] > 0
        assert summary['checkbox_fields_count'] > 0
    
    def test_validate_pdf_fields(self):
        """Test PDF field validation."""
        field_mapping = generate_pdf_field_mapping_from_json(self.test_data)
        missing_fields = validate_pdf_fields(field_mapping)
        
        # Should have some required fields filled
        assert len(missing_fields) < 6  # Not all required fields may be present
    
    def test_get_pdf_template_path_error(self):
        """Test template path error handling."""
        with pytest.raises(FileNotFoundError):
            get_pdf_template_path('nonexistent_template')
    
    def test_fill_pdf_with_mapping_without_template(self):
        """Test PDF filling without template file."""
        field_mapping = generate_pdf_field_mapping_from_json(self.test_data)
        
        with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as tmp_file:
            tmp_path = tmp_file.name
        
        try:
            with pytest.raises(FileNotFoundError):
                fill_pdf_with_mapping('/nonexistent/template.pdf', field_mapping, tmp_path)
        finally:
            if os.path.exists(tmp_path):
                os.unlink(tmp_path)
    
    def test_field_mapping_generation(self):
        """Test that field mapping is generated correctly."""
        field_mapping = generate_pdf_field_mapping_from_json(self.test_data)
        
        # Should have text fields
        assert any(k.startswith('text') for k in field_mapping.keys())
        
        # Should have checkbox fields
        assert any(k.startswith('checkbox') for k in field_mapping.keys())
        
        # Should have specific expected fields
        assert 'text297' in field_mapping  # Loan amount
        assert 'text298' in field_mapping  # Loan term
        assert 'text107' in field_mapping  # First name
        assert 'text108' in field_mapping  # Last name
    
    def test_empty_data_handling(self):
        """Test handling of empty data."""
        empty_data = {}
        field_mapping = generate_pdf_field_mapping_from_json(empty_data)
        
        # Should return empty mapping
        assert isinstance(field_mapping, dict)
        assert len(field_mapping) == 0
    
    def test_malformed_data_handling(self):
        """Test handling of malformed data."""
        malformed_data = "not a dictionary"
        field_mapping = generate_pdf_field_mapping_from_json(malformed_data)
        
        # Should handle gracefully
        assert isinstance(field_mapping, dict)
        assert len(field_mapping) == 0 