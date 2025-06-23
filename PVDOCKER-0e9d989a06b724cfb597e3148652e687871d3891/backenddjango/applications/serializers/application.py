"""
Application Serializers

This module contains serializers for the core Application model,
including create, detail, list, and various update serializers.
"""

from rest_framework import serializers
from django.db import transaction
from decimal import Decimal
from django.utils import timezone

from ..models import Application, SecurityProperty, LoanRequirement
from borrowers.models import Borrower, Guarantor
from users.serializers import UserSerializer
from brokers.serializers import BrokerDetailSerializer as BrokerSerializer, BDMSerializer, BranchSerializer
from documents.models import Document, Fee, Repayment, Note, Ledger
from documents.serializers import DocumentSerializer, NoteSerializer, FeeSerializer, RepaymentSerializer, LedgerSerializer

# Import from other serializer modules
from .borrowers import BorrowerSerializer, GuarantorSerializer, CompanyBorrowerSerializer
from .property import SecurityPropertySerializer, LoanRequirementSerializer
from .funding import FundingCalculationInputSerializer, FundingCalculationHistorySerializer
from .professionals import ValuerListSerializer, QuantitySurveyorListSerializer
from .utils import SolvencyEnquiriesSerializer


class GeneratePDFSerializer(serializers.Serializer):
    """
    Serializer for PDF generation endpoint
    """
    template_name = serializers.CharField(required=False)
    output_format = serializers.ChoiceField(choices=['pdf', 'docx'], default='pdf', required=False)


class ApplicationSignatureSerializer(serializers.Serializer):
    """
    Serializer for application signature
    """
    signature = serializers.CharField(required=True)
    name = serializers.CharField(required=True, max_length=255)
    signature_date = serializers.DateField(required=False)
    notes = serializers.CharField(allow_blank=True, required=False)


class ApplicationStageUpdateSerializer(serializers.Serializer):
    """
    Serializer for updating application stage
    
    Handles stage transitions and maintains a history of stage changes.
    """
    stage = serializers.ChoiceField(choices=Application.STAGE_CHOICES)
    notes = serializers.CharField(required=False, allow_blank=True)
    
    def validate_stage(self, value):
        """Validate stage transitions."""
        if self.instance and value == self.instance.stage:
            raise serializers.ValidationError("Application is already in this stage.")
        
        # Add any specific stage transition validation rules here
        # For example, prevent going back to 'received' from later stages
        if self.instance and self.instance.stage != 'received' and value == 'received':
            raise serializers.ValidationError("Cannot move back to 'received' stage once application has progressed.")
        
        return value
    
    def update(self, instance, validated_data):
        """Update application stage and maintain history."""
        old_stage = instance.stage
        new_stage = validated_data['stage']
        notes = validated_data.get('notes', '')
        
        # Update stage history
        if not instance.stage_history:
            instance.stage_history = []
        
        instance.stage_history.append({
            'from_stage': old_stage,
            'to_stage': new_stage,
            'timestamp': timezone.now().isoformat(),
            'user': self.context['request'].user.username,
            'notes': notes
        })
        
        # Update stage
        instance.stage = new_stage
        instance.save()
        
        # Create note about stage change
        Note.objects.create(
            application=instance,
            title=f"Stage Updated: {instance.get_stage_display()}",
            content=f"Stage changed from '{dict(Application.STAGE_CHOICES)[old_stage]}' to '{dict(Application.STAGE_CHOICES)[new_stage]}'\n\nNotes: {notes}",
            created_by=self.context['request'].user
        )
        
        return instance


class ApplicationBorrowerSerializer(serializers.Serializer):
    """
    Serializer for managing application borrowers
    """
    borrower_ids = serializers.ListField(
        child=serializers.IntegerField(),
        min_length=1
    )


class AssignBDSerializer(serializers.Serializer):
    """
    Serializer for assigning a BD to an application
    """
    bd_id = serializers.IntegerField(required=True)

    def validate_bd_id(self, value):
        from django.contrib.auth import get_user_model
        User = get_user_model()
        
        try:
            user = User.objects.get(id=value)
            if user.role != 'bd':
                raise serializers.ValidationError("User is not a Business Developer")
            return value
        except User.DoesNotExist:
            raise serializers.ValidationError("Invalid BD user ID")


class LoanExtensionSerializer(serializers.Serializer):
    """
    Serializer for extending a loan with new terms
    """
    new_rate = serializers.DecimalField(max_digits=5, decimal_places=2, required=True)
    new_loan_amount = serializers.DecimalField(max_digits=12, decimal_places=2, required=True)
    new_repayment = serializers.DecimalField(max_digits=10, decimal_places=2, required=True)
    
    def validate(self, data):
        """
        Validate the loan extension data
        """
        # Ensure new_rate is positive
        if data['new_rate'] <= Decimal('0'):
            raise serializers.ValidationError({"new_rate": "Interest rate must be greater than 0"})
        
        # Ensure new_loan_amount is positive
        if data['new_loan_amount'] <= Decimal('0'):
            raise serializers.ValidationError({"new_loan_amount": "Loan amount must be greater than 0"})
        
        # Ensure new_repayment is positive
        if data['new_repayment'] <= Decimal('0'):
            raise serializers.ValidationError({"new_repayment": "Repayment amount must be greater than 0"})
        
        # Ensure new_repayment is less than new_loan_amount
        if data['new_repayment'] >= data['new_loan_amount']:
            raise serializers.ValidationError({"new_repayment": "Repayment amount must be less than loan amount"})
        
        return data


class ApplicationCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating new applications with comprehensive null/blank handling
    """
    borrowers = BorrowerSerializer(many=True, required=False)
    guarantors = GuarantorSerializer(many=True, required=False)
    company_borrowers = CompanyBorrowerSerializer(many=True, required=False)
    security_properties = SecurityPropertySerializer(many=True, required=False)
    loan_requirements = LoanRequirementSerializer(many=True, required=False)
    
    # Add funding calculation input fields
    funding_calculation_input = FundingCalculationInputSerializer(required=False)
    
    # CRITICAL FIX: Explicitly define branch_id and bd_id as write-only fields
    branch_id = serializers.IntegerField(write_only=True, required=False, allow_null=True)
    bd_id = serializers.IntegerField(write_only=True, required=False, allow_null=True)
    
    class Meta:
        model = Application
        fields = [
            'id', 'reference_number', 'loan_amount', 'loan_term', 'capitalised_interest_term',
            'interest_rate', 'purpose', 'repayment_frequency',
            'application_type', 'application_type_other', 'product_id', 'estimated_settlement_date',
            'stage', 'broker', 'branch_id', 'bd_id', 'valuer', 'quantity_surveyor', 'borrowers', 'guarantors',
            'company_borrowers', 'security_properties', 'loan_requirements',
            'loan_purpose', 'additional_comments', 'prior_application',
            'prior_application_details', 'exit_strategy', 'exit_strategy_details',
            'valuer_company_name', 'valuer_contact_name', 'valuer_phone',
            'valuer_email', 'qs_company_name', 'qs_contact_name', 'qs_phone', 'qs_email',
            'funding_calculation_input',
            # General Solvency Enquiries
            'has_pending_litigation', 'has_unsatisfied_judgements', 'has_been_bankrupt',
            'has_been_refused_credit', 'has_outstanding_ato_debt', 'has_outstanding_tax_returns',
            'has_payment_arrangements', 'solvency_enquiries_details'
        ]
        extra_kwargs = {
            # Make most fields optional and allow null/blank values
            'reference_number': {'required': False, 'allow_null': True, 'allow_blank': True},
            'loan_amount': {'required': False, 'allow_null': True},
            'loan_term': {'required': False, 'allow_null': True},
            'capitalised_interest_term': {'required': False, 'allow_null': True},
            'interest_rate': {'required': False, 'allow_null': True},
            'purpose': {'required': False, 'allow_null': True, 'allow_blank': True},
            'repayment_frequency': {'required': False, 'allow_null': True, 'allow_blank': True},
            'application_type': {'required': False, 'allow_null': True, 'allow_blank': True},
            'application_type_other': {'required': False, 'allow_null': True, 'allow_blank': True},
            'product_id': {'required': False, 'allow_null': True, 'allow_blank': True},
            'estimated_settlement_date': {'required': False, 'allow_null': True},
            'stage': {'required': False, 'allow_null': True, 'allow_blank': True},
            'broker': {'required': False, 'allow_null': True},
            'branch_id': {'required': False, 'allow_null': True},
            'bd_id': {'required': False, 'allow_null': True},
            'valuer': {'required': False, 'allow_null': True},
            'quantity_surveyor': {'required': False, 'allow_null': True},
            'loan_purpose': {'required': False, 'allow_null': True, 'allow_blank': True},
            'additional_comments': {'required': False, 'allow_null': True, 'allow_blank': True},
            'prior_application': {'required': False, 'allow_null': True},
            'prior_application_details': {'required': False, 'allow_null': True, 'allow_blank': True},
            'exit_strategy': {'required': False, 'allow_null': True, 'allow_blank': True},
            'exit_strategy_details': {'required': False, 'allow_null': True, 'allow_blank': True},
            'valuer_company_name': {'required': False, 'allow_null': True, 'allow_blank': True},
            'valuer_contact_name': {'required': False, 'allow_null': True, 'allow_blank': True},
            'valuer_phone': {'required': False, 'allow_null': True, 'allow_blank': True},
            'valuer_email': {'required': False, 'allow_null': True, 'allow_blank': True},
            'qs_company_name': {'required': False, 'allow_null': True, 'allow_blank': True},
            'qs_contact_name': {'required': False, 'allow_null': True, 'allow_blank': True},
            'qs_phone': {'required': False, 'allow_null': True, 'allow_blank': True},
            'qs_email': {'required': False, 'allow_null': True, 'allow_blank': True},
            # Solvency fields - allow null since they're nullable BooleanFields
            'has_pending_litigation': {'required': False, 'allow_null': True},
            'has_unsatisfied_judgements': {'required': False, 'allow_null': True},
            'has_been_bankrupt': {'required': False, 'allow_null': True},
            'has_been_refused_credit': {'required': False, 'allow_null': True},
            'has_outstanding_ato_debt': {'required': False, 'allow_null': True},
            'has_outstanding_tax_returns': {'required': False, 'allow_null': True},
            'has_payment_arrangements': {'required': False, 'allow_null': True},
            'solvency_enquiries_details': {'required': False, 'allow_null': True, 'allow_blank': True},
        }
    
    def validate_broker(self, value):
        """
        Validate that the broker ID exists in the database
        """
        if value is not None:
            from brokers.models import Broker
            try:
                Broker.objects.get(id=value.id if hasattr(value, 'id') else value)
            except Broker.DoesNotExist:
                raise serializers.ValidationError(f"Broker with ID {value.id if hasattr(value, 'id') else value} does not exist.")
        return value
    
    def validate_bd_id(self, value):
        """
        Validate that the BDM ID exists in the database
        """
        if value is not None:
            from brokers.models import BDM
            try:
                BDM.objects.get(id=value)
            except BDM.DoesNotExist:
                raise serializers.ValidationError(f"BDM with ID {value} does not exist.")
        return value
    
    def validate_branch_id(self, value):
        """
        Validate that the branch ID exists in the database
        """
        if value is not None:
            from brokers.models import Branch
            try:
                Branch.objects.get(id=value)
            except Branch.DoesNotExist:
                raise serializers.ValidationError(f"Branch with ID {value} does not exist.")
        return value
    
    def validate_valuer(self, value):
        """
        Validate that the valuer ID exists in the database
        """
        if value is not None:
            from ..models import Valuer
            try:
                Valuer.objects.get(id=value.id if hasattr(value, 'id') else value)
            except Valuer.DoesNotExist:
                raise serializers.ValidationError(f"Valuer with ID {value.id if hasattr(value, 'id') else value} does not exist.")
        return value
    
    def validate_quantity_surveyor(self, value):
        """
        Validate that the quantity surveyor ID exists in the database
        """
        if value is not None:
            from ..models import QuantitySurveyor
            try:
                QuantitySurveyor.objects.get(id=value.id if hasattr(value, 'id') else value)
            except QuantitySurveyor.DoesNotExist:
                raise serializers.ValidationError(f"Quantity Surveyor with ID {value.id if hasattr(value, 'id') else value} does not exist.")
        return value

    def create(self, validated_data):
        borrowers_data = validated_data.pop('borrowers', [])
        guarantors_data = validated_data.pop('guarantors', [])
        company_borrowers_data = validated_data.pop('company_borrowers', [])
        security_properties_data = validated_data.pop('security_properties', [])
        loan_requirements_data = validated_data.pop('loan_requirements', [])
        funding_calculation_input = validated_data.pop('funding_calculation_input', None)
        
        # Process new_borrowers data if present in the request
        new_borrowers = validated_data.pop('new_borrowers', [])
        
        # CRITICAL FIX: Handle branch_id and bd_id conversion to foreign key objects
        branch_id = validated_data.pop('branch_id', None)
        bd_id = validated_data.pop('bd_id', None)
        
        # Convert branch_id to branch object
        if branch_id:
            from brokers.models import Branch
            try:
                branch = Branch.objects.get(id=branch_id)
                validated_data['branch'] = branch
            except Branch.DoesNotExist:
                pass  # Already validated in validate_branch_id
        
        # Convert bd_id to bd object  
        if bd_id:
            from brokers.models import BDM
            try:
                bd = BDM.objects.get(id=bd_id)
                validated_data['bd'] = bd
            except BDM.DoesNotExist:
                pass  # Already validated in validate_bd_id
        
        # Clean and validate company borrowers data
        cleaned_company_borrowers = []
        for company_data in company_borrowers_data:
            # Handle directors data - filter out entries with null/empty names
            if 'directors' in company_data:
                valid_directors = []
                for director in company_data['directors']:
                    # Only include directors with valid names
                    if director.get('name') and director['name'].strip():
                        valid_directors.append(director)
                company_data['directors'] = valid_directors
            cleaned_company_borrowers.append(company_data)
        
        # Use transaction to ensure all related entities are created or none
        with transaction.atomic():
            # Create the application
            application = Application.objects.create(**validated_data)
            
            # Create borrowers and link to application
            for borrower_data in borrowers_data:
                borrower_serializer = BorrowerSerializer(data=borrower_data)
                borrower_serializer.is_valid(raise_exception=True)
                borrower = borrower_serializer.save()
                application.borrowers.add(borrower)
            
            # Process new_borrowers if present
            for new_borrower_data in new_borrowers:
                # Create a new borrower
                borrower = Borrower.objects.create(
                    first_name=new_borrower_data.get('first_name', ''),
                    last_name=new_borrower_data.get('last_name', ''),
                    date_of_birth=new_borrower_data.get('date_of_birth'),
                    email=new_borrower_data.get('email', ''),
                    phone=new_borrower_data.get('phone', ''),
                    residential_address=new_borrower_data.get('residential_address', ''),
                    marital_status=new_borrower_data.get('marital_status', ''),
                    residency_status=new_borrower_data.get('residency_status', ''),
                    employment_type=new_borrower_data.get('employment_type', ''),
                    employer_name=new_borrower_data.get('employer_name', ''),
                    annual_income=new_borrower_data.get('annual_income', 0),
                    created_by=validated_data.get('created_by')
                )
                # Add the borrower to the application
                application.borrowers.add(borrower)
            
            # Create guarantors and link to application
            for guarantor_data in guarantors_data:
                guarantor_serializer = GuarantorSerializer(data=guarantor_data)
                guarantor_serializer.is_valid(raise_exception=True)
                guarantor = guarantor_serializer.save(application=application)
                application.guarantors.add(guarantor)
            
            # Process guarantor_data if present
            guarantor_data_list = validated_data.pop('guarantor_data', [])
            for guarantor_data in guarantor_data_list:
                # Create a new guarantor
                guarantor = Guarantor.objects.create(
                    guarantor_type=guarantor_data.get('guarantor_type', ''),
                    first_name=guarantor_data.get('first_name', ''),
                    last_name=guarantor_data.get('last_name', ''),
                    email=guarantor_data.get('email', ''),
                    mobile=guarantor_data.get('mobile', ''),
                    date_of_birth=guarantor_data.get('date_of_birth'),
                    application=application,
                    created_by=validated_data.get('created_by')
                )
                # Add the guarantor to the application
                application.guarantors.add(guarantor)
            
            # Create company borrowers and link to application
            for company_borrower_data in cleaned_company_borrowers:
                try:
                    company_borrower_serializer = CompanyBorrowerSerializer(data=company_borrower_data)
                    if company_borrower_serializer.is_valid():
                        company_borrower = company_borrower_serializer.save()
                        application.borrowers.add(company_borrower)
                    else:
                        # Log validation errors but don't fail the entire transaction
                        import logging
                        logger = logging.getLogger(__name__)
                        logger.warning(f"Company borrower validation errors: {company_borrower_serializer.errors}")
                except Exception as e:
                    # Log the error but continue with other company borrowers
                    import logging
                    logger = logging.getLogger(__name__)
                    logger.error(f"Error creating company borrower: {str(e)}")
            
            # Create security properties
            for security_property_data in security_properties_data:
                security_property_serializer = SecurityPropertySerializer(data=security_property_data)
                security_property_serializer.is_valid(raise_exception=True)
                security_property = security_property_serializer.save(application=application)
            
            # Create loan requirements
            for loan_requirement_data in loan_requirements_data:
                loan_requirement_serializer = LoanRequirementSerializer(data=loan_requirement_data)
                loan_requirement_serializer.is_valid(raise_exception=True)
                loan_requirement = loan_requirement_serializer.save(application=application)
            
            # Handle funding calculation if provided and loan amount is available
            if funding_calculation_input and application.loan_amount:
                try:
                    from ..services import calculate_funding
                    calculation_result, funding_history = calculate_funding(
                        application=application,
                        calculation_input=funding_calculation_input,
                        user=validated_data.get('created_by')
                    )
                except Exception as e:
                    # Log the error but don't fail the application creation
                    import logging
                    logger = logging.getLogger(__name__)
                    logger.error(f"Error performing funding calculation during create: {type(e).__name__}: {str(e)}")
            
            return application


class ApplicationDetailSerializer(serializers.ModelSerializer):
    """
    Comprehensive serializer for application details
    """
    # Basic application fields are included by default
    
    # Related entities - separate individual and company borrowers for clarity
    borrowers = serializers.SerializerMethodField()
    company_borrowers = serializers.SerializerMethodField()
    guarantors = GuarantorSerializer(many=True, read_only=True)
    security_properties = SecurityPropertySerializer(many=True, read_only=True)
    loan_requirements = LoanRequirementSerializer(many=True, read_only=True)
    
    # Documents and notes
    documents = serializers.SerializerMethodField()
    notes = serializers.SerializerMethodField()
    
    # Financial tracking
    fees = serializers.SerializerMethodField()
    repayments = serializers.SerializerMethodField()
    ledger_entries = serializers.SerializerMethodField()
    funding_calculation_history = serializers.SerializerMethodField()
    
    # Related parties
    broker = BrokerSerializer(read_only=True)
    bd = BDMSerializer(read_only=True)
    branch = BranchSerializer(read_only=True)
    valuer = ValuerListSerializer(read_only=True)
    quantity_surveyor = QuantitySurveyorListSerializer(read_only=True)
    
    # Status information
    stage_display = serializers.CharField(source='get_stage_display', read_only=True)
    created_by_details = UserSerializer(source='created_by', read_only=True)
    
    class Meta:
        model = Application
        fields = [
            # Basic fields
            'id', 'reference_number', 'loan_amount', 'loan_term', 'capitalised_interest_term',
            'interest_rate', 'purpose', 'repayment_frequency',
            'application_type', 'application_type_other', 'product_id', 'estimated_settlement_date',
            'stage', 'stage_display', 'created_at', 'updated_at',
            
            # Loan purpose details
            'loan_purpose', 'additional_comments', 'prior_application',
            'prior_application_details',
            
            # Exit strategy
            'exit_strategy', 'exit_strategy_details',
            
            # General Solvency Enquiries
            'has_pending_litigation', 'has_unsatisfied_judgements', 'has_been_bankrupt',
            'has_been_refused_credit', 'has_outstanding_ato_debt', 'has_outstanding_tax_returns',
            'has_payment_arrangements', 'solvency_enquiries_details',
            
            # Related entities - now including separate company_borrowers
            'borrowers', 'company_borrowers', 'guarantors', 'broker', 'bd', 'branch',
            'valuer', 'quantity_surveyor', 'security_properties', 'loan_requirements',
            
            # Documents and notes
            'documents', 'notes',
            
            # Financial tracking
            'fees', 'repayments', 'ledger_entries', 'funding_calculation_history',
            
            # Security property details (legacy fields)
            'security_address', 'security_type', 'security_value',
            
            # Valuer information
            'valuer_company_name', 'valuer_contact_name', 'valuer_phone',
            'valuer_email', 'valuation_date', 'valuation_amount',
            
            # QS information
            'qs_company_name', 'qs_contact_name', 'qs_phone',
            'qs_email', 'qs_report_date',
            
            # Signature and PDF
            'signed_by', 'signature_date', 'uploaded_pdf_path',
            
            # Funding calculation
            'funding_result',
            
            # Metadata
            'created_by_details'
        ]
    
    def get_borrowers(self, obj) -> list:
        """Get individual borrowers (is_company=False) using prefetched data"""
        # Use prefetched borrowers to avoid additional queries
        individual_borrowers = [b for b in obj.borrowers.all() if not b.is_company]
        return BorrowerSerializer(individual_borrowers, many=True, context=self.context).data
    
    def get_company_borrowers(self, obj) -> list:
        """Get company borrowers (is_company=True) using prefetched data"""
        # Use prefetched borrowers to avoid additional queries
        company_borrowers = [b for b in obj.borrowers.all() if b.is_company]
        return CompanyBorrowerSerializer(company_borrowers, many=True, context=self.context).data
    
    def get_documents(self, obj) -> list:
        """Get documents using prefetched data"""
        # Use prefetched documents to avoid additional queries
        if hasattr(obj, '_prefetched_objects_cache') and 'documents' in obj._prefetched_objects_cache:
            documents = obj.documents.all()
        else:
            documents = Document.objects.filter(application=obj)
        return DocumentSerializer(documents, many=True, context=self.context).data
    
    def get_notes(self, obj) -> list:
        """Get notes using prefetched data"""
        # Use prefetched notes to avoid additional queries
        if hasattr(obj, '_prefetched_objects_cache') and 'notes' in obj._prefetched_objects_cache:
            notes = obj.notes.all()
        else:
            notes = Note.objects.filter(application=obj).order_by('-created_at')
        return NoteSerializer(notes, many=True, context=self.context).data
    
    def get_fees(self, obj) -> list:
        """Get fees using prefetched data"""
        # Use prefetched fees to avoid additional queries
        if hasattr(obj, '_prefetched_objects_cache') and 'fees' in obj._prefetched_objects_cache:
            fees = obj.fees.all()
        else:
            fees = Fee.objects.filter(application=obj)
        return FeeSerializer(fees, many=True, context=self.context).data
    
    def get_repayments(self, obj) -> list:
        """Get repayments using prefetched data"""
        # Use prefetched repayments to avoid additional queries
        if hasattr(obj, '_prefetched_objects_cache') and 'repayments' in obj._prefetched_objects_cache:
            repayments = obj.repayments.all()
        else:
            repayments = Repayment.objects.filter(application=obj).order_by('due_date')
        return RepaymentSerializer(repayments, many=True, context=self.context).data
    
    def get_ledger_entries(self, obj) -> list:
        """Get ledger entries using prefetched data"""
        # Use prefetched ledger entries to avoid additional queries
        if hasattr(obj, '_prefetched_objects_cache') and 'ledger_entries' in obj._prefetched_objects_cache:
            ledger_entries = obj.ledger_entries.all()
        else:
            ledger_entries = Ledger.objects.filter(application=obj).order_by('-transaction_date')
        return LedgerSerializer(ledger_entries, many=True, context=self.context).data
    
    def get_funding_calculation_history(self, obj) -> list:
        """Get funding calculation history using prefetched data"""
        from ..models import FundingCalculationHistory
        # Use prefetched funding calculations to avoid additional queries
        if hasattr(obj, '_prefetched_objects_cache') and 'funding_calculations' in obj._prefetched_objects_cache:
            history = obj.funding_calculations.all()
        else:
            history = FundingCalculationHistory.objects.filter(application=obj).order_by('-created_at')
        return FundingCalculationHistorySerializer(history, many=True, context=self.context).data
        
    def to_representation(self, instance):
        data = super().to_representation(instance)
        
        # Ensure all expected fields are present with defaults
        data['borrowers'] = data.get('borrowers', [])
        data['company_borrowers'] = data.get('company_borrowers', [])
        data['guarantors'] = data.get('guarantors', [])
        data['security_properties'] = data.get('security_properties', [])
        data['loan_requirements'] = data.get('loan_requirements', [])
        data['documents'] = data.get('documents', [])
        data['notes'] = data.get('notes', [])
        data['fees'] = data.get('fees', [])
        data['repayments'] = data.get('repayments', [])
        data['ledger_entries'] = data.get('ledger_entries', [])
        
        # Ensure each guarantor has assets and liabilities
        for guarantor in data['guarantors']:
            guarantor['assets'] = guarantor.get('assets', [])
            guarantor['liabilities'] = guarantor.get('liabilities', [])
            
        return data


class ApplicationListSerializer(serializers.ModelSerializer):
    """
    Serializer for listing applications with summary information
    """
    stage_display = serializers.CharField(source='get_stage_display', read_only=True)
    last_stage_change = serializers.SerializerMethodField()
    stage_history_summary = serializers.SerializerMethodField()
    borrower_count = serializers.SerializerMethodField()
    borrower_name = serializers.SerializerMethodField()
    guarantor_name = serializers.SerializerMethodField()
    bdm_name = serializers.SerializerMethodField()
    broker_name = serializers.SerializerMethodField()
    branch_name = serializers.SerializerMethodField()
    security_address = serializers.SerializerMethodField()
    purpose = serializers.CharField(source='loan_purpose', read_only=True)
    product_name = serializers.SerializerMethodField()
    updated_at = serializers.DateTimeField(read_only=True)
    solvency_issues = serializers.SerializerMethodField()
    
    class Meta:
        model = Application
        fields = [
            'id', 'reference_number', 'borrower_name', 'stage', 'stage_display',
            'last_stage_change', 'stage_history_summary',
            'bdm_name', 'broker_name', 'branch_name', 'guarantor_name', 'purpose', 'product_name', 'security_address',
            'loan_amount', 'loan_term', 'capitalised_interest_term', 'estimated_settlement_date', 'updated_at', 'created_at',
            'application_type', 'borrower_count', 'solvency_issues'
        ]
    
    def get_last_stage_change(self, obj):
        """Get information about the last stage change."""
        if not obj.stage_history:
            return None
        last_change = obj.stage_history[-1]
        
        # Handle both old and new stage_history structures
        # Old structure: {'stage': 'old_stage', 'timestamp': ..., 'user': ...}
        # New structure: {'from_stage': 'old_stage', 'to_stage': 'new_stage', 'timestamp': ..., 'user': ..., 'notes': ...}
        
        if 'from_stage' in last_change and 'to_stage' in last_change:
            # New structure
            return {
                'from_stage': dict(Application.STAGE_CHOICES).get(last_change['from_stage'], 'Unknown'),
                'to_stage': dict(Application.STAGE_CHOICES).get(last_change['to_stage'], 'Unknown'),
                'timestamp': last_change['timestamp'],
                'user': last_change['user'],
                'notes': last_change.get('notes', '')
            }
        elif 'stage' in last_change:
            # Old structure - convert to new format
            return {
                'from_stage': dict(Application.STAGE_CHOICES).get(last_change['stage'], 'Unknown'),
                'to_stage': dict(Application.STAGE_CHOICES).get(obj.stage, 'Unknown'),
                'timestamp': last_change['timestamp'],
                'user': last_change['user'],
                'notes': last_change.get('notes', '')
            }
        else:
            # Fallback for unexpected structure
            return {
                'from_stage': 'Unknown',
                'to_stage': dict(Application.STAGE_CHOICES).get(obj.stage, 'Unknown'),
                'timestamp': last_change.get('timestamp', ''),
                'user': last_change.get('user', ''),
                'notes': last_change.get('notes', '')
            }
    
    def get_stage_history_summary(self, obj):
        """Get a summary of stage changes."""
        if not obj.stage_history:
            return []
        
        summary = []
        for change in obj.stage_history[-5:]:  # Return last 5 changes
            # Handle both old and new stage_history structures
            if 'to_stage' in change:
                # New structure
                summary.append({
                    'stage': dict(Application.STAGE_CHOICES).get(change['to_stage'], 'Unknown'),
                    'timestamp': change['timestamp'],
                    'user': change['user']
                })
            elif 'stage' in change:
                # Old structure
                summary.append({
                    'stage': dict(Application.STAGE_CHOICES).get(change['stage'], 'Unknown'),
                    'timestamp': change['timestamp'],
                    'user': change['user']
                })
            else:
                # Fallback for unexpected structure
                summary.append({
                    'stage': 'Unknown',
                    'timestamp': change.get('timestamp', ''),
                    'user': change.get('user', '')
                })
        
        return summary
    
    def get_borrower_count(self, obj) -> int:
        return obj.borrowers.count()
    
    def get_borrower_name(self, obj) -> str:
        """Get the primary borrower name(s)"""
        borrowers = obj.borrowers.all()
        if not borrowers:
            return ""
        
        names = []
        for borrower in borrowers:
            if borrower.is_company:
                if borrower.company_name:
                    names.append(str(borrower.company_name))
            else:
                first_name = str(borrower.first_name) if borrower.first_name else ""
                last_name = str(borrower.last_name) if borrower.last_name else ""
                name = f"{first_name} {last_name}".strip()
                if name:
                    names.append(name)
        
        return ", ".join(names) if names else ""
    
    def get_guarantor_name(self, obj) -> str:
        """Get the guarantor name(s)"""
        guarantors = obj.guarantors.all()
        if not guarantors:
            return ""
        
        names = []
        for guarantor in guarantors:
            first_name = str(guarantor.first_name) if guarantor.first_name else ""
            last_name = str(guarantor.last_name) if guarantor.last_name else ""
            name = f"{first_name} {last_name}".strip()
            if name:
                names.append(name)
        
        return ", ".join(names) if names else ""
    
    def get_bdm_name(self, obj) -> str:
        """Get the BDM name"""
        if hasattr(obj, 'bd') and obj.bd:
            return obj.bd.name
        return ""
    
    def get_broker_name(self, obj) -> str:
        """Get the broker name"""
        if hasattr(obj, 'broker') and obj.broker:
            return obj.broker.name
        return ""
    
    def get_branch_name(self, obj) -> str:
        """Get the branch name"""
        if hasattr(obj, 'branch') and obj.branch:
            return obj.branch.name
        return ""
    
    def get_security_address(self, obj) -> str:
        """Get the security property address"""
        # First try to get from prefetched security_properties
        if hasattr(obj, 'security_properties') and obj.security_properties.all():
            prop = obj.security_properties.all()[0]
            address_parts = [
                str(prop.address_unit) if prop.address_unit else "",
                str(prop.address_street_no) if prop.address_street_no else "",
                str(prop.address_street_name) if prop.address_street_name else "",
                str(prop.address_suburb) if prop.address_suburb else "",
                str(prop.address_state) if prop.address_state else "",
                str(prop.address_postcode) if prop.address_postcode else ""
            ]
            address = " ".join(part for part in address_parts if part)
            return address
        
        # Fall back to legacy field
        return str(obj.security_address) if obj.security_address else ""
    
    def get_product_name(self, obj) -> str:
        """Get the product name"""
        if obj.product_id:
            try:
                from products.models import Product
                product = Product.objects.get(id=obj.product_id)
                return product.name
            except:
                return f"Product {obj.product_id}"
        return ""
        
    def get_solvency_issues(self, obj) -> dict:
        """Get solvency issues summary"""
        serializer = SolvencyEnquiriesSerializer(obj)
        return serializer.data


class ApplicationPartialUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for partial updates of applications with cascade support
    """
    # Use proper serializers instead of JSONField for better validation and processing
    borrowers = serializers.ListField(
        child=serializers.DictField(), 
        required=False, 
        allow_empty=True
    )
    guarantors = serializers.ListField(
        child=serializers.DictField(), 
        required=False, 
        allow_empty=True
    )
    company_borrowers = serializers.ListField(
        child=serializers.DictField(), 
        required=False, 
        allow_empty=True
    )
    security_properties = SecurityPropertySerializer(many=True, required=False, allow_empty=True)
    loan_requirements = LoanRequirementSerializer(many=True, required=False, allow_empty=True)
    
    # Add funding calculation input fields
    funding_calculation_input = FundingCalculationInputSerializer(required=False)
    
    # CRITICAL FIX: Explicitly define branch_id and bd_id as write-only fields
    branch_id = serializers.IntegerField(write_only=True, required=False, allow_null=True)
    bd_id = serializers.IntegerField(write_only=True, required=False, allow_null=True)
    
    class Meta:
        model = Application
        fields = [
            'id', 'reference_number', 'loan_amount', 'loan_term', 'capitalised_interest_term',
            'interest_rate', 'purpose', 'repayment_frequency',
            'application_type', 'application_type_other', 'product_id', 'estimated_settlement_date',
            'stage', 'broker', 'branch_id', 'bd_id', 'valuer', 'quantity_surveyor', 'borrowers', 'guarantors',
            'company_borrowers', 'security_properties', 'loan_requirements',
            'loan_purpose', 'additional_comments', 'prior_application',
            'prior_application_details', 'exit_strategy', 'exit_strategy_details',
            'valuer_company_name', 'valuer_contact_name', 'valuer_phone',
            'valuer_email', 'qs_company_name', 'qs_contact_name', 'qs_phone', 'qs_email',
            'funding_calculation_input',
            # General Solvency Enquiries
            'has_pending_litigation', 'has_unsatisfied_judgements', 'has_been_bankrupt',
            'has_been_refused_credit', 'has_outstanding_ato_debt', 'has_outstanding_tax_returns',
            'has_payment_arrangements', 'solvency_enquiries_details'
        ]
        extra_kwargs = {
            # Make all model fields optional for partial update, excluding explicitly defined nested fields
            field: {'required': False} for field in [
                'id', 'reference_number', 'loan_amount', 'loan_term', 'capitalised_interest_term',
                'interest_rate', 'purpose', 'repayment_frequency',
                'application_type', 'application_type_other', 'product_id', 'estimated_settlement_date',
                'stage', 'broker', 'branch_id', 'bd_id', 'valuer', 'quantity_surveyor',
                'loan_purpose', 'additional_comments', 'prior_application',
                'prior_application_details', 'exit_strategy', 'exit_strategy_details',
                'valuer_company_name', 'valuer_contact_name', 'valuer_phone',
                'valuer_email', 'qs_company_name', 'qs_contact_name', 'qs_phone', 'qs_email',
                'has_pending_litigation', 'has_unsatisfied_judgements', 'has_been_bankrupt',
                'has_been_refused_credit', 'has_outstanding_ato_debt', 'has_outstanding_tax_returns',
                'has_payment_arrangements', 'solvency_enquiries_details'
            ]
        }
    
    def validate_broker(self, value):
        """
        Validate that the broker ID exists in the database
        """
        if value is not None:
            from brokers.models import Broker
            try:
                Broker.objects.get(id=value.id if hasattr(value, 'id') else value)
            except Broker.DoesNotExist:
                raise serializers.ValidationError(f"Broker with ID {value.id if hasattr(value, 'id') else value} does not exist.")
        return value
    
    def validate_bd_id(self, value):
        """
        Validate that the BDM ID exists in the database
        """
        if value is not None:
            from brokers.models import BDM
            try:
                BDM.objects.get(id=value)
            except BDM.DoesNotExist:
                raise serializers.ValidationError(f"BDM with ID {value} does not exist.")
        return value
    
    def validate_branch_id(self, value):
        """
        Validate that the branch ID exists in the database
        """
        if value is not None:
            from brokers.models import Branch
            try:
                Branch.objects.get(id=value)
            except Branch.DoesNotExist:
                raise serializers.ValidationError(f"Branch with ID {value} does not exist.")
        return value
    
    def validate_valuer(self, value):
        """
        Validate that the valuer ID exists in the database
        """
        if value is not None:
            from ..models import Valuer
            try:
                Valuer.objects.get(id=value.id if hasattr(value, 'id') else value)
            except Valuer.DoesNotExist:
                raise serializers.ValidationError(f"Valuer with ID {value.id if hasattr(value, 'id') else value} does not exist.")
        return value
    
    def validate_quantity_surveyor(self, value):
        """
        Validate that the quantity surveyor ID exists in the database
        """
        if value is not None:
            from ..models import QuantitySurveyor
            try:
                QuantitySurveyor.objects.get(id=value.id if hasattr(value, 'id') else value)
            except QuantitySurveyor.DoesNotExist:
                raise serializers.ValidationError(f"Quantity Surveyor with ID {value.id if hasattr(value, 'id') else value} does not exist.")
        return value

    def update(self, instance, validated_data):
        """
        Update the application with cascade support for related objects
        """
        borrowers_data = validated_data.pop('borrowers', None)
        guarantors_data = validated_data.pop('guarantors', None)
        company_borrowers_data = validated_data.pop('company_borrowers', None)
        security_properties_data = validated_data.pop('security_properties', None)
        loan_requirements_data = validated_data.pop('loan_requirements', None)
        funding_calculation_input = validated_data.pop('funding_calculation_input', None)
        
        # CRITICAL FIX: Handle branch_id and bd_id conversion to foreign key objects for updates
        branch_id = validated_data.pop('branch_id', None)
        bd_id = validated_data.pop('bd_id', None)
        
        # Convert branch_id to branch object
        if branch_id:
            from brokers.models import Branch
            try:
                branch = Branch.objects.get(id=branch_id)
                validated_data['branch'] = branch
            except Branch.DoesNotExist:
                pass  # Already validated in validate_branch_id
        
        # Convert bd_id to bd object  
        if bd_id:
            from brokers.models import BDM
            try:
                bd = BDM.objects.get(id=bd_id)
                validated_data['bd'] = bd
            except BDM.DoesNotExist:
                pass  # Already validated in validate_bd_id
        
        # Use transaction to ensure atomicity
        with transaction.atomic():
            # Update the main application fields
            for attr, value in validated_data.items():
                setattr(instance, attr, value)
            instance.save()
            
            # Handle security properties update (cascade)
            if security_properties_data is not None:
                # Clear existing security properties
                instance.security_properties.all().delete()
                
                # Create new security properties
                for security_property_data in security_properties_data:
                    SecurityProperty.objects.create(
                        application=instance,
                        **security_property_data
                    )
            
            # Handle loan requirements update (cascade)
            if loan_requirements_data is not None:
                # Clear existing loan requirements
                instance.loan_requirements.all().delete()
                
                # Create new loan requirements
                for loan_requirement_data in loan_requirements_data:
                    LoanRequirement.objects.create(
                        application=instance,
                        **loan_requirement_data
                    )
            
            # CRITICAL FIX: Handle borrowers and company borrowers update with enhanced validation and error recovery
            individual_borrowers_to_keep = []
            company_borrowers_to_keep = []
            
            # STEP 1: Get existing borrowers as fallback
            existing_individual_borrowers = list(instance.borrowers.filter(is_company=False))
            existing_company_borrowers = list(instance.borrowers.filter(is_company=True))
            
            import logging
            logger = logging.getLogger(__name__)
            
            # STEP 2: Process individual borrowers data with enhanced error handling
            if borrowers_data is not None:
                logger.info(f"Processing {len(borrowers_data)} individual borrowers for application {instance.id}")
                
                try:
                    for idx, borrower_data in enumerate(borrowers_data):
                        if not borrower_data:  # Skip empty dictionaries
                            logger.warning(f"Skipping empty borrower data at index {idx}")
                            continue
                            
                        try:
                            if 'id' in borrower_data and borrower_data['id']:
                                # Update existing borrower
                                borrower_id = borrower_data['id']
                                logger.info(f"Updating existing individual borrower ID: {borrower_id}")
                                
                                try:
                                    borrower = Borrower.objects.get(id=borrower_id, is_company=False)
                                    
                                    # Validate this borrower belongs to this application or is being added
                                    if borrower not in existing_individual_borrowers:
                                        logger.warning(f"Borrower {borrower_id} not currently associated with application {instance.id}, adding...")
                                    
                                    # Update borrower with provided data using serializer for proper validation
                                    borrower_serializer = BorrowerSerializer(borrower, data=borrower_data, partial=True)
                                    if borrower_serializer.is_valid():
                                        borrower = borrower_serializer.save()
                                        individual_borrowers_to_keep.append(borrower)
                                        logger.info(f"Successfully updated individual borrower {borrower_id}")
                                    else:
                                        logger.error(f"Individual borrower validation failed for ID {borrower_id}: {borrower_serializer.errors}")
                                        # Still keep the original borrower if update fails
                                        individual_borrowers_to_keep.append(borrower)
                                        logger.warning(f"Keeping original individual borrower {borrower_id} due to validation failure")
                                except Borrower.DoesNotExist:
                                    logger.warning(f"Individual borrower with ID {borrower_id} not found, creating new...")
                                    # Create new borrower if ID doesn't exist
                                    new_data = {k: v for k, v in borrower_data.items() if k != 'id'}
                                    if new_data:
                                        # Set created_by for new borrowers
                                        if 'request' in self.context:
                                            new_data['created_by'] = self.context['request'].user
                                        
                                        borrower_serializer = BorrowerSerializer(data=new_data)
                                        if borrower_serializer.is_valid():
                                            borrower = borrower_serializer.save()
                                            individual_borrowers_to_keep.append(borrower)
                                            logger.info(f"Created new individual borrower with ID {borrower.id}")
                                        else:
                                            logger.error(f"Failed to create new individual borrower: {borrower_serializer.errors}")
                            else:
                                # Create new borrower
                                logger.info(f"Creating new individual borrower from data: {borrower_data}")
                                if borrower_data:
                                    # Set created_by for new borrowers
                                    if 'request' in self.context:
                                        borrower_data['created_by'] = self.context['request'].user
                                    
                                    borrower_serializer = BorrowerSerializer(data=borrower_data)
                                    if borrower_serializer.is_valid():
                                        borrower = borrower_serializer.save()
                                        individual_borrowers_to_keep.append(borrower)
                                        logger.info(f"Created new individual borrower with ID {borrower.id}")
                                    else:
                                        logger.error(f"Failed to create new individual borrower: {borrower_serializer.errors}")
                        except Exception as e:
                            logger.error(f"Error processing individual borrower at index {idx}: {type(e).__name__}: {str(e)}")
                            # Continue processing other borrowers
                            
                except Exception as e:
                    logger.error(f"Critical error in individual borrowers processing: {type(e).__name__}: {str(e)}")
                    # If there's a critical error, preserve existing borrowers
                    individual_borrowers_to_keep = existing_individual_borrowers
                    logger.warning("Falling back to existing individual borrowers due to processing error")
            else:
                # If no individual borrowers data provided, keep existing ones
                individual_borrowers_to_keep = existing_individual_borrowers
                logger.info(f"No individual borrowers data provided, keeping {len(existing_individual_borrowers)} existing")
            
            # STEP 3: Process company borrowers data with enhanced error handling
            if company_borrowers_data is not None:
                logger.info(f"Processing {len(company_borrowers_data)} company borrowers for application {instance.id}")
                
                try:
                    for idx, company_data in enumerate(company_borrowers_data):
                        if not company_data:  # Skip empty dictionaries
                            logger.warning(f"Skipping empty company data at index {idx}")
                            continue
                            
                        try:
                            if 'id' in company_data and company_data['id']:
                                # Update existing company borrower
                                company_id = company_data['id']
                                logger.info(f"Updating existing company borrower ID: {company_id}")
                                
                                try:
                                    company = Borrower.objects.get(id=company_id, is_company=True)
                                    
                                    # Validate this company belongs to this application or is being added
                                    if company not in existing_company_borrowers:
                                        logger.warning(f"Company borrower {company_id} not currently associated with application {instance.id}, adding...")
                                    
                                    # Use the CompanyBorrowerSerializer to handle the update properly
                                    company_serializer = CompanyBorrowerSerializer(company, data=company_data, partial=True)
                                    if company_serializer.is_valid():
                                        company = company_serializer.save()
                                        company_borrowers_to_keep.append(company)
                                        logger.info(f"Successfully updated company borrower {company_id}")
                                    else:
                                        logger.error(f"Company borrower validation failed for ID {company_id}: {company_serializer.errors}")
                                        # Still keep the original company if update fails
                                        company_borrowers_to_keep.append(company)
                                        logger.warning(f"Keeping original company borrower {company_id} due to validation failure")
                                        
                                except Borrower.DoesNotExist:
                                    logger.warning(f"Company borrower with ID {company_id} not found, creating new...")
                                    # Create new company borrower if ID doesn't exist
                                    new_data = {k: v for k, v in company_data.items() if k != 'id'}
                                    if new_data:
                                        # Set created_by for new company borrowers
                                        if 'request' in self.context:
                                            new_data['created_by'] = self.context['request'].user
                                        
                                        company_serializer = CompanyBorrowerSerializer(data=new_data)
                                        if company_serializer.is_valid():
                                            company = company_serializer.save()
                                            company_borrowers_to_keep.append(company)
                                            logger.info(f"Created new company borrower with ID {company.id}")
                                        else:
                                            logger.error(f"Failed to create new company borrower: {company_serializer.errors}")
                            else:
                                # Create new company borrower
                                logger.info(f"Creating new company borrower from data")
                                if company_data:
                                    # Set created_by for new company borrowers
                                    if 'request' in self.context:
                                        company_data['created_by'] = self.context['request'].user
                                    
                                    company_serializer = CompanyBorrowerSerializer(data=company_data)
                                    if company_serializer.is_valid():
                                        company = company_serializer.save()
                                        company_borrowers_to_keep.append(company)
                                        logger.info(f"Created new company borrower with ID {company.id}")
                                    else:
                                        logger.error(f"Failed to create new company borrower: {company_serializer.errors}")
                        except Exception as e:
                            logger.error(f"Error processing company borrower at index {idx}: {type(e).__name__}: {str(e)}")
                            # Continue processing other company borrowers
                            
                except Exception as e:
                    logger.error(f"Critical error in company borrowers processing: {type(e).__name__}: {str(e)}")
                    import traceback
                    logger.error(f"Traceback: {traceback.format_exc()}")
                    # If there's a critical error, preserve existing company borrowers
                    company_borrowers_to_keep = existing_company_borrowers
                    logger.warning("Falling back to existing company borrowers due to processing error")
            else:
                # If no company borrowers data provided, keep existing ones
                company_borrowers_to_keep = existing_company_borrowers
                logger.info(f"No company borrowers data provided, keeping {len(existing_company_borrowers)} existing")
            
            # STEP 4: Update the borrowers relationship with enhanced validation
            if borrowers_data is not None or company_borrowers_data is not None:
                all_borrowers = individual_borrowers_to_keep + company_borrowers_to_keep
                
                logger.info(f"Updating borrowers relationship: {len(individual_borrowers_to_keep)} individual + {len(company_borrowers_to_keep)} company = {len(all_borrowers)} total")
                
                # Validate that we haven't lost borrowers compared to the original count
                original_count = len(existing_individual_borrowers) + len(existing_company_borrowers)
                
                if len(all_borrowers) < original_count:
                    logger.warning(f"POTENTIAL DATA LOSS: Original borrower count was {original_count}, now {len(all_borrowers)}")
                    
                    # If we've lost borrowers, provide detailed info for debugging
                    original_ids = set([b.id for b in existing_individual_borrowers + existing_company_borrowers])
                    new_ids = set([b.id for b in all_borrowers])
                    lost_ids = original_ids - new_ids
                    
                    if lost_ids:
                        logger.error(f"LOST BORROWER IDs: {list(lost_ids)}")
                        # Optionally, you could restore the lost borrowers here if needed
                        
                instance.borrowers.set(all_borrowers)
                logger.info(f"Successfully updated borrowers relationship for application {instance.id}")
            
            # Handle guarantors update (many-to-many with application reference)
            if guarantors_data is not None:
                try:
                    # Track guarantors to keep
                    guarantors_to_keep = []
                    
                    # Process guarantors data
                    for guarantor_data in guarantors_data:
                        if not guarantor_data:  # Skip empty dictionaries
                            continue
                            
                        if 'id' in guarantor_data and guarantor_data['id']:
                            # Update existing guarantor
                            try:
                                guarantor_id = guarantor_data['id']
                                guarantor = Guarantor.objects.get(id=guarantor_id)
                                # Update guarantor with provided data using serializer for proper validation
                                guarantor_serializer = GuarantorSerializer(guarantor, data=guarantor_data, partial=True)
                                if guarantor_serializer.is_valid():
                                    guarantor = guarantor_serializer.save()
                                    guarantors_to_keep.append(guarantor)
                                else:
                                    logger.error(f"Guarantor validation failed for ID {guarantor_id}: {guarantor_serializer.errors}")
                                    # Still keep the original guarantor if update fails
                                    guarantors_to_keep.append(guarantor)
                                    logger.warning(f"Keeping original guarantor {guarantor_id} due to validation failure")
                            except Guarantor.DoesNotExist:
                                # Create new guarantor if ID doesn't exist
                                new_data = {k: v for k, v in guarantor_data.items() if k != 'id'}
                                if new_data:  # Only create if there's actual data
                                    guarantor_serializer = GuarantorSerializer(data=new_data)
                                    if guarantor_serializer.is_valid():
                                        guarantor = guarantor_serializer.save(application=instance)
                                        guarantors_to_keep.append(guarantor)
                        else:
                            # Create new guarantor
                            if guarantor_data:  # Only create if there's actual data
                                guarantor_serializer = GuarantorSerializer(data=guarantor_data)
                                if guarantor_serializer.is_valid():
                                    guarantor = guarantor_serializer.save(application=instance)
                                    guarantors_to_keep.append(guarantor)
                    
                    # Update the guarantors relationship
                    instance.guarantors.set(guarantors_to_keep)
                except Exception as e:
                    # Log the error but don't fail the entire update
                    logger.error(f"Error updating guarantors: {type(e).__name__}: {str(e)}")
            
            # Perform funding calculation if input is provided and loan amount is available
            if funding_calculation_input and instance.loan_amount:
                from ..services import calculate_funding
                try:
                    calculation_result, funding_history = calculate_funding(
                        application=instance,
                        calculation_input=funding_calculation_input,
                        user=self.context['request'].user if 'request' in self.context else None
                    )
                    
                    # Create note about funding calculation
                    from documents.models import Note
                    Note.objects.create(
                        application=instance,
                        content=f"Funding calculation updated: Total fees ${calculation_result.get('total_fees', 0)}, Funds available ${calculation_result.get('funds_available', 0)}",
                        created_by=self.context['request'].user if 'request' in self.context else None
                    )
                except Exception as e:
                    # Log the error but don't fail the update
                    logger.error(f"Error performing funding calculation during update: {type(e).__name__}: {str(e)}")
            
            return instance 