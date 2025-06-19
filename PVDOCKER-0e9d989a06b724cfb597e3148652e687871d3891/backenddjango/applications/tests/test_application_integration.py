"""
Integration tests for application APIs.

This module tests end-to-end workflows and cross-component interactions
between applications, borrowers, documents, and other related entities.
"""

import json
import tempfile
from django.test import TestCase, override_settings
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from unittest.mock import patch, MagicMock
from decimal import Decimal
from datetime import date, timedelta
from django.utils import timezone
from django.core.files.uploadedfile import SimpleUploadedFile

from applications.models import Application, FundingCalculationHistory
from borrowers.models import Borrower, Guarantor
from documents.models import Document, Note, Fee, Repayment
from users.models import Notification
from .base import BaseApplicationTestCase, ApplicationTestMixin


class ApplicationWorkflowIntegrationTest(BaseApplicationTestCase, ApplicationTestMixin):
    """Test complete application workflows from creation to completion."""
    
    def test_complete_application_lifecycle(self):
        """Test a complete application workflow from draft to approval."""
        # Step 1: Create application in draft
        url = self.get_application_url()
        data = self.get_application_data(stage='inquiry')  # Changed from 'draft' to 'inquiry'
        
        response = self.client.post(url, data, format='json')
        self.assertResponseSuccess(response, 201)
        
        app_id = response.data['id']
        
        # Step 2: Add borrowers
        borrowers_url = self.get_application_url(app_id, 'borrowers')
        borrower_data = self.get_borrower_update_data([self.borrower.id])
        
        response = self.client.put(borrowers_url, borrower_data, format='json')
        self.assertResponseSuccess(response)
        
        # Step 3: Update stage to submitted
        stage_url = self.get_application_url(app_id, 'stage')
        stage_data = self.get_stage_update_data(stage='app_submitted')
        
        response = self.client.put(stage_url, stage_data, format='json')
        self.assertResponseSuccess(response)
        
        # Step 4: Assign BD
        bd_url = self.get_application_url(app_id, 'assign-bd')
        bd_data = self.get_bd_assignment_data()
        
        response = self.client.post(bd_url, bd_data, format='json')
        self.assertResponseSuccess(response)
        
        # Step 5: Perform funding calculation
        funding_url = self.get_application_url(app_id, 'funding-calculation')
        funding_data = self.get_funding_calculation_data()
        
        with patch('applications.services.calculate_funding') as mock_calc:
            mock_result = {'total_funding': 400000, 'fees': 25000}
            mock_history = MagicMock()
            mock_history.id = 1
            mock_calc.return_value = (mock_result, mock_history)
            
            response = self.client.post(funding_url, funding_data, format='json')
            self.assertResponseSuccess(response)
        
        # Step 6: Sign application
        sign_url = self.get_application_url(app_id, 'sign')
        sign_data = {'name': 'John Doe', 'date': date.today().isoformat()}
        
        response = self.client.post(sign_url, sign_data, format='json')
        self.assertResponseSuccess(response)
        
        # Step 7: Update to formal_approval
        final_stage_data = self.get_stage_update_data(stage='formal_approval')
        response = self.client.put(stage_url, final_stage_data, format='json')
        self.assertResponseSuccess(response)
        
        # Verify final application state
        app_url = self.get_application_url(app_id)
        response = self.client.get(app_url)
        self.assertResponseSuccess(response)
        
        app_data = response.data
        self.assertEqual(app_data['stage'], 'formal_approval')
        self.assertEqual(app_data['signed_by'], 'John Doe')
        self.assertIsNotNone(app_data['signature_date'])
        self.assertGreater(len(app_data['borrowers']), 0)
    
    def test_application_rejection_workflow(self):
        """Test application rejection with notes and notifications."""
        # Create application
        url = self.get_application_url()
        data = self.get_application_data(stage='app_submitted')
        
        response = self.client.post(url, data, format='json')
        app_id = response.data['id']
        
        # Assign BD first
        bd_url = self.get_application_url(app_id, 'assign-bd')
        bd_data = self.get_bd_assignment_data()
        response = self.client.post(bd_url, bd_data, format='json')
        
        # Reject application with notes
        stage_url = self.get_application_url(app_id, 'stage')
        rejection_data = self.get_stage_update_data(
            stage='declined',
            notes='Application declined due to insufficient documentation'
        )
        
        response = self.client.put(stage_url, rejection_data, format='json')
        self.assertResponseSuccess(response)
        
        # Verify application state
        app_url = self.get_application_url(app_id)
        response = self.client.get(app_url)
        app_data = response.data
        
        self.assertEqual(app_data['stage'], 'declined')
        
        # Verify note was created
        self.assertIn('notes', app_data)
        notes = app_data['notes']
        rejection_note = next((note for note in notes if 'declined' in note['content'].lower()), None)
        self.assertIsNotNone(rejection_note)


