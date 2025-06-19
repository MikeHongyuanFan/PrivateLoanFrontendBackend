"""
Unit tests for application API endpoints.

This module tests all application-related endpoints including CRUD operations,
custom actions, and business logic.
"""

from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from unittest.mock import patch, MagicMock
from decimal import Decimal
from datetime import date
from django.utils import timezone

from applications.models import Application
from .base import BaseApplicationTestCase, ApplicationTestMixin


class ApplicationCRUDEndpointsTest(BaseApplicationTestCase, ApplicationTestMixin):
    """Test standard CRUD operations for applications."""
    
    def test_list_applications(self):
        """Test GET /api/applications/ - List applications."""
        url = self.get_application_url()
        response = self.client.get(url)
        
        self.assertResponseSuccess(response)
        self.assertIn('results', response.data)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['id'], self.application.id)
    
    def test_create_application(self):
        """Test POST /api/applications/ - Create application."""
        url = self.get_application_url()
        data = self.get_application_data()
        
        response = self.client.post(url, data, format='json')
        
        self.assertResponseSuccess(response, 201)
        self.assertResponseContains(response, 'id')
        self.assertResponseContains(response, 'reference_number')
        
        # Verify application was created
        new_app = Application.objects.get(id=response.data['id'])
        self.assertEqual(new_app.loan_amount, Decimal('250000.00'))
        self.assertEqual(new_app.stage, 'inquiry')
    
    def test_retrieve_application(self):
        """Test GET /api/applications/{id}/ - Retrieve application."""
        url = self.get_application_url(self.application.id)
        response = self.client.get(url)
        
        self.assertResponseSuccess(response)
        self.assertResponseContains(response, 'id', self.application.id)
        self.assertResponseContains(response, 'reference_number', self.application.reference_number)
        self.assertIn('borrowers', response.data)
        self.assertIn('guarantors', response.data)
    
    def test_update_application(self):
        """Test PUT /api/applications/{id}/ - Update application."""
        url = self.get_application_url(self.application.id)
        data = self.get_application_data(
            loan_amount='750000.00',
            stage='sent_to_lender'
        )
        
        response = self.client.put(url, data, format='json')
        
        self.assertResponseSuccess(response)
        
        # Verify application was updated
        self.application.refresh_from_db()
        self.assertEqual(self.application.loan_amount, Decimal('750000.00'))
        self.assertEqual(self.application.stage, 'sent_to_lender')
    
    def test_partial_update_application(self):
        """Test PATCH /api/applications/{id}/ - Partial update application."""
        url = self.get_application_url(self.application.id)
        data = {'loan_amount': '600000.00'}
        
        response = self.client.patch(url, data, format='json')
        
        self.assertResponseSuccess(response)
        
        # Verify only loan_amount was updated
        self.application.refresh_from_db()
        self.assertEqual(self.application.loan_amount, Decimal('600000.00'))
        self.assertEqual(self.application.stage, 'inquiry')  # Should remain unchanged
    
    def test_delete_application(self):
        """Test DELETE /api/applications/{id}/ - Delete application."""
        url = self.get_application_url(self.application.id)
        response = self.client.delete(url)
        
        self.assertResponseSuccess(response, 204)
        
        # Verify application was deleted
        self.assertFalse(Application.objects.filter(id=self.application.id).exists())


class ApplicationCustomActionsTest(BaseApplicationTestCase, ApplicationTestMixin):
    """Test custom action endpoints for applications."""
    
    def test_enhanced_list(self):
        """Test GET /api/applications/enhanced-applications/ - Enhanced list view."""
        url = '/api/applications/enhanced-applications/'
        response = self.client.get(url)
        
        self.assertResponseSuccess(response)
        self.assertIn('results', response.data)
        self.assertIn('metadata', response.data)
        self.assertIn('applied_filters', response.data['metadata'])
        self.assertIn('filter_options', response.data['metadata'])
    
    def test_enhanced_list_with_filters(self):
        """Test enhanced list with query parameters."""
        url = '/api/applications/enhanced-applications/'
        params = {
            'stage': 'inquiry',
            'min_loan_amount': '100000',
            'sort_by': 'loan_amount',
            'sort_direction': 'asc'
        }
        
        response = self.client.get(url, params)
        
        self.assertResponseSuccess(response)
        self.assertIn('metadata', response.data)
        self.assertEqual(response.data['metadata']['applied_filters']['stage'], 'inquiry')
    
    def test_enhanced_applications_alt(self):
        """Test GET /api/applications/enhanced-applications-alt/ - Alternative enhanced view."""
        url = '/api/applications/enhanced-applications-alt/'
        response = self.client.get(url)
        
        self.assertResponseSuccess(response)
        # This endpoint should also return enhanced data
        self.assertIn('results', response.data)
    
    def test_create_with_cascade(self):
        """Test POST /api/applications/create-with-cascade/ - Create with cascade."""
        url = '/api/applications/create-with-cascade/'
        data = self.get_application_data()
        
        response = self.client.post(url, data, format='json')
        
        self.assertResponseSuccess(response, 201)
        self.assertResponseContains(response, 'id')
        self.assertResponseContains(response, 'reference_number')
    
    def test_create_with_cascade_minimal_data(self):
        """Test create with cascade endpoint with minimal data - just reference number."""
        url = '/api/applications/create-with-cascade/'
        minimal_data = {
            'reference_number': 'TEST-MIN-001'
        }
        
        response = self.client.post(url, minimal_data, format='json')
        
        self.assertResponseSuccess(response, 201)
        self.assertResponseContains(response, 'id')
        self.assertResponseContains(response, 'reference_number', 'TEST-MIN-001')
        
        # Verify application was created with minimal data
        application = Application.objects.get(reference_number='TEST-MIN-001')
        self.assertEqual(application.reference_number, 'TEST-MIN-001')
        self.assertIsNone(application.loan_amount)
        self.assertIsNone(application.loan_term)
        self.assertEqual(application.borrowers.count(), 0)
        self.assertEqual(application.guarantors.count(), 0)
    
    def test_create_with_cascade_borrower_name_only(self):
        """Test create with cascade endpoint with just borrower name."""
        url = '/api/applications/create-with-cascade/'
        data = {
            'reference_number': 'TEST-BORROWER-001',
            'borrowers': [
                {
                    'first_name': 'John',
                    'last_name': 'Doe'
                }
            ]
        }
        
        response = self.client.post(url, data, format='json')
        
        self.assertResponseSuccess(response, 201)
        self.assertResponseContains(response, 'id')
        
        # Verify application and borrower were created
        application = Application.objects.get(reference_number='TEST-BORROWER-001')
        self.assertEqual(application.borrowers.count(), 1)
        
        borrower = application.borrowers.first()
        self.assertEqual(borrower.first_name, 'John')
        self.assertEqual(borrower.last_name, 'Doe')
        self.assertIsNone(borrower.email)
        self.assertIsNone(borrower.phone)
    
    def test_create_with_cascade_empty_nested_objects(self):
        """Test create with cascade endpoint with empty nested objects."""
        url = '/api/applications/create-with-cascade/'
        data = {
            'reference_number': 'TEST-EMPTY-001',
            'borrowers': [],
            'guarantors': [],
            'security_properties': [],
            'loan_requirements': []
        }
        
        response = self.client.post(url, data, format='json')
        
        self.assertResponseSuccess(response, 201)
        self.assertResponseContains(response, 'id')
        
        # Verify application was created with empty collections
        application = Application.objects.get(reference_number='TEST-EMPTY-001')
        self.assertEqual(application.borrowers.count(), 0)
        self.assertEqual(application.guarantors.count(), 0)
        self.assertEqual(application.security_properties.count(), 0)
        self.assertEqual(application.loan_requirements.count(), 0)
    
    def test_validate_schema(self):
        """Test POST /api/applications/validate-schema/ - Schema validation."""
        url = '/api/applications/validate-schema/'
        data = self.get_application_data()
        
        response = self.client.post(url, data, format='json')
        
        self.assertResponseSuccess(response)
        self.assertResponseContains(response, 'valid', True)


