from rest_framework import serializers
from .models import Borrower, Guarantor
from users.serializers import UserSerializer
from drf_spectacular.utils import extend_schema_serializer


class BorrowerListSerializer(serializers.ModelSerializer):
    """Serializer for listing borrowers with minimal information"""
    application_count = serializers.SerializerMethodField()
    related_brokers = serializers.SerializerMethodField()
    address = serializers.SerializerMethodField()
    
    class Meta:
        model = Borrower
        fields = [
            'id', 'first_name', 'last_name', 'email', 
            'phone', 'created_at', 'application_count',
            'residential_address', 'mailing_address', 'address',
            'related_brokers', 'is_company', 'company_name'
        ]
    
    def get_application_count(self, obj) -> int:
        return obj.borrower_applications.count()
        
    def get_related_brokers(self, obj) -> list:
        """Get brokers related to this borrower through applications"""
        from brokers.serializers import BrokerListSerializer
        from brokers.models import Broker
        
        # Get unique broker IDs from all applications this borrower is associated with
        broker_ids = obj.borrower_applications.values_list('broker_id', flat=True).distinct()
        
        # Filter out None values
        broker_ids = [bid for bid in broker_ids if bid is not None]
        
        if not broker_ids:
            return []
            
        # Get the broker objects
        brokers = Broker.objects.filter(id__in=broker_ids)
        
        # Serialize the brokers
        return BrokerListSerializer(brokers, many=True).data
        
    def get_address(self, obj) -> dict:
        """Get formatted address information"""
        if obj.is_company:
            # Return company address information
            return {
                'unit': obj.registered_address_unit,
                'street_no': obj.registered_address_street_no,
                'street_name': obj.registered_address_street_name,
                'suburb': obj.registered_address_suburb,
                'state': obj.registered_address_state,
                'postcode': obj.registered_address_postcode,
                'full_address': obj.company_address or '',
            }
        else:
            # Return individual address information
            return {
                'residential_address': obj.residential_address or '',
                'mailing_address': obj.mailing_address or '',
            }