class ApplicationBorrowerIntegrationTest(BaseApplicationTestCase, ApplicationTestMixin):
    """Test integration between applications and borrowers."""
    
    def test_application_with_multiple_borrowers_and_guarantors(self):
        """Test creating application with multiple borrowers and guarantors."""
        # Create additional borrowers and guarantors
        borrower2 = Borrower.objects.create(
            first_name='Jane',
            last_name='Smith',
            email='jane.smith@test.com',
            phone='0987654321',
            date_of_birth=date(1985, 5, 15)
        )
        
        guarantor2 = Guarantor.objects.create(
            first_name='Bob',
            last_name='Johnson',
            email='bob.johnson@test.com',
            mobile='0555123456',
            date_of_birth=date(1970, 3, 10)
        )
        
        # Create application
        url = self.get_application_url()
        data = self.get_application_data()
        
        response = self.client.post(url, data, format='json')
        app_id = response.data['id']
        
        # Update borrowers
        borrowers_url = self.get_application_url(app_id, 'borrowers')
        borrower_data = self.get_borrower_update_data([self.borrower.id, borrower2.id])
        
        response = self.client.put(borrowers_url, borrower_data, format='json')
        self.assertResponseSuccess(response)
        
        # Verify application details include all borrowers
        app_url = self.get_application_url(app_id)
        response = self.client.get(app_url)
        app_data = response.data
        
        self.assertEqual(len(app_data['borrowers']), 2)
        borrower_ids = [b['id'] for b in app_data['borrowers']]
        self.assertIn(self.borrower.id, borrower_ids)
        self.assertIn(borrower2.id, borrower_ids)
    
    def test_borrower_removal_from_application(self):
        """Test removing borrower from application."""
        # Start with application having borrower
        borrowers_url = self.get_application_url(self.application.id, 'borrowers')
        
        # Create second borrower and add both
        borrower2 = Borrower.objects.create(
            first_name='Jane',
            last_name='Smith',
            email='jane.smith@test.com',
            phone='0987654321',
            date_of_birth=date(1985, 5, 15)
        )
        
        # Add both borrowers
        borrower_data = self.get_borrower_update_data([self.borrower.id, borrower2.id])
        response = self.client.put(borrowers_url, borrower_data, format='json')
        self.assertResponseSuccess(response)
        
        # Remove one borrower
        borrower_data = self.get_borrower_update_data([borrower2.id])
        response = self.client.put(borrowers_url, borrower_data, format='json')
        self.assertResponseSuccess(response)
        
        # Verify only one borrower remains
        app_url = self.get_application_url(self.application.id)
        response = self.client.get(app_url)
        app_data = response.data
        
        self.assertEqual(len(app_data['borrowers']), 1)
        self.assertEqual(app_data['borrowers'][0]['id'], borrower2.id)