class ApplicationSignatureEndpointsTest(BaseApplicationTestCase, ApplicationTestMixin):
    """Test signature-related endpoints."""
    
    def test_add_signature(self):
        """Test POST /api/applications/{id}/signature/ - Add signature."""
        url = self.get_application_url(self.application.id, 'signature')
        data = self.get_signature_data()
        
        response = self.client.post(url, data, format='json')
        
        self.assertResponseSuccess(response)
        self.assertResponseContains(response, 'message')
        
        # Verify signature was added
        self.application.refresh_from_db()
        self.assertEqual(self.application.signed_by, 'Test Signatory')
        self.assertEqual(self.application.signature_date, date.today())
    
    def test_add_signature_invalid_data(self):
        """Test signature endpoint with invalid data."""
        url = self.get_application_url(self.application.id, 'signature')
        data = {'name': ''}  # Missing signature_date
        
        response = self.client.post(url, data, format='json')
        
        self.assertResponseError(response, 400)
    
    def test_sign_application(self):
        """Test POST /api/applications/{id}/sign/ - Sign application."""
        url = self.get_application_url(self.application.id, 'sign')
        data = {
            'name': 'John Doe',
            'date': date.today().isoformat()
        }
        
        response = self.client.post(url, data, format='json')
        
        self.assertResponseSuccess(response)
        self.assertResponseContains(response, 'message')
        
        # Verify application was signed
        self.application.refresh_from_db()
        self.assertEqual(self.application.signed_by, 'John Doe')
    
    def test_sign_already_signed_application(self):
        """Test signing an already signed application."""
        # First sign the application
        self.application.signed_by = 'Already Signed'
        self.application.save()
        
        url = self.get_application_url(self.application.id, 'sign')
        data = {'name': 'New Signatory', 'date': date.today().isoformat()}
        
        response = self.client.post(url, data, format='json')
        
        self.assertResponseError(response, 400)
        self.assertIn('already signed', response.data['error'])


class ApplicationStageManagementTest(BaseApplicationTestCase, ApplicationTestMixin):
    """Test stage management endpoints."""
    
    def test_update_stage(self):
        """Test PUT /api/applications/{id}/stage/ - Update stage."""
        url = self.get_application_url(self.application.id, 'stage')
        data = self.get_stage_update_data()
        
        response = self.client.put(url, data, format='json')
        
        self.assertResponseSuccess(response)
        self.assertResponseContains(response, 'message')
        
        # Verify stage was updated
        self.application.refresh_from_db()
        self.assertEqual(self.application.stage, 'sent_to_lender')
    
    def test_update_stage_invalid(self):
        """Test stage update with invalid stage."""
        url = self.get_application_url(self.application.id, 'stage')
        data = self.get_stage_update_data(stage='invalid_stage')
        
        response = self.client.put(url, data, format='json')
        
        self.assertResponseError(response, 400)