class BorrowerDetailSerializer(serializers.ModelSerializer):
    """Serializer for detailed borrower information with null/blank handling for minimal data creation"""
    created_by = UserSerializer(read_only=True)
    
    class Meta:
        model = Borrower
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at', 'created_by']
        extra_kwargs = {
            # ===== SHARED PERSONAL INFORMATION FIELDS =====
            'title': {'required': False, 'allow_null': True, 'allow_blank': True},
            'first_name': {'required': False, 'allow_null': True, 'allow_blank': True},
            'last_name': {'required': False, 'allow_null': True, 'allow_blank': True},
            'date_of_birth': {'required': False, 'allow_null': True},
            'drivers_licence_no': {'required': False, 'allow_null': True, 'allow_blank': True},
            'home_phone': {'required': False, 'allow_null': True, 'allow_blank': True},
            'mobile': {'required': False, 'allow_null': True, 'allow_blank': True},
            'email': {'required': False, 'allow_null': True, 'allow_blank': True},
            
            # ===== SHARED RESIDENTIAL ADDRESS FIELDS =====
            'address_unit': {'required': False, 'allow_null': True, 'allow_blank': True},
            'address_street_no': {'required': False, 'allow_null': True, 'allow_blank': True},
            'address_street_name': {'required': False, 'allow_null': True, 'allow_blank': True},
            'address_suburb': {'required': False, 'allow_null': True, 'allow_blank': True},
            'address_state': {'required': False, 'allow_null': True, 'allow_blank': True},
            'address_postcode': {'required': False, 'allow_null': True, 'allow_blank': True},
            
            # ===== SHARED EMPLOYMENT DETAILS FIELDS =====
            'occupation': {'required': False, 'allow_null': True, 'allow_blank': True},
            'employer_name': {'required': False, 'allow_null': True, 'allow_blank': True},
            'employment_type': {'required': False, 'allow_null': True, 'allow_blank': True},
            'annual_income': {'required': False, 'allow_null': True},
            
            # ===== LEGACY FIELDS =====
            'phone': {'required': False, 'allow_null': True, 'allow_blank': True},
            'residential_address': {'required': False, 'allow_null': True, 'allow_blank': True},
            'mailing_address': {'required': False, 'allow_null': True, 'allow_blank': True},
            'job_title': {'required': False, 'allow_null': True, 'allow_blank': True},
            'employer_address': {'required': False, 'allow_null': True, 'allow_blank': True},
            'employment_duration': {'required': False, 'allow_null': True},
            
            # ===== BORROWER-SPECIFIC FIELDS =====
            'tax_id': {'required': False, 'allow_null': True, 'allow_blank': True},
            'marital_status': {'required': False, 'allow_null': True, 'allow_blank': True},
            'residency_status': {'required': False, 'allow_null': True, 'allow_blank': True},
            'other_income': {'required': False, 'allow_null': True},
            'monthly_expenses': {'required': False, 'allow_null': True},
            'bank_name': {'required': False, 'allow_null': True, 'allow_blank': True},
            'bank_account_name': {'required': False, 'allow_null': True, 'allow_blank': True},
            'bank_account_number': {'required': False, 'allow_null': True, 'allow_blank': True},
            'bank_bsb': {'required': False, 'allow_null': True, 'allow_blank': True},
            'referral_source': {'required': False, 'allow_null': True, 'allow_blank': True},
            'tags': {'required': False, 'allow_null': True, 'allow_blank': True},
            'notes_text': {'required': False, 'allow_null': True, 'allow_blank': True},
            'is_company': {'required': False, 'allow_null': True},
            'company_name': {'required': False, 'allow_null': True, 'allow_blank': True},
            'company_abn': {'required': False, 'allow_null': True, 'allow_blank': True},
            'company_acn': {'required': False, 'allow_null': True, 'allow_blank': True},
            'company_address': {'required': False, 'allow_null': True, 'allow_blank': True},
            'industry_type': {'required': False, 'allow_null': True, 'allow_blank': True},
            'contact_number': {'required': False, 'allow_null': True, 'allow_blank': True},
            'annual_company_income': {'required': False, 'allow_null': True},
            'is_trustee': {'required': False, 'allow_null': True},
            'is_smsf_trustee': {'required': False, 'allow_null': True},
            'trustee_name': {'required': False, 'allow_null': True, 'allow_blank': True},
            'registered_address_unit': {'required': False, 'allow_null': True, 'allow_blank': True},
            'registered_address_street_no': {'required': False, 'allow_null': True, 'allow_blank': True},
            'registered_address_street_name': {'required': False, 'allow_null': True, 'allow_blank': True},
            'registered_address_suburb': {'required': False, 'allow_null': True, 'allow_blank': True},
            'registered_address_state': {'required': False, 'allow_null': True, 'allow_blank': True},
            'registered_address_postcode': {'required': False, 'allow_null': True, 'allow_blank': True},
        }
    
    def create(self, validated_data):
        # Set the created_by field to the current user
        # Handle cases where request context might not be available (e.g., when called from other serializers)
        if 'request' in self.context and self.context['request'].user:
            user = self.context['request'].user
            validated_data['created_by'] = user
        elif 'created_by' in validated_data:
            # If created_by is already provided in the data, use it
            pass
        else:
            # Fallback: try to get user from context or use None
            validated_data['created_by'] = self.context.get('user', None)
        return super().create(validated_data)


class BorrowerFinancialSummarySerializer(serializers.Serializer):
    """Serializer for borrower financial summary"""
    total_applications = serializers.IntegerField()
    total_funded = serializers.DecimalField(max_digits=15, decimal_places=2)
    active_loans = serializers.IntegerField()
    active_loan_amount = serializers.DecimalField(max_digits=15, decimal_places=2)
    completed_loans = serializers.IntegerField()
    completed_loan_amount = serializers.DecimalField(max_digits=15, decimal_places=2)