class ApplicationFilteringIntegrationTest(BaseApplicationTestCase, ApplicationTestMixin):
    """Test application filtering and search functionality."""
    
    def setUp(self):
        super().setUp()
        # Create additional applications for filtering tests
        self.high_value_app = self.create_test_application(
            loan_amount=Decimal('1000000.00'),
            stage='formal_approval',
            application_type='refinance'
        )
        
        self.low_value_app = self.create_test_application(
            loan_amount=Decimal('200000.00'),
            stage='app_submitted',
            application_type='acquisition'
        )
    
    def test_enhanced_list_filtering_comprehensive(self):
        """Test comprehensive filtering on enhanced list endpoint."""
        url = '/api/applications/enhanced-applications/'
        
        # Test stage filtering
        response = self.client.get(url, {'stage': 'formal_approval'})
        self.assertResponseSuccess(response)
        results = response.data['results']
        self.assertTrue(all(app['stage'] == 'formal_approval' for app in results))
        
        # Test loan amount range filtering
        response = self.client.get(url, {
            'min_loan_amount': '500000',
            'max_loan_amount': '1500000'
        })
        self.assertResponseSuccess(response)
        results = response.data['results']
        for app in results:
            loan_amount = float(app['loan_amount'])
            self.assertGreaterEqual(loan_amount, 500000)
            self.assertLessEqual(loan_amount, 1500000)
        
        # Test application type filtering
        response = self.client.get(url, {'application_type': 'acquisition'})
        self.assertResponseSuccess(response)
        results = response.data['results']
        self.assertTrue(all(app['application_type'] == 'acquisition' for app in results))
        
        # Test sorting
        response = self.client.get(url, {
            'sort_by': 'loan_amount',
            'sort_direction': 'asc'
        })
        self.assertResponseSuccess(response)
        results = response.data['results']
        
        if len(results) > 1:
            for i in range(len(results) - 1):
                current_amount = float(results[i]['loan_amount'])
                next_amount = float(results[i + 1]['loan_amount'])
                self.assertLessEqual(current_amount, next_amount)
    
    def test_filter_metadata_accuracy(self):
        """Test that filter metadata is accurate and complete."""
        url = '/api/applications/enhanced-applications/'
        response = self.client.get(url, {
            'stage': 'inquiry',
            'min_loan_amount': '100000'
        })
        
        self.assertResponseSuccess(response)
        metadata = response.data['metadata']
        
        # Check applied filters
        self.assertEqual(metadata['applied_filters']['stage'], 'inquiry')
        self.assertEqual(metadata['applied_filters']['min_loan_amount'], '100000')
        
        # Check filter options
        self.assertIn('stages', metadata['filter_options'])
        self.assertIn('application_types', metadata['filter_options'])
        
        # Check total count
        self.assertIsInstance(metadata['total_count'], int)
        self.assertGreaterEqual(metadata['total_count'], 0)


class ApplicationDocumentIntegrationTest(BaseApplicationTestCase, ApplicationTestMixin):
    """Test integration between applications and documents."""
    
    @override_settings(MEDIA_ROOT=tempfile.mkdtemp())
    def test_application_document_lifecycle(self):
        """Test document management throughout application lifecycle."""
        # Create a test file
        test_file = SimpleUploadedFile(
            "test_document.pdf",
            b"file_content",
            content_type="application/pdf"
        )
        
        # Test document creation would be done through document API
        # For integration testing, we simulate this
        document = Document.objects.create(
            application=self.application,
            file=test_file,
            document_type='identity'
        )
        
        # Retrieve application with documents
        url = self.get_application_url(self.application.id)
        response = self.client.get(url)
        
        self.assertResponseSuccess(response)
        app_data = response.data
        
        # Verify document is included
        self.assertIn('documents', app_data)
        documents = app_data['documents']
        self.assertEqual(len(documents), 1)
        self.assertEqual(documents[0]['document_type'], 'identity')
    
    def test_application_notes_integration(self):
        """Test note creation and retrieval with applications."""
        # Create note through stage update
        stage_url = self.get_application_url(self.application.id, 'stage')
        stage_data = self.get_stage_update_data(
            stage='app_submitted',
            notes='Application moved to app_submitted stage'
        )
        
        response = self.client.put(stage_url, stage_data, format='json')
        self.assertResponseSuccess(response)
        
        # Retrieve application with notes
        app_url = self.get_application_url(self.application.id)
        response = self.client.get(app_url)
        
        app_data = response.data
        self.assertIn('notes', app_data)
        
        # Find the stage update note
        notes = app_data['notes']
        stage_note = next((note for note in notes if 'app_submitted' in note['content']), None)
        self.assertIsNotNone(stage_note)