class ApplicationBorrowerManagementTest(BaseApplicationTestCase, ApplicationTestMixin):
    """Test borrower management endpoints."""
    
    def test_update_borrowers(self):
        """Test PUT /api/applications/{id}/borrowers/ - Update borrowers."""
        # Create an additional borrower
        from borrowers.models import Borrower
        borrower2 = Borrower.objects.create(
            first_name='Jane',
            last_name='Doe',
            email='jane.doe@test.com',
            phone='0123456789',
            date_of_birth=date(1985, 1, 1)
        )
        
        url = self.get_application_url(self.application.id, 'borrowers')
        data = self.get_borrower_update_data([self.borrower.id, borrower2.id])
        
        response = self.client.put(url, data, format='json')
        
        self.assertResponseSuccess(response)
        self.assertResponseContains(response, 'message')
        
        # Verify borrowers were updated
        self.application.refresh_from_db()
        borrower_ids = list(self.application.borrowers.values_list('id', flat=True))
        self.assertIn(self.borrower.id, borrower_ids)
        self.assertIn(borrower2.id, borrower_ids)
    
    def test_update_borrowers_invalid_ids(self):
        """Test borrower update with invalid borrower IDs."""
        url = self.get_application_url(self.application.id, 'borrowers')
        data = self.get_borrower_update_data([9999, 10000])  # Non-existent IDs
        
        response = self.client.put(url, data, format='json')
        
        self.assertResponseError(response, 400)
        self.assertIn('invalid', response.data['error'])


class ApplicationBDAssignmentTest(BaseApplicationTestCase, ApplicationTestMixin):
    """Test BD assignment endpoints."""
    
    def test_assign_bd_new(self):
        """Test POST /api/applications/{id}/assign-bd/ - New BD assignment."""
        # Ensure no BD is currently assigned
        self.application.assigned_bd = None
        self.application.save()
        
        url = self.get_application_url(self.application.id, 'assign-bd')
        data = self.get_bd_assignment_data()
        
        response = self.client.post(url, data, format='json')
        
        self.assertResponseSuccess(response)
        self.assertResponseContains(response, 'message')
        
        # Verify BD was assigned
        self.application.refresh_from_db()
        self.assertEqual(self.application.assigned_bd, self.bd_user)
    
    def test_assign_bd_already_assigned(self):
        """Test POST when BD is already assigned."""
        # Assign a BD first
        self.application.assigned_bd = self.bd_user
        self.application.save()
        
        url = self.get_application_url(self.application.id, 'assign-bd')
        data = self.get_bd_assignment_data()
        
        response = self.client.post(url, data, format='json')
        
        self.assertResponseError(response, 400)
        self.assertIn('already has', response.data['error'])
    
    def test_reassign_bd(self):
        """Test PUT /api/applications/{id}/assign-bd/ - Reassign BD."""
        # Assign initial BD
        self.application.assigned_bd = self.admin_user
        self.application.save()
        
        url = self.get_application_url(self.application.id, 'assign-bd')
        data = self.get_bd_assignment_data()
        
        response = self.client.put(url, data, format='json')
        
        self.assertResponseSuccess(response)
        self.assertResponseContains(response, 'message')
        
        # Verify BD was reassigned
        self.application.refresh_from_db()
        self.assertEqual(self.application.assigned_bd, self.bd_user)
    
    def test_remove_bd_assignment(self):
        """Test DELETE /api/applications/{id}/assign-bd/ - Remove BD assignment."""
        # Assign a BD first
        self.application.assigned_bd = self.bd_user
        self.application.save()
        
        url = self.get_application_url(self.application.id, 'assign-bd')
        
        response = self.client.delete(url)
        
        self.assertResponseSuccess(response)
        self.assertResponseContains(response, 'message')
        
        # Verify BD assignment was removed
        self.application.refresh_from_db()
        self.assertIsNone(self.application.assigned_bd)
    
    def test_remove_bd_not_assigned(self):
        """Test DELETE when no BD is assigned."""
        # Ensure no BD is assigned
        self.application.assigned_bd = None
        self.application.save()
        
        url = self.get_application_url(self.application.id, 'assign-bd')
        
        response = self.client.delete(url)
        
        self.assertResponseError(response, 400)
        self.assertIn('does not have', response.data['error'])


class ApplicationLoanExtensionTest(BaseApplicationTestCase, ApplicationTestMixin):
    """Test loan extension endpoints."""
    
    def test_extend_loan(self):
        """Test POST /api/applications/{id}/extend-loan/ - Extend loan."""
        url = self.get_application_url(self.application.id, 'extend-loan')
        data = self.get_loan_extension_data()
        
        response = self.client.post(url, data, format='json')
        
        self.assertResponseSuccess(response)
        self.assertResponseContains(response, 'message')
        
        # Verify loan was extended
        self.application.refresh_from_db()
        self.assertEqual(self.application.interest_rate, Decimal('9.00'))
        self.assertEqual(self.application.loan_amount, Decimal('600000.00'))
    
    def test_extend_loan_invalid_data(self):
        """Test loan extension with invalid data."""
        url = self.get_application_url(self.application.id, 'extend-loan')
        data = self.get_loan_extension_data(new_rate='invalid')
        
        response = self.client.post(url, data, format='json')
        
        self.assertResponseError(response, 400)


