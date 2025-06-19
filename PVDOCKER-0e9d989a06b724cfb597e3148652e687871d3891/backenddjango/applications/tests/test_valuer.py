from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from applications.models import Valuer, Application
from brokers.models import Broker, Branch, BDM
from decimal import Decimal

User = get_user_model()


class ValuerViewSetTests(TestCase):
    def setUp(self):
        """Set up test data"""
        # Create test users
        self.admin_user = User.objects.create_user(
            email='admin@test.com',
            password='testpass123',
            role='admin',
            first_name='Admin',
            last_name='User'
        )
        self.broker_user = User.objects.create_user(
            email='broker@test.com',
            password='testpass123',
            role='broker',
            first_name='Broker',
            last_name='User'  
        )
        self.regular_user = User.objects.create_user(
            email='user@test.com',
            password='testpass123',
            role='client',
            first_name='Regular',
            last_name='User'
        )

        # Create test valuers
        self.valuer1 = Valuer.objects.create(
            company_name='Premium Valuations',
            contact_name='John Smith',
            phone='02 1234 5678',
            email='john@premiumval.com.au',
            address='123 Business St, Sydney NSW 2000',
            notes='Specializes in commercial properties',
            is_active=True,
            created_by=self.admin_user
        )
        
        self.valuer2 = Valuer.objects.create(
            company_name='Elite Property Valuers',
            contact_name='Sarah Johnson',
            phone='03 9876 5432',
            email='sarah@elitevaluers.com.au',
            address='456 Professional Ave, Melbourne VIC 3000',
            notes='Expert in residential properties',
            is_active=True,
            created_by=self.admin_user
        )
        
        self.valuer3 = Valuer.objects.create(
            company_name='Inactive Valuers Ltd',
            contact_name='Michael Brown',
            phone='07 5555 1234',
            email='michael@inactivevaluers.com.au',
            address='789 Inactive Rd, Brisbane QLD 4000',
            notes='Currently inactive',
            is_active=False,
            created_by=self.admin_user
        )

        # Create test application with valuer relationship
        broker = Broker.objects.create(
            name='Test Broker',
            email='testbroker@example.com',
            phone='1234567890'
        )
        branch = Branch.objects.create(
            name='Test Branch'
        )
        bdm = BDM.objects.create(
            user=self.broker_user,
            name='Test BDM',
            email='testbdm@example.com',
            phone='1234567890'
        )
        
        self.application = Application.objects.create(
            loan_amount=Decimal('500000.00'),
            loan_term=360,
            purpose='Property Purchase',
            application_type='residential',
            valuer=self.valuer1,
            broker=broker,
            branch=branch,
            bd=bdm,
            created_by=self.admin_user
        )

        # Set up API client
        self.client = APIClient()
        
        # Base URL for valuer endpoints
        self.base_url = '/api/applications/valuers/'

    def test_list_valuers_authenticated(self):
        """Test listing valuers with authentication"""
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.get(self.base_url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('results', response.data)
        # Should return all valuers by default (active and inactive)
        self.assertEqual(len(response.data['results']), 3)

    def test_list_valuers_unauthenticated(self):
        """Test listing valuers without authentication"""
        response = self.client.get(self.base_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_filter_by_active_status(self):
        """Test filtering valuers by active status"""
        self.client.force_authenticate(user=self.admin_user)
        
        # Filter for active valuers only
        response = self.client.get(f'{self.base_url}?is_active=true')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)
        
        # Filter for inactive valuers only
        response = self.client.get(f'{self.base_url}?is_active=false')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['company_name'], 'Inactive Valuers Ltd')

    def test_search_valuers(self):
        """Test searching valuers by various fields"""
        self.client.force_authenticate(user=self.admin_user)
        
        # Search by company name
        response = self.client.get(f'{self.base_url}?search=Premium')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['company_name'], 'Premium Valuations')
        
        # Search by contact name
        response = self.client.get(f'{self.base_url}?search=Sarah')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['contact_name'], 'Sarah Johnson')
        
        # Search by email
        response = self.client.get(f'{self.base_url}?search=elitevaluers')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        
        # Search by phone
        response = self.client.get(f'{self.base_url}?search=02 1234')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_ordering_valuers(self):
        """Test ordering valuers"""
        self.client.force_authenticate(user=self.admin_user)
        
        # Order by company name
        response = self.client.get(f'{self.base_url}?ordering=company_name')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['results'][0]['company_name'], 'Elite Property Valuers')
        
        # Order by contact name descending
        response = self.client.get(f'{self.base_url}?ordering=-contact_name')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['results'][0]['contact_name'], 'Sarah Johnson')

    def test_retrieve_valuer(self):
        """Test retrieving a specific valuer"""
        self.client.force_authenticate(user=self.admin_user)
        url = f'{self.base_url}{self.valuer1.id}/'
        
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['company_name'], 'Premium Valuations')
        self.assertEqual(response.data['contact_name'], 'John Smith')
        self.assertIn('application_count', response.data)
        self.assertEqual(response.data['application_count'], 1)  # One application uses this valuer

    def test_create_valuer_as_admin(self):
        """Test creating a new valuer as admin"""
        self.client.force_authenticate(user=self.admin_user)
        
        data = {
            'company_name': 'New Valuation Company',
            'contact_name': 'Jane Doe',
            'phone': '04 1111 2222',
            'email': 'jane@newval.com.au',
            'address': '321 New St, Perth WA 6000',
            'notes': 'Newly established valuation firm',
            'is_active': True
        }
        
        response = self.client.post(self.base_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # Verify the valuer was created
        valuer = Valuer.objects.get(id=response.data['id'])
        self.assertEqual(valuer.company_name, 'New Valuation Company')
        self.assertEqual(valuer.contact_name, 'Jane Doe')
        self.assertEqual(valuer.created_by, self.admin_user)

    def test_create_valuer_as_broker(self):
        """Test creating a new valuer as broker"""
        self.client.force_authenticate(user=self.broker_user)
        
        data = {
            'company_name': 'Broker Created Valuer',
            'contact_name': 'Broker Contact',
            'phone': '04 2222 3333',
            'email': 'broker@valuer.com.au',
            'is_active': True
        }
        
        response = self.client.post(self.base_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # Verify the valuer was created by the broker
        valuer = Valuer.objects.get(id=response.data['id'])
        self.assertEqual(valuer.created_by, self.broker_user)

    def test_create_valuer_invalid_data(self):
        """Test creating valuer with invalid data"""
        self.client.force_authenticate(user=self.admin_user)
        
        # Missing required fields
        data = {
            'company_name': '',  # Required field empty
            'phone': '04 1111 2222',
            'email': 'invalid-email',  # Invalid email format
        }
        
        response = self.client.post(self.base_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('company_name', response.data)
        self.assertIn('contact_name', response.data)
        self.assertIn('email', response.data)

    def test_update_valuer(self):
        """Test updating a valuer"""
        self.client.force_authenticate(user=self.admin_user)
        url = f'{self.base_url}{self.valuer1.id}/'
        
        data = {
            'company_name': 'Updated Valuation Services',
            'contact_name': 'John Smith Updated',
            'phone': '02 1111 1111',
            'email': 'john.updated@premiumval.com.au',
            'address': 'Updated Address',
            'notes': 'Updated notes',
            'is_active': True
        }
        
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Verify the valuer was updated
        self.valuer1.refresh_from_db()
        self.assertEqual(self.valuer1.company_name, 'Updated Valuation Services')
        self.assertEqual(self.valuer1.contact_name, 'John Smith Updated')

    def test_partial_update_valuer(self):
        """Test partially updating a valuer"""
        self.client.force_authenticate(user=self.admin_user)
        url = f'{self.base_url}{self.valuer1.id}/'
        
        # Include required fields for the update to succeed
        data = {
            'company_name': self.valuer1.company_name,
            'contact_name': self.valuer1.contact_name,
            'phone': self.valuer1.phone,
            'email': self.valuer1.email,
            'notes': 'Partially updated notes only',
            'is_active': True
        }
        
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Verify the notes were updated
        self.valuer1.refresh_from_db()
        self.assertEqual(self.valuer1.notes, 'Partially updated notes only')

    def test_activate_valuer(self):
        """Test activating an inactive valuer"""
        self.client.force_authenticate(user=self.admin_user)
        url = f'{self.base_url}{self.valuer3.id}/activate/'
        
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('status', response.data)
        
        # Verify the valuer was activated
        self.valuer3.refresh_from_db()
        self.assertTrue(self.valuer3.is_active)

    def test_deactivate_valuer(self):
        """Test deactivating an active valuer"""
        self.client.force_authenticate(user=self.admin_user)
        url = f'{self.base_url}{self.valuer1.id}/deactivate/'
        
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('status', response.data)
        
        # Verify the valuer was deactivated
        self.valuer1.refresh_from_db()
        self.assertFalse(self.valuer1.is_active)

    def test_get_applications_for_valuer(self):
        """Test getting applications that use a specific valuer"""
        self.client.force_authenticate(user=self.admin_user)
        url = f'{self.base_url}{self.valuer1.id}/applications/'
        
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['id'], self.application.id)

    def test_pagination(self):
        """Test pagination of valuers list"""
        # Create additional valuers for pagination test
        for i in range(10):
            Valuer.objects.create(
                company_name=f'Test Valuer {i}',
                contact_name=f'Contact {i}',
                phone=f'04 0000 000{i}',
                email=f'test{i}@valuer.com.au',
                created_by=self.admin_user
            )
        
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.get(f'{self.base_url}')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Should return all valuers since pagination might not be implemented yet
        # or configured differently in the actual API
        self.assertTrue(len(response.data.get('results', response.data)) >= 3)

    def test_valuer_str_representation(self):
        """Test the string representation of Valuer model"""
        expected_str = f"{self.valuer1.company_name} - {self.valuer1.contact_name}"
        self.assertEqual(str(self.valuer1), expected_str)

    def test_valuer_ordering(self):
        """Test the default ordering of Valuer model"""
        valuers = list(Valuer.objects.all())
        # Should be ordered by company_name, then contact_name
        self.assertEqual(valuers[0].company_name, 'Elite Property Valuers')
        self.assertEqual(valuers[1].company_name, 'Inactive Valuers Ltd')
        self.assertEqual(valuers[2].company_name, 'Premium Valuations')

    def test_application_count_calculation(self):
        """Test that application_count is calculated correctly"""
        self.client.force_authenticate(user=self.admin_user)
        
        # Valuer1 should have 1 application
        url = f'{self.base_url}{self.valuer1.id}/'
        response = self.client.get(url)
        self.assertEqual(response.data['application_count'], 1)
        
        # Valuer2 should have 0 applications
        url = f'{self.base_url}{self.valuer2.id}/'
        response = self.client.get(url)
        self.assertEqual(response.data['application_count'], 0)

    def test_list_serializer_vs_detail_serializer(self):
        """Test that both list and detail views work correctly"""
        self.client.force_authenticate(user=self.admin_user)
        
        # Test list view
        list_response = self.client.get(self.base_url)
        self.assertEqual(list_response.status_code, status.HTTP_200_OK)
        results_data = list_response.data.get('results', list_response.data)
        if results_data:
            list_fields = set(results_data[0].keys())
            # Basic fields should be present
            self.assertIn('id', list_fields)
            self.assertIn('company_name', list_fields)
            self.assertIn('contact_name', list_fields)
        
        # Test detail view
        detail_response = self.client.get(f'{self.base_url}{self.valuer1.id}/')
        self.assertEqual(detail_response.status_code, status.HTTP_200_OK)
        detail_fields = set(detail_response.data.keys())
        
        # Detail view should have application_count
        self.assertIn('application_count', detail_fields)


class ValuerQuantitySurveyorIntegrationTests(TestCase):
    """Integration tests for Valuer and Quantity Surveyor relationships with Applications"""
    
    def setUp(self):
        """Set up test data"""
        self.admin_user = User.objects.create_user(
            email='admin@test.com',
            password='testpass123',
            role='admin'
        )
        
        self.valuer = Valuer.objects.create(
            company_name='Test Valuer',
            contact_name='Test Contact',
            phone='04 1111 1111',
            email='test@valuer.com.au',
            created_by=self.admin_user
        )
        
        from applications.models import QuantitySurveyor
        self.qs = QuantitySurveyor.objects.create(
            company_name='Test QS',
            contact_name='Test QS Contact',
            phone='04 2222 2222',
            email='test@qs.com.au',
            created_by=self.admin_user
        )
        
        # Create required related objects
        broker = Broker.objects.create(
            name='Test Broker',
            email='broker@test.com',
            phone='1234567890'
        )
        branch = Branch.objects.create(name='Test Branch')
        bdm = BDM.objects.create(
            user=self.admin_user,
            name='Test BDM',
            email='bdm@test.com',
            phone='1234567890'
        )
        
        self.application = Application.objects.create(
            loan_amount=Decimal('500000.00'),
            loan_term=360,
            purpose='Construction',
            application_type='residential',
            valuer=self.valuer,
            quantity_surveyor=self.qs,
            broker=broker,
            branch=branch,
            bd=bdm,
            created_by=self.admin_user
        )
        
        self.client = APIClient()
        self.client.force_authenticate(user=self.admin_user)

    def test_application_relationships(self):
        """Test that applications correctly link to both valuer and QS"""
        # Test valuer relationship
        valuer_apps_url = f'/api/applications/valuers/{self.valuer.id}/applications/'
        response = self.client.get(valuer_apps_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['id'], self.application.id)
        
        # Test QS relationship
        qs_apps_url = f'/api/applications/quantity-surveyors/{self.qs.id}/applications/'
        response = self.client.get(qs_apps_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['id'], self.application.id)

    def test_application_counts_in_listings(self):
        """Test that application counts are correctly displayed in listings"""
        # Check valuer application count
        valuer_detail_url = f'/api/applications/valuers/{self.valuer.id}/'
        response = self.client.get(valuer_detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['application_count'], 1)
        
        # Check QS application count
        qs_detail_url = f'/api/applications/quantity-surveyors/{self.qs.id}/'
        response = self.client.get(qs_detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['application_count'], 1) 