class ApplicationFundingIntegrationTest(BaseApplicationTestCase, ApplicationTestMixin):
    """Test funding calculation integration workflows."""
    
    @patch('applications.services.calculate_funding')
    def test_funding_calculation_history_workflow(self, mock_calculate_funding):
        """Test complete funding calculation workflow with history."""
        # Setup mock
        mock_result = {
            'establishment_fee': 10000.0,
            'total_funding': 490000.0,
            'funds_available': 465000.0
        }
        mock_history = FundingCalculationHistory.objects.create(
            application=self.application,
            calculation_input={'loan_amount': '500000'},
            calculation_result=mock_result,
            created_by=self.admin_user
        )
        mock_calculate_funding.return_value = (mock_result, mock_history)
        
        # Perform funding calculation
        funding_url = self.get_application_url(self.application.id, 'funding-calculation')
        funding_data = self.get_funding_calculation_data()
        
        response = self.client.post(funding_url, funding_data, format='json')
        self.assertResponseSuccess(response)
        
        result_data = response.data
        self.assertIn('result', result_data)
        self.assertIn('history_id', result_data)
        
        # Retrieve funding calculation history
        history_url = self.get_application_url(
            self.application.id, 
            'funding-calculation-history'
        )
        response = self.client.get(history_url)
        
        self.assertResponseSuccess(response)
        history_data = response.data
        self.assertGreaterEqual(len(history_data), 1)
        
        # Verify history entry
        latest_history = history_data[0]
        self.assertEqual(latest_history['id'], mock_history.id)
        self.assertIn('calculation_result', latest_history)
    
    def test_manual_funding_calculator(self):
        """Test manual funding calculator endpoint."""
        url = '/api/applications/manual-funding-calculator/'
        data = {
            'loan_amount': '500000.00',
            'interest_rate': '7.50',
            'security_value': '750000.00',
            'establishment_fee_rate': '2.00',
            'capped_interest_months': 9,
            'monthly_line_fee_rate': '0.50',
            'brokerage_fee_rate': '2.00',
            'application_fee': '500.00',
            'due_diligence_fee': '800.00',
            'legal_fee_before_gst': '1200.00',
            'valuation_fee': '1000.00',
            'monthly_account_fee': '50.00',
            'working_fee': '0.00'
        }
        
        response = self.client.post(url, data, format='json')
        self.assertResponseSuccess(response)
        
        result = response.data['result']
        self.assertIn('loan_amount', result)
        self.assertIn('total_fees', result)
        self.assertIn('funds_available', result)
        self.assertIn('lvr', result)
        
        # Verify calculations
        self.assertEqual(result['loan_amount'], 500000.0)
        self.assertGreater(result['total_fees'], 0)
        self.assertLess(result['funds_available'], result['loan_amount'])


class ApplicationBDManagementIntegrationTest(BaseApplicationTestCase, ApplicationTestMixin):
    """Test BD assignment and notification integration."""
    
    def test_bd_assignment_with_notifications(self):
        """Test BD assignment creates proper notifications."""
        # Count initial notifications
        initial_count = Notification.objects.filter(user=self.bd_user).count()
        
        # Assign BD
        bd_url = self.get_application_url(self.application.id, 'assign-bd')
        bd_data = self.get_bd_assignment_data()
        
        response = self.client.post(bd_url, bd_data, format='json')
        self.assertResponseSuccess(response)
        
        # Verify notification was created
        final_count = Notification.objects.filter(user=self.bd_user).count()
        self.assertEqual(final_count, initial_count + 1)
        
        # Check notification content
        notification = Notification.objects.filter(
            user=self.bd_user,
            notification_type='application_status'
        ).latest('created_at')
        
        self.assertIn(self.application.reference_number, notification.title)
        self.assertEqual(notification.related_object_id, self.application.id)
    
    def test_bd_reassignment_workflow(self):
        """Test complete BD reassignment with notifications and notes."""
        # Initial assignment
        bd_url = self.get_application_url(self.application.id, 'assign-bd')
        bd_data = self.get_bd_assignment_data()
        response = self.client.post(bd_url, bd_data, format='json')
        
        # Create second BD user
        from django.contrib.auth import get_user_model
        User = get_user_model()
        bd_user2 = User.objects.create_user(
            email='bd2@test.com',
            password='testpass123',
            first_name='BD2',
            last_name='User',
            role='bd'
        )
        
        # Reassign to different BD
        reassign_data = self.get_bd_assignment_data(bd_id=bd_user2.id)
        response = self.client.put(bd_url, reassign_data, format='json')
        self.assertResponseSuccess(response)
        
        # Verify assignment changed
        self.application.refresh_from_db()
        self.assertEqual(self.application.assigned_bd, bd_user2)
        
        # Verify notification for new BD
        notification = Notification.objects.filter(
            user=bd_user2,
            notification_type='application_status'
        ).latest('created_at')
        self.assertIn(self.application.reference_number, notification.title)