from drf_spectacular.utils import extend_schema_serializer

@extend_schema_serializer(component_name="BorrowerGuarantor")
class GuarantorSerializer(serializers.ModelSerializer):
    """Serializer for guarantor information with null/blank handling for minimal data creation"""
    created_by = UserSerializer(read_only=True)
    
    class Meta:
        model = Guarantor
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at', 'created_by']
        extra_kwargs = {
            # ===== SHARED PERSONAL INFORMATION FIELDS =====
            'title': {'required': False, 'allow_null': True, 'allow_blank': True},
            'first_name': {'required': False, 'allow_null': True, 'allow_blank': True},
            'last_name': {'required': False, 'allow_null': True, 'allow_blank': True},
            'date_of_birth': {'required': False, 'allow_null': True},
            'drivers_licence_no': {'required': False, 'allow_null': True, 'allow_blank': True},
            'home_phone': {'required': False, 'allow_null': True, 'allow_blank': True},
            'mobile': {'required': False, 'allow_null': True, 'allow_blank': True},
            'email': {'required': False, 'allow_null': True, 'allow_blank': True},
            
            # ===== SHARED RESIDENTIAL ADDRESS FIELDS =====
            'address_unit': {'required': False, 'allow_null': True, 'allow_blank': True},
            'address_street_no': {'required': False, 'allow_null': True, 'allow_blank': True},
            'address_street_name': {'required': False, 'allow_null': True, 'allow_blank': True},
            'address_suburb': {'required': False, 'allow_null': True, 'allow_blank': True},
            'address_state': {'required': False, 'allow_null': True, 'allow_blank': True},
            'address_postcode': {'required': False, 'allow_null': True, 'allow_blank': True},
            
            # ===== SHARED EMPLOYMENT DETAILS FIELDS =====
            'occupation': {'required': False, 'allow_null': True, 'allow_blank': True},
            'employer_name': {'required': False, 'allow_null': True, 'allow_blank': True},
            'employment_type': {'required': False, 'allow_null': True, 'allow_blank': True},
            'annual_income': {'required': False, 'allow_null': True},
            
            # ===== LEGACY FIELDS =====
            'address': {'required': False, 'allow_null': True, 'allow_blank': True},
            
            # ===== GUARANTOR-SPECIFIC FIELDS =====
            'guarantor_type': {'required': False, 'allow_null': True, 'allow_blank': True},
            'company_name': {'required': False, 'allow_null': True, 'allow_blank': True},
            'company_abn': {'required': False, 'allow_null': True, 'allow_blank': True},
            'company_acn': {'required': False, 'allow_null': True, 'allow_blank': True},
            'borrower': {'required': False, 'allow_null': True},
            'application': {'required': False, 'allow_null': True},
        }
    
    def create(self, validated_data):
        # Set the created_by field to the current user
        # Handle cases where request context might not be available (e.g., when called from other serializers)
        if 'request' in self.context and self.context['request'].user:
            user = self.context['request'].user
            validated_data['created_by'] = user
        elif 'created_by' in validated_data:
            # If created_by is already provided in the data, use it
            pass
        else:
            # Fallback: try to get user from context or use None
            validated_data['created_by'] = self.context.get('user', None)
        return super().create(validated_data)
    
    def validate(self, data):
        """
        Validate that the appropriate fields are provided based on guarantor type - made optional for minimal data creation
        """
        guarantor_type = data.get('guarantor_type')
        
        # Only validate if guarantor_type is provided - allow minimal data creation
        if guarantor_type == 'individual':
            if not data.get('first_name') and not data.get('last_name'):
                # Allow creation with minimal data - no strict validation for minimal data scenarios
                pass
        elif guarantor_type == 'company':
            if not data.get('company_name'):
                # Allow creation with minimal data - no strict validation for minimal data scenarios
                pass
        
        return data