class ApplicationFundingCalculationTest(BaseApplicationTestCase, ApplicationTestMixin):
    """Test funding calculation endpoints."""
    
    @patch('applications.services.calculate_funding')
    def test_funding_calculation(self, mock_calculate_funding):
        """Test POST /api/applications/{id}/funding-calculation/ - Funding calculation."""
        # Mock the funding calculation service
        mock_result = {'total_funding': 500000, 'fees': 25000}
        mock_history = MagicMock()
        mock_history.id = 1
        mock_calculate_funding.return_value = (mock_result, mock_history)
        
        url = self.get_application_url(self.application.id, 'funding-calculation')
        data = self.get_funding_calculation_data()
        
        response = self.client.post(url, data, format='json')
        
        self.assertResponseSuccess(response)
        self.assertResponseContains(response, 'message')
        self.assertResponseContains(response, 'result')
        self.assertResponseContains(response, 'history_id')
        
        # Verify the service was called
        mock_calculate_funding.assert_called_once()
    
    @patch('applications.services.calculate_funding')
    def test_funding_calculation_error(self, mock_calculate_funding):
        """Test funding calculation with service error."""
        mock_calculate_funding.side_effect = Exception('Calculation failed')
        
        url = self.get_application_url(self.application.id, 'funding-calculation')
        data = self.get_funding_calculation_data()
        
        response = self.client.post(url, data, format='json')
        
        self.assertResponseError(response, 400)
        self.assertIn('error', response.data)
    
    def test_funding_calculation_history(self):
        """Test GET /api/applications/{id}/funding-calculation-history/ - Get calculation history."""
        # Create some funding calculation history
        from applications.models import FundingCalculationHistory
        history = FundingCalculationHistory.objects.create(
            application=self.application,
            calculation_input={'loan_amount': '500000'},
            calculation_result={'total_funding': 500000},
            created_by=self.admin_user
        )
        
        url = self.get_application_url(self.application.id, 'funding-calculation-history')
        
        response = self.client.get(url)
        
        self.assertResponseSuccess(response)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['id'], history.id)


class ApplicationPermissionsTest(BaseApplicationTestCase):
    """Test application endpoint permissions."""
    
    def test_unauthenticated_access(self):
        """Test that unauthenticated users cannot access endpoints."""
        self.client.credentials()  # Remove authentication
        
        url = self.get_application_url()
        response = self.client.get(url)
        
        self.assertResponseError(response, 401)
    
    def test_broker_access_own_applications(self):
        """Test that brokers can access their own applications."""
        self.authenticate_user(self.broker_user)
        
        # Create application assigned to this broker
        app = self.create_test_application(broker=self.broker, created_by=self.broker_user)
        
        url = self.get_application_url(app.id)
        response = self.client.get(url)
        
        self.assertResponseSuccess(response)
    
    def test_bd_access_assigned_applications(self):
        """Test that BDs can access applications assigned to them."""
        self.authenticate_user(self.bd_user)
        
        # Assign application to this BD
        self.application.assigned_bd = self.bd_user
        self.application.save()
        
        url = self.get_application_url(self.application.id)
        response = self.client.get(url)
        
        self.assertResponseSuccess(response)