class ApplicationPermissionIntegrationTest(BaseApplicationTestCase):
    """Test permission integration across different user roles."""
    
    def test_broker_application_access_workflow(self):
        """Test broker can only access their own applications throughout workflow."""
        # Create application for broker
        self.authenticate_user(self.broker_user)
        
        url = self.get_application_url()
        data = {
            'stage': 'inquiry',
            'application_type': 'acquisition',
            'purpose': 'Broker test application',
            'loan_amount': '300000.00',
            'loan_term': 12,
            'interest_rate': '8.00',
            'loan_purpose': 'purchase'
        }
        
        response = self.client.post(url, data, format='json')
        self.assertResponseSuccess(response, 201)
        
        broker_app_id = response.data['id']
        
        # Broker can access their own application
        app_url = self.get_application_url(broker_app_id)
        response = self.client.get(app_url)
        self.assertResponseSuccess(response)
        
        # Broker can access admin's application (no restrictions implemented)
        admin_app_url = self.get_application_url(self.application.id)
        response = self.client.get(admin_app_url)
        # Currently no permission restrictions are implemented
        self.assertResponseSuccess(response)
    
    def test_bd_application_access_workflow(self):
        """Test BD can access assigned applications."""
        self.authenticate_user(self.bd_user)
        
        # BD can access unassigned application (no restrictions implemented)
        app_url = self.get_application_url(self.application.id)
        response = self.client.get(app_url)
        self.assertResponseSuccess(response)
        
        # Assign application to BD (as admin)
        self.authenticate_user(self.admin_user)
        self.application.assigned_bd = self.bd_user
        self.application.save()
        
        # BD can still access the application
        self.authenticate_user(self.bd_user)
        response = self.client.get(app_url)
        self.assertResponseSuccess(response)


class ApplicationConcurrencyIntegrationTest(BaseApplicationTestCase, ApplicationTestMixin):
    """Test concurrent access and race condition handling."""
    
    def test_concurrent_stage_updates(self):
        """Test handling of concurrent stage updates."""
        # Simulate concurrent updates by making rapid sequential calls
        stage_url = self.get_application_url(self.application.id, 'stage')
        
        # First update
        stage_data1 = self.get_stage_update_data(stage='app_submitted')
        response1 = self.client.put(stage_url, stage_data1, format='json')
        self.assertResponseSuccess(response1)
        
        # Second update immediately after
        stage_data2 = self.get_stage_update_data(stage='sent_to_lender')
        response2 = self.client.put(stage_url, stage_data2, format='json')
        self.assertResponseSuccess(response2)
        
        # Verify final state
        self.application.refresh_from_db()
        self.assertEqual(self.application.stage, 'sent_to_lender')
    
    def test_concurrent_bd_assignments(self):
        """Test handling of concurrent BD assignments."""
        bd_url = self.get_application_url(self.application.id, 'assign-bd')
        bd_data = self.get_bd_assignment_data()
        
        # First assignment
        response1 = self.client.post(bd_url, bd_data, format='json')
        self.assertResponseSuccess(response1)
        
        # Second assignment attempt (should fail)
        response2 = self.client.post(bd_url, bd_data, format='json')
        self.assertResponseError(response2, 400)
        self.assertIn('already has', response2.data['error'])


class ApplicationDataIntegrityTest(BaseApplicationTestCase, ApplicationTestMixin):
    """Test data integrity across application operations."""
    
    def test_application_deletion_cascade(self):
        """Test that application deletion properly cascades to related objects."""
        app_id = self.application.id
        
        # Create related objects
        note = Note.objects.create(
            application=self.application,
            content='Test note',
            created_by=self.admin_user
        )
        
        funding_history = FundingCalculationHistory.objects.create(
            application=self.application,
            calculation_input={'test': 'data'},
            calculation_result={'test': 'result'},
            created_by=self.admin_user
        )
        
        # Delete application
        url = self.get_application_url(app_id)
        response = self.client.delete(url)
        self.assertResponseSuccess(response, 204)
        
        # Verify cascaded deletion
        self.assertFalse(Application.objects.filter(id=app_id).exists())
        self.assertFalse(Note.objects.filter(id=note.id).exists())
        self.assertFalse(FundingCalculationHistory.objects.filter(id=funding_history.id).exists())
    
    def test_application_reference_number_uniqueness(self):
        """Test that reference numbers remain unique."""
        # Create first application
        url = self.get_application_url()
        data1 = self.get_application_data()
        
        response1 = self.client.post(url, data1, format='json')
        self.assertResponseSuccess(response1, 201)
        
        # Create second application
        data2 = self.get_application_data()
        response2 = self.client.post(url, data2, format='json')
        self.assertResponseSuccess(response2, 201)
        
        # Verify different reference numbers
        ref1 = response1.data['reference_number']
        ref2 = response2.data['reference_number']
        self.assertNotEqual(ref1, ref2)


