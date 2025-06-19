"""
Base test utilities and fixtures for applications tests.
"""

from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken
from decimal import Decimal
from datetime import date, timedelta
from django.utils import timezone

from applications.models import Application, Valuer, QuantitySurveyor
from borrowers.models import Borrower, Guarantor
from brokers.models import Broker, Branch, BDM

User = get_user_model()


class BaseApplicationTestCase(APITestCase):
    """
    Base test case with common setup for application tests.
    """
    
    def setUp(self):
        """Set up test data for application tests."""
        # Create test users
        self.admin_user = User.objects.create_user(
            email='admin@test.com',
            password='testpass123',
            first_name='Admin',
            last_name='User',
            is_staff=True,
            is_superuser=True
        )
        
        self.broker_user = User.objects.create_user(
            email='broker@test.com',
            password='testpass123',
            first_name='Broker',
            last_name='User'
        )
        
        self.bd_user = User.objects.create_user(
            email='bd@test.com',
            password='testpass123',
            first_name='BD',
            last_name='User',
            role='bd'
        )
        
        # Create test broker entities
        self.branch = Branch.objects.create(
            name='Test Branch',
            address='123 Test St',
            phone='0123456789',
            email='branch@test.com'
        )
        
        self.broker = Broker.objects.create(
            user=self.broker_user,
            name='Test Broker',
            company='Test Brokerage',
            phone='0123456789',
            branch=self.branch
        )
        
        self.bdm = BDM.objects.create(
            user=self.bd_user,
            name='Test BDM',
            phone='0123456789'
        )
        
        # Create test borrower
        self.borrower = Borrower.objects.create(
            first_name='John',
            last_name='Doe',
            email='john.doe@test.com',
            phone='0123456789',
            date_of_birth=date(1980, 1, 1)
        )
        
        # Create test guarantor
        self.guarantor = Guarantor.objects.create(
            first_name='Jane',
            last_name='Smith',
            email='jane.smith@test.com',
            mobile='0123456789',
            date_of_birth=date(1975, 1, 1)
        )
        
        # Create test valuer
        self.valuer = Valuer.objects.create(
            company_name='Test Valuers Ltd',
            contact_name='Valuer Contact',
            phone='0123456789',
            email='valuer@test.com',
            address='456 Valuer St',
            is_active=True
        )
        
        # Create test quantity surveyor
        self.quantity_surveyor = QuantitySurveyor.objects.create(
            company_name='Test QS Ltd',
            contact_name='QS Contact',
            phone='0123456789',
            email='qs@test.com',
            address='789 QS St',
            is_active=True
        )
        
        # Create test application
        self.application = self.create_test_application()
        
        # Set default authenticated user
        self.authenticate_user(self.admin_user)
    
    def create_test_application(self, **kwargs):
        """Create a test application with default values."""
        defaults = {
            'stage': 'inquiry',
            'application_type': 'acquisition',
            'purpose': 'Test loan application',
            'loan_amount': Decimal('500000.00'),
            'loan_term': 12,
            'interest_rate': Decimal('8.50'),
            'loan_purpose': 'purchase',
            'broker': self.broker,
            'branch': self.branch,
            'bd': self.bdm,
            'valuer': self.valuer,
            'quantity_surveyor': self.quantity_surveyor,
            'created_by': self.admin_user,
        }
        defaults.update(kwargs)
        
        application = Application.objects.create(**defaults)
        application.borrowers.add(self.borrower)
        application.guarantors.add(self.guarantor)
        
        return application
    
    def authenticate_user(self, user):
        """Authenticate a user for API requests."""
        refresh = RefreshToken.for_user(user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
    
    def get_application_url(self, application_id=None, action=None):
        """Get URL for application endpoints."""
        base_url = '/api/applications/'
        
        if application_id:
            if action:
                return f'{base_url}{application_id}/{action}/'
            return f'{base_url}applications/{application_id}/'
        
        return f'{base_url}applications/'
    
    def get_valuer_url(self, valuer_id=None, action=None):
        """Get URL for valuer endpoints."""
        base_url = '/api/applications/valuers/'
        
        if valuer_id:
            if action:
                return f'{base_url}{valuer_id}/{action}/'
            return f'{base_url}{valuer_id}/'
        
        return base_url
    
    def get_qs_url(self, qs_id=None, action=None):
        """Get URL for quantity surveyor endpoints."""
        base_url = '/api/applications/quantity-surveyors/'
        
        if qs_id:
            if action:
                return f'{base_url}{qs_id}/{action}/'
            return f'{base_url}{qs_id}/'
        
        return base_url
    
    def assertResponseSuccess(self, response, expected_status=200):
        """Assert that response is successful."""
        response_data = getattr(response, 'data', '<no data>')
        self.assertEqual(
            response.status_code, 
            expected_status, 
            f"Expected {expected_status}, got {response.status_code}. Response: {response_data}"
        )
    
    def assertResponseError(self, response, expected_status=400):
        """Assert that response has expected error status."""
        response_data = getattr(response, 'data', '<no data>')
        self.assertEqual(
            response.status_code, 
            expected_status,
            f"Expected {expected_status}, got {response.status_code}. Response: {response_data}"
        )
    
    def assertResponseContains(self, response, key, value=None):
        """Assert that response contains specified key and optionally value."""
        self.assertIn(key, response.data, f"Key '{key}' not found in response data")
        if value is not None:
            self.assertEqual(
                response.data[key], 
                value, 
                f"Expected {key}={value}, got {response.data[key]}"
            )


class ApplicationTestMixin:
    """Mixin providing application-specific test utilities."""
    
    def get_application_data(self, **overrides):
        """Get default application data for testing."""
        data = {
            'stage': 'inquiry',
            'application_type': 'acquisition',
            'purpose': 'Test application purpose',
            'loan_amount': '250000.00',
            'loan_term': 24,
            'interest_rate': '7.50',
            'loan_purpose': 'purchase',
            'exit_strategy': 'sale',
            'has_pending_litigation': False,
            'has_unsatisfied_judgements': False,
            'has_been_bankrupt': False,
            'has_been_refused_credit': False,
            'has_outstanding_ato_debt': False,
            'has_outstanding_tax_returns': False,
            'has_payment_arrangements': False,
        }
        data.update(overrides)
        return data
    
    def get_signature_data(self, **overrides):
        """Get default signature data for testing."""
        data = {
            'name': 'Test Signatory',
            'signature': 'Test Signature Content',
            'signature_date': date.today().isoformat(),
        }
        data.update(overrides)
        return data
    
    def get_stage_update_data(self, **overrides):
        """Get default stage update data for testing."""
        data = {
            'stage': 'sent_to_lender',
            'notes': 'Stage updated via test',
        }
        data.update(overrides)
        return data
    
    def get_borrower_update_data(self, borrower_ids=None, **overrides):
        """Get default borrower update data for testing."""
        if borrower_ids is None:
            borrower_ids = [self.borrower.id] if hasattr(self, 'borrower') else []
        
        data = {
            'borrower_ids': borrower_ids,
        }
        data.update(overrides)
        return data
    
    def get_bd_assignment_data(self, bd_id=None, **overrides):
        """Get default BD assignment data for testing."""
        if bd_id is None:
            bd_id = self.bd_user.id if hasattr(self, 'bd_user') else None
        
        data = {
            'bd_id': bd_id,
        }
        data.update(overrides)
        return data
    
    def get_loan_extension_data(self, **overrides):
        """Get default loan extension data for testing."""
        data = {
            'new_rate': '9.00',
            'new_loan_amount': '600000.00',
            'new_repayment': '5000.00',
        }
        data.update(overrides)
        return data
    
    def get_funding_calculation_data(self, **overrides):
        """Get default funding calculation data for testing."""
        data = {
            'loan_amount': '500000.00',
            'interest_rate': '8.50',
            'term_months': 12,
            'capitalised_interest_months': 6,
        }
        data.update(overrides)
        return data


class ValuerTestMixin:
    """Mixin providing valuer-specific test utilities."""
    
    def get_valuer_data(self, **overrides):
        """Get default valuer data for testing."""
        data = {
            'company_name': 'Test Valuer Company',
            'contact_name': 'Test Contact',
            'phone': '0123456789',
            'email': 'test.valuer@example.com',
            'address': '123 Test Street',
            'is_active': True,
        }
        data.update(overrides)
        return data


class QuantitySurveyorTestMixin:
    """Mixin providing quantity surveyor-specific test utilities."""
    
    def get_qs_data(self, **overrides):
        """Get default quantity surveyor data for testing."""
        data = {
            'company_name': 'Test QS Company',
            'contact_name': 'Test QS Contact',
            'phone': '0123456789',
            'email': 'test.qs@example.com',
            'address': '456 Test Avenue',
            'is_active': True,
        }
        data.update(overrides)
        return data 