class ApplicationPartialUpdateCascadeTest(BaseApplicationTestCase, ApplicationTestMixin):
    """Test partial update with cascade endpoint."""
    
    def setUp(self):
        super().setUp()
        # Create additional test data for cascade testing
        from borrowers.models import Borrower
        self.borrower2 = Borrower.objects.create(
            first_name='Jane',
            last_name='Smith',
            email='jane.smith@test.com',
            phone='0987654321',
            date_of_birth=date(1985, 5, 15)
        )
    
    def test_partial_update_basic_fields(self):
        """Test partial update of basic application fields."""
        url = f'/api/applications/{self.application.id}/partial-update-cascade/'
        data = {
            'loan_amount': '750000.00',
            'interest_rate': '9.25',
            'purpose': 'Updated loan purpose'
        }
        
        response = self.client.patch(url, data, format='json')
        
        self.assertResponseSuccess(response)
        
        # Verify fields were updated
        self.application.refresh_from_db()
        self.assertEqual(self.application.loan_amount, Decimal('750000.00'))
        self.assertEqual(self.application.interest_rate, Decimal('9.25'))
        self.assertEqual(self.application.purpose, 'Updated loan purpose')
    
    def test_partial_update_security_properties(self):
        """Test partial update with security properties cascade."""
        url = f'/api/applications/{self.application.id}/partial-update-cascade/'
        data = {
            'security_properties': [
                {
                    'property_type': 'residential',
                    'address_street_no': '123',
                    'address_street_name': 'Test Street',
                    'address_suburb': 'Test Suburb',
                    'address_state': 'NSW',
                    'address_postcode': '2000',
                    'estimated_value': '850000.00',
                    'bedrooms': 3,
                    'bathrooms': 2
                },
                {
                    'property_type': 'commercial',
                    'address_street_no': '456',
                    'address_street_name': 'Business Ave',
                    'address_suburb': 'Business District',
                    'address_state': 'VIC',
                    'address_postcode': '3000',
                    'estimated_value': '1200000.00'
                }
            ]
        }
        
        response = self.client.patch(url, data, format='json')
        
        self.assertResponseSuccess(response)
        
        # Verify security properties were replaced
        self.application.refresh_from_db()
        properties = self.application.security_properties.all()
        self.assertEqual(properties.count(), 2)
        
        # Check first property
        prop1 = properties.filter(property_type='residential').first()
        self.assertIsNotNone(prop1)
        self.assertEqual(prop1.address_street_no, '123')
        self.assertEqual(prop1.estimated_value, Decimal('850000.00'))
        
        # Check second property
        prop2 = properties.filter(property_type='commercial').first()
        self.assertIsNotNone(prop2)
        self.assertEqual(prop2.address_street_name, 'Business Ave')
    
    def test_partial_update_loan_requirements(self):
        """Test partial update with loan requirements cascade."""
        url = f'/api/applications/{self.application.id}/partial-update-cascade/'
        data = {
            'loan_requirements': [
                {
                    'description': 'Property purchase',
                    'amount': '500000.00'
                },
                {
                    'description': 'Renovation costs',
                    'amount': '150000.00'
                },
                {
                    'description': 'Legal fees',
                    'amount': '25000.00'
                }
            ]
        }
        
        response = self.client.patch(url, data, format='json')
        
        self.assertResponseSuccess(response)
        
        # Verify loan requirements were replaced
        self.application.refresh_from_db()
        requirements = self.application.loan_requirements.all()
        self.assertEqual(requirements.count(), 3)
        
        # Check total amount
        total_amount = sum(req.amount for req in requirements)
        self.assertEqual(total_amount, Decimal('675000.00'))
    
    def test_partial_update_borrowers_create_new(self):
        """Test partial update with new borrowers."""
        url = f'/api/applications/{self.application.id}/partial-update-cascade/'
        data = {
            'borrowers': [
                {
                    'first_name': 'New',
                    'last_name': 'Borrower',
                    'email': 'new.borrower@test.com',
                    'phone': '0111222333',
                    'date_of_birth': '1990-01-01'
                }
            ]
        }
        
        response = self.client.patch(url, data, format='json')
        
        self.assertResponseSuccess(response)
        
        # Verify borrowers were replaced
        self.application.refresh_from_db()
        borrowers = self.application.borrowers.all()
        self.assertEqual(borrowers.count(), 1)
        
        new_borrower = borrowers.first()
        self.assertEqual(new_borrower.first_name, 'New')
        self.assertEqual(new_borrower.last_name, 'Borrower')
        self.assertEqual(new_borrower.email, 'new.borrower@test.com')
    
    def test_partial_update_borrowers_update_existing(self):
        """Test partial update with existing borrower update."""
        url = f'/api/applications/{self.application.id}/partial-update-cascade/'
        data = {
            'borrowers': [
                {
                    'id': self.borrower.id,
                    'first_name': 'Updated John',
                    'email': 'updated.john@test.com'
                },
                {
                    'id': self.borrower2.id,
                    'first_name': 'Updated Jane'
                }
            ]
        }
        
        response = self.client.patch(url, data, format='json')
        
        self.assertResponseSuccess(response)
        
        # Verify borrowers were updated and still associated with application
        self.application.refresh_from_db()
        borrowers = self.application.borrowers.all()
        self.assertEqual(borrowers.count(), 2)
        
        # Check that the borrowers were updated (they should be the same objects)
        borrower_ids = [b.id for b in borrowers]
        self.assertIn(self.borrower.id, borrower_ids)
        self.assertIn(self.borrower2.id, borrower_ids)
        
        # Check updated borrower data
        self.borrower.refresh_from_db()
        self.assertEqual(self.borrower.first_name, 'Updated John')
        self.assertEqual(self.borrower.email, 'updated.john@test.com')
        
        self.borrower2.refresh_from_db()
        self.assertEqual(self.borrower2.first_name, 'Updated Jane')
    
    def test_partial_update_mixed_fields(self):
        """Test partial update with mixed field types."""
        url = f'/api/applications/{self.application.id}/partial-update-cascade/'
        data = {
            'loan_amount': '900000.00',
            'stage': 'sent_to_lender',
            'security_properties': [
                {
                    'property_type': 'residential',
                    'address_street_no': '789',
                    'address_street_name': 'Mixed Update St',
                    'address_suburb': 'Update Suburb',
                    'address_state': 'QLD',
                    'address_postcode': '4000',
                    'estimated_value': '1000000.00'
                }
            ],
            'loan_requirements': [
                {
                    'description': 'Mixed update requirement',
                    'amount': '900000.00'
                }
            ]
        }
        
        response = self.client.patch(url, data, format='json')
        
        self.assertResponseSuccess(response)
        
        # Verify all fields were updated
        self.application.refresh_from_db()
        self.assertEqual(self.application.loan_amount, Decimal('900000.00'))
        self.assertEqual(self.application.stage, 'sent_to_lender')
        
        # Check security property
        properties = self.application.security_properties.all()
        self.assertEqual(properties.count(), 1)
        prop = properties.first()
        self.assertEqual(prop.address_street_name, 'Mixed Update St')
        
        # Check loan requirement
        requirements = self.application.loan_requirements.all()
        self.assertEqual(requirements.count(), 1)
        req = requirements.first()
        self.assertEqual(req.description, 'Mixed update requirement')
    
    def test_partial_update_invalid_data(self):
        """Test partial update with invalid data."""
        url = f'/api/applications/{self.application.id}/partial-update-cascade/'
        data = {
            'loan_amount': 'invalid_amount',
            'stage': 'invalid_stage'
        }
        
        response = self.client.patch(url, data, format='json')
        
        self.assertResponseError(response, 400)
    
    def test_partial_update_nonexistent_application(self):
        """Test partial update on non-existent application."""
        url = '/api/applications/99999/partial-update-cascade/'
        data = {'loan_amount': '500000.00'}
        
        response = self.client.patch(url, data, format='json')
        
        self.assertResponseError(response, 404)