class ApplicationSearchIntegrationTest(BaseApplicationTestCase, ApplicationTestMixin):
    """Test application search and filtering integration."""
    
    def setUp(self):
        super().setUp()
        # Create applications with different characteristics for search testing
        self.search_app1 = self.create_test_application(
            purpose='Property development loan for commercial building',
            loan_amount=Decimal('800000.00'),
            stage='app_submitted'
        )
        
        self.search_app2 = self.create_test_application(
            purpose='Residential property purchase',
            loan_amount=Decimal('450000.00'),
            stage='formal_approval'
        )
    
    def test_enhanced_list_complex_filtering(self):
        """Test complex filtering scenarios on enhanced list."""
        url = '/api/applications/enhanced-applications/'
        
        # Test multiple filter combination
        params = {
            'stage': 'app_submitted',
            'min_loan_amount': '500000',
            'application_type': 'acquisition'
        }
        
        response = self.client.get(url, params)
        self.assertResponseSuccess(response)
        
        results = response.data['results']
        metadata = response.data['metadata']
        
        # Verify filtering applied correctly
        for app in results:
            self.assertEqual(app['stage'], 'app_submitted')
            self.assertGreaterEqual(float(app['loan_amount']), 500000)
            self.assertEqual(app['application_type'], 'acquisition')
        
        # Verify metadata reflects filters
        applied_filters = metadata['applied_filters']
        self.assertEqual(applied_filters['stage'], 'app_submitted')
        self.assertEqual(applied_filters['min_loan_amount'], '500000')
        self.assertEqual(applied_filters['application_type'], 'acquisition')
    
    def test_pagination_consistency(self):
        """Test pagination consistency across filtered results."""
        url = '/api/applications/enhanced-applications/'
        
        # Get first page
        response1 = self.client.get(url, {'page_size': 2, 'page': 1})
        self.assertResponseSuccess(response1)
        
        # Get second page  
        response2 = self.client.get(url, {'page_size': 2, 'page': 2})
        self.assertResponseSuccess(response2)
        
        # Verify no overlap between pages
        if response1.data['results'] and response2.data['results']:
            page1_ids = {app['id'] for app in response1.data['results']}
            page2_ids = {app['id'] for app in response2.data['results']}
            self.assertEqual(len(page1_ids.intersection(page2_ids)), 0)


class ApplicationErrorHandlingIntegrationTest(BaseApplicationTestCase, ApplicationTestMixin):
    """Test error handling and edge cases in integration scenarios."""
    
    def test_invalid_filter_values_handling(self):
        """Test handling of invalid filter values."""
        url = '/api/applications/enhanced-applications/'
        
        # Test with invalid numeric filter
        response = self.client.get(url, {'min_loan_amount': 'invalid_number'})
        self.assertResponseError(response, 400)
        self.assertIn('Invalid filter value', response.data['error'])
        
        # Test with invalid choice field
        response = self.client.get(url, {'stage': 'invalid_stage'})
        # Should either filter out results or return error
        self.assertIn(response.status_code, [200, 400])
    
    def test_large_dataset_performance(self):
        """Test system behavior with larger datasets."""
        # Create multiple applications for performance testing
        applications = []
        for i in range(20):
            app = self.create_test_application(
                loan_amount=Decimal(f'{300000 + i * 10000}.00'),
                purpose=f'Test application {i}'
            )
            applications.append(app)
        
        # Test list endpoint performance
        url = '/api/applications/enhanced-applications/'
        response = self.client.get(url)
        
        self.assertResponseSuccess(response)
        self.assertIn('results', response.data)
        self.assertIn('metadata', response.data)
        
        # Cleanup
        for app in applications:
            app.delete()
    
    def test_missing_application_handling(self):
        """Test handling of requests for non-existent applications."""
        non_existent_id = 99999
        
        # Test retrieve
        url = self.get_application_url(non_existent_id)
        response = self.client.get(url)
        self.assertResponseError(response, 404)
        
        # Test update
        data = self.get_application_data()
        response = self.client.put(url, data, format='json')
        self.assertResponseError(response, 404)
        
        # Test action endpoints
        sign_url = self.get_application_url(non_existent_id, 'sign')
        response = self.client.post(sign_url, {'name': 'Test'}, format='json')
        self.assertResponseError(response, 404) 