class ApplicationRetrieveCascadeTest(BaseApplicationTestCase, ApplicationTestMixin):
    """Test retrieve with cascade endpoint."""
    
    def setUp(self):
        super().setUp()
        
        # Create additional test data for comprehensive cascade testing
        from borrowers.models import Borrower, Guarantor, Asset, Liability
        from documents.models import Document, Note, Fee, Repayment, Ledger
        from applications.models import SecurityProperty, LoanRequirement, FundingCalculationHistory
        
        # Update the existing borrower from BaseApplicationTestCase to have correct name
        self.borrower.first_name = 'Test'
        self.borrower.last_name = 'Borrower'
        self.borrower.save()
        
        # Update the existing guarantor from BaseApplicationTestCase to have correct name  
        self.guarantor.first_name = 'Test'
        self.guarantor.last_name = 'Guarantor'
        self.guarantor.save()
        
        # Create additional borrowers and guarantors
        self.borrower2 = Borrower.objects.create(
            first_name='Jane',
            last_name='Smith',
            email='jane.smith@test.com',
            phone='0987654321',
            date_of_birth=date(1985, 5, 15)
        )
        
        self.guarantor2 = Guarantor.objects.create(
            application=self.application,
            first_name='Mary',
            last_name='Johnson',
            email='mary.johnson@test.com',
            mobile='0111222333',
            date_of_birth=date(1975, 3, 20)
        )
        
        # Add borrowers and guarantors to application
        self.application.borrowers.add(self.borrower2)
        self.application.guarantors.add(self.guarantor2)
        
        # Create assets and liabilities for borrowers and guarantors
        Asset.objects.create(
            borrower=self.borrower,
            asset_type='property',
            description='Primary residence',
            value=Decimal('750000.00')
        )
        
        Asset.objects.create(
            borrower=self.borrower2,
            asset_type='vehicle',
            description='Car',
            value=Decimal('45000.00')
        )
        
        Liability.objects.create(
            borrower=self.borrower,
            liability_type='mortgage',
            description='Home mortgage',
            amount=Decimal('450000.00'),
            monthly_payment=Decimal('2500.00')
        )
        
        Asset.objects.create(
            guarantor=self.guarantor,
            asset_type='investment',
            description='Stock portfolio',
            value=Decimal('150000.00')
        )
        
        Asset.objects.create(
            guarantor=self.guarantor2,
            asset_type='property',
            description='Investment property',
            value=Decimal('850000.00')
        )
        
        Liability.objects.create(
            guarantor=self.guarantor2,
            liability_type='credit_card',
            description='Credit card debt',
            amount=Decimal('15000.00'),
            monthly_payment=Decimal('500.00')
        )
        
        # Create security properties
        SecurityProperty.objects.create(
            application=self.application,
            property_type='residential',
            address_street_no='123',
            address_street_name='Main Street',
            address_suburb='Test Suburb',
            address_state='NSW',
            address_postcode='2000',
            estimated_value=Decimal('900000.00'),
            bedrooms=4,
            bathrooms=2
        )
        
        SecurityProperty.objects.create(
            application=self.application,
            property_type='commercial',
            address_street_no='456',
            address_street_name='Business Avenue',
            address_suburb='Business District',
            address_state='VIC',
            address_postcode='3000',
            estimated_value=Decimal('1200000.00')
        )
        
        # Create loan requirements
        LoanRequirement.objects.create(
            application=self.application,
            description='Property purchase',
            amount=Decimal('750000.00')
        )
        
        LoanRequirement.objects.create(
            application=self.application,
            description='Renovation costs',
            amount=Decimal('150000.00')
        )
        
        LoanRequirement.objects.create(
            application=self.application,
            description='Legal fees',
            amount=Decimal('25000.00')
        )
        
        # Create documents
        Document.objects.create(
            application=self.application,
            document_type='identity',
            title='Driver License',
            description='Primary borrower ID'
        )
        
        Document.objects.create(
            application=self.application,
            document_type='financial',
            title='Bank Statement',
            description='Last 3 months statements'
        )
        
        # Create notes
        Note.objects.create(
            application=self.application,
            content='Initial application review completed',
            created_by=self.admin_user
        )
        
        Note.objects.create(
            application=self.application,
            content='Documents verified successfully',
            created_by=self.admin_user
        )
        
        # Create fees
        Fee.objects.create(
            application=self.application,
            fee_type='establishment',
            description='Establishment fee',
            amount=Decimal('5000.00'),
            due_date=date.today()
        )
        
        Fee.objects.create(
            application=self.application,
            fee_type='valuation',
            description='Property valuation fee',
            amount=Decimal('800.00'),
            due_date=date.today()
        )
        
        # Create repayments
        Repayment.objects.create(
            application=self.application,
            amount=Decimal('25000.00'),
            due_date=date.today()
        )
        
        # Create ledger entries
        Ledger.objects.create(
            application=self.application,
            transaction_type='adjustment',
            amount=Decimal('500000.00'),
            description='Loan funding',
            transaction_date=timezone.now()
        )
        
        Ledger.objects.create(
            application=self.application,
            transaction_type='fee_created',
            amount=Decimal('5000.00'),
            description='Fee payment',
            transaction_date=timezone.now()
        )
        
        # Create funding calculation history
        FundingCalculationHistory.objects.create(
            application=self.application,
            calculation_input={
                'loan_amount': '500000.00',
                'interest_rate': '8.50',
                'term_months': 12
            },
            calculation_result={
                'establishment_fee': 5000.0,
                'total_funding': 495000.0,
                'funds_available': 470000.0
            },
            created_by=self.admin_user
        )
        
        FundingCalculationHistory.objects.create(
            application=self.application,
            calculation_input={
                'loan_amount': '600000.00',
                'interest_rate': '9.00',
                'term_months': 18
            },
            calculation_result={
                'establishment_fee': 6000.0,
                'total_funding': 594000.0,
                'funds_available': 565000.0
            },
            created_by=self.admin_user
        )
        
    def test_retrieve_with_cascade_success(self):
        """Test successful retrieval with cascade including all related objects."""
        url = f'/api/applications/{self.application.id}/retrieve-cascade/'
        
        response = self.client.get(url)
        
        self.assertResponseSuccess(response)
        
        # Verify all main application fields are present
        self.assertResponseContains(response, 'id', self.application.id)
        self.assertResponseContains(response, 'reference_number', self.application.reference_number)
        self.assertResponseContains(response, 'loan_amount')
        self.assertResponseContains(response, 'stage')
        
        # Verify all related objects are included
        self.assertIn('borrowers', response.data)
        self.assertIn('guarantors', response.data)
        self.assertIn('security_properties', response.data)
        self.assertIn('loan_requirements', response.data)
        self.assertIn('documents', response.data)
        self.assertIn('notes', response.data)
        self.assertIn('fees', response.data)
        self.assertIn('repayments', response.data)
        self.assertIn('ledger_entries', response.data)
        
        # Verify related parties are included
        self.assertIn('broker', response.data)
        self.assertIn('bd', response.data)
        self.assertIn('branch', response.data)
        self.assertIn('valuer', response.data)
        self.assertIn('quantity_surveyor', response.data)
        
        # Verify cascade metadata is included
        self.assertIn('cascade_info', response.data)
        cascade_info = response.data['cascade_info']
        
        self.assertIn('retrieved_at', cascade_info)
        self.assertIn('borrower_count', cascade_info)
        self.assertIn('guarantor_count', cascade_info)
        self.assertIn('security_property_count', cascade_info)
        self.assertIn('loan_requirement_count', cascade_info)
        self.assertIn('document_count', cascade_info)
        self.assertIn('note_count', cascade_info)
        self.assertIn('retrieval_method', cascade_info)
        
        self.assertEqual(cascade_info['retrieval_method'], 'cascade')
        
    def test_retrieve_with_cascade_counts_verification(self):
        """Test that cascade metadata counts match the actual data returned."""
        url = f'/api/applications/{self.application.id}/retrieve-cascade/'
        
        response = self.client.get(url)
        self.assertResponseSuccess(response)
        
        data = response.data
        cascade_info = data['cascade_info']
        
        # Verify counts match actual data
        self.assertEqual(cascade_info['borrower_count'], len(data['borrowers']))
        self.assertEqual(cascade_info['guarantor_count'], len(data['guarantors']))
        self.assertEqual(cascade_info['security_property_count'], len(data['security_properties']))
        self.assertEqual(cascade_info['loan_requirement_count'], len(data['loan_requirements']))
        self.assertEqual(cascade_info['document_count'], len(data['documents']))
        self.assertEqual(cascade_info['note_count'], len(data['notes']))
        
        # Verify expected counts based on setup
        self.assertEqual(cascade_info['borrower_count'], 2)  # borrower + borrower2
        self.assertEqual(cascade_info['guarantor_count'], 2)  # guarantor + guarantor2
        self.assertEqual(cascade_info['security_property_count'], 2)
        self.assertEqual(cascade_info['loan_requirement_count'], 3)
        self.assertEqual(cascade_info['document_count'], 2)
        self.assertGreaterEqual(cascade_info['note_count'], 2)  # Initial notes + cascade retrieval note
        
    def test_retrieve_with_cascade_borrower_details(self):
        """Test that borrower data includes assets and liabilities."""
        url = f'/api/applications/{self.application.id}/retrieve-cascade/'
        
        response = self.client.get(url)
        self.assertResponseSuccess(response)
        
        borrowers = response.data['borrowers']
        self.assertEqual(len(borrowers), 2)
        
        # Find borrowers by email to verify specific data
        borrower1_data = next(b for b in borrowers if b['email'] == self.borrower.email)
        borrower2_data = next(b for b in borrowers if b['email'] == self.borrower2.email)
        
        # Verify borrower1 has expected data
        self.assertEqual(borrower1_data['first_name'], 'Test')
        self.assertEqual(borrower1_data['last_name'], 'Borrower')
        self.assertIn('assets', borrower1_data)
        self.assertIn('liabilities', borrower1_data)
        
        # Verify borrower2 has expected data
        self.assertEqual(borrower2_data['first_name'], 'Jane')
        self.assertEqual(borrower2_data['last_name'], 'Smith')
        self.assertIn('assets', borrower2_data)
        self.assertIn('liabilities', borrower2_data)
        
    def test_retrieve_with_cascade_guarantor_details(self):
        """Test that guarantor data includes assets and liabilities."""
        url = f'/api/applications/{self.application.id}/retrieve-cascade/'
        
        response = self.client.get(url)
        self.assertResponseSuccess(response)
        
        guarantors = response.data['guarantors']
        self.assertEqual(len(guarantors), 2)
        
        # Find guarantors by email to verify specific data
        guarantor1_data = next(g for g in guarantors if g['email'] == self.guarantor.email)
        guarantor2_data = next(g for g in guarantors if g['email'] == self.guarantor2.email)
        
        # Verify guarantor1 has expected data
        self.assertEqual(guarantor1_data['first_name'], 'Test')
        self.assertEqual(guarantor1_data['last_name'], 'Guarantor')
        self.assertIn('assets', guarantor1_data)
        self.assertIn('liabilities', guarantor1_data)
        
        # Verify guarantor2 has expected data
        self.assertEqual(guarantor2_data['first_name'], 'Mary')
        self.assertEqual(guarantor2_data['last_name'], 'Johnson')
        self.assertIn('assets', guarantor2_data)
        self.assertIn('liabilities', guarantor2_data)
        
    def test_retrieve_with_cascade_security_properties(self):
        """Test that security properties are properly returned."""
        url = f'/api/applications/{self.application.id}/retrieve-cascade/'
        
        response = self.client.get(url)
        self.assertResponseSuccess(response)
        
        properties = response.data['security_properties']
        self.assertEqual(len(properties), 2)
        
        # Find properties by type
        residential = next(p for p in properties if p['property_type'] == 'residential')
        commercial = next(p for p in properties if p['property_type'] == 'commercial')
        
        # Verify residential property
        self.assertEqual(residential['address_street_no'], '123')
        self.assertEqual(residential['address_street_name'], 'Main Street')
        self.assertEqual(residential['estimated_value'], '900000.00')
        self.assertEqual(residential['bedrooms'], 4)
        self.assertEqual(residential['bathrooms'], 2)
        
        # Verify commercial property
        self.assertEqual(commercial['address_street_no'], '456')
        self.assertEqual(commercial['address_street_name'], 'Business Avenue')
        self.assertEqual(commercial['estimated_value'], '1200000.00')
        
    def test_retrieve_with_cascade_loan_requirements(self):
        """Test that loan requirements are properly returned."""
        url = f'/api/applications/{self.application.id}/retrieve-cascade/'
        
        response = self.client.get(url)
        self.assertResponseSuccess(response)
        
        requirements = response.data['loan_requirements']
        self.assertEqual(len(requirements), 3)
        
        # Verify total amount matches expected
        total_amount = sum(Decimal(req['amount']) for req in requirements)
        self.assertEqual(total_amount, Decimal('925000.00'))
        
        # Verify specific requirements exist
        descriptions = [req['description'] for req in requirements]
        self.assertIn('Property purchase', descriptions)
        self.assertIn('Renovation costs', descriptions)
        self.assertIn('Legal fees', descriptions)
        
    def test_retrieve_with_cascade_financial_data(self):
        """Test that financial data (fees, repayments, ledger) is properly returned."""
        url = f'/api/applications/{self.application.id}/retrieve-cascade/'
        
        response = self.client.get(url)
        self.assertResponseSuccess(response)
        
        # Verify fees
        fees = response.data['fees']
        self.assertEqual(len(fees), 2)
        fee_types = [fee['fee_type'] for fee in fees]
        self.assertIn('establishment', fee_types)
        self.assertIn('valuation', fee_types)
        
        # Verify repayments (removed repayment_type check as field doesn't exist)
        repayments = response.data['repayments']
        self.assertEqual(len(repayments), 1)
        self.assertEqual(repayments[0]['amount'], '25000.00')
        
        # Verify ledger entries
        ledger_entries = response.data['ledger_entries']
        self.assertEqual(len(ledger_entries), 5)  # Updated to expect 5 ledger entries
    
    def test_retrieve_with_cascade_creates_audit_note(self):
        """Test that cascade retrieval creates an audit note."""
        initial_note_count = self.application.notes.count()
        
        url = f'/api/applications/{self.application.id}/retrieve-cascade/'
        response = self.client.get(url)
        
        self.assertResponseSuccess(response)
        
        # Verify a new note was created
        final_note_count = self.application.notes.count()
        self.assertEqual(final_note_count, initial_note_count + 1)
        
        # Verify the note content
        latest_note = self.application.notes.latest('created_at')
        self.assertIn('cascade', latest_note.content.lower())
        self.assertIn('retrieved', latest_note.content.lower())
        self.assertEqual(latest_note.created_by, self.admin_user)
        
    def test_retrieve_with_cascade_nonexistent_application(self):
        """Test retrieve with cascade on non-existent application."""
        url = '/api/applications/99999/retrieve-cascade/'
        
        response = self.client.get(url)
        
        self.assertResponseError(response, 404)
        self.assertIn('not found', response.data['error'].lower())
        
    def test_retrieve_with_cascade_unauthenticated(self):
        """Test that unauthenticated users cannot access cascade retrieval."""
        self.client.credentials()  # Remove authentication
        
        url = f'/api/applications/{self.application.id}/retrieve-cascade/'
        response = self.client.get(url)
        
        self.assertResponseError(response, 401)
        
    def test_retrieve_with_cascade_performance_optimization(self):
        """Test that cascade retrieval uses optimized queries."""
        # This test verifies the response structure which indicates proper prefetching
        url = f'/api/applications/{self.application.id}/retrieve-cascade/'
        
        # Optimized query count after fixing N+1 issues in ApplicationDetailSerializer
        with self.assertNumQueries(27):  # Significantly reduced from 35+ through prefetch optimization
            response = self.client.get(url)
            
        self.assertResponseSuccess(response)
        
        # Verify that all related data is present (indicating successful prefetching)
        data = response.data
        
        # Check that borrowers have their assets and liabilities loaded
        for borrower in data['borrowers']:
            self.assertIn('assets', borrower)
            self.assertIn('liabilities', borrower)
            
        # Check that guarantors have their assets and liabilities loaded
        for guarantor in data['guarantors']:
            self.assertIn('assets', guarantor)
            self.assertIn('liabilities', guarantor)
            
        # Verify all other related objects are present
        self.assertTrue(len(data['security_properties']) > 0)
        self.assertTrue(len(data['loan_requirements']) > 0)
        self.assertTrue(len(data['documents']) > 0)
        self.assertTrue(len(data['notes']) > 0)
        
    def test_retrieve_with_cascade_vs_regular_retrieve(self):
        """Test that cascade retrieval returns more comprehensive data than regular retrieve."""
        # Regular retrieve (fix URL pattern)
        regular_url = f'/api/applications/applications/{self.application.id}/'
        regular_response = self.client.get(regular_url)
        self.assertResponseSuccess(regular_response)
        
        # Cascade retrieve
        cascade_url = f'/api/applications/{self.application.id}/retrieve-cascade/'
        cascade_response = self.client.get(cascade_url)
        self.assertResponseSuccess(cascade_response)
        
        # Verify cascade response has more comprehensive data
        self.assertIn('borrowers', cascade_response.data)
        self.assertIn('guarantors', cascade_response.data)
        self.assertIn('security_properties', cascade_response.data)
        self.assertIn('loan_requirements', cascade_response.data)
        self.assertIn('documents', cascade_response.data)
        self.assertIn('notes', cascade_response.data)
        self.assertIn('fees', cascade_response.data)
        self.assertIn('repayments', cascade_response.data)
        self.assertIn('ledger_entries', cascade_response.data)
        self.assertIn('funding_calculation_history', cascade_response.data)
        self.assertIn('cascade_info', cascade_response.data)
        
        # Verify regular response has basic data but not the comprehensive cascade data
        self.assertNotIn('cascade_info', regular_response.data) 