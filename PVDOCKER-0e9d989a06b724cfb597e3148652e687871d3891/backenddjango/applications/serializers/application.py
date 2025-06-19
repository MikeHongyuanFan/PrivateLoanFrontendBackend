"""
Application Serializers

This module contains serializers for the core Application model,
including create, detail, list, and various update serializers.
"""

from rest_framework import serializers
from django.db import transaction
from decimal import Decimal

from ..models import Application, SecurityProperty, LoanRequirement
from borrowers.models import Borrower, Guarantor
from users.serializers import UserSerializer
from brokers.serializers import BrokerDetailSerializer as BrokerSerializer, BDMSerializer, BranchSerializer
from documents.models import Document, Fee, Repayment, Note, Ledger
from documents.serializers import DocumentSerializer, NoteSerializer, FeeSerializer, RepaymentSerializer, LedgerSerializer

# Import from other serializer modules
from .borrowers import BorrowerSerializer, GuarantorSerializer, CompanyBorrowerSerializer
from .property import SecurityPropertySerializer, LoanRequirementSerializer
from .funding import FundingCalculationInputSerializer
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
    """
    stage = serializers.ChoiceField(choices=Application.STAGE_CHOICES)
    notes = serializers.CharField(required=False, allow_blank=True)


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
    Serializer for creating new applications
    """
    borrowers = BorrowerSerializer(many=True, required=False)
    guarantors = GuarantorSerializer(many=True, required=False)
    company_borrowers = CompanyBorrowerSerializer(many=True, required=False)
    security_properties = SecurityPropertySerializer(many=True, required=False)
    loan_requirements = LoanRequirementSerializer(many=True, required=False)
    
    # Add funding calculation input fields
    funding_calculation_input = FundingCalculationInputSerializer(required=False)
    
    class Meta:
        model = Application
        fields = [
            'id', 'reference_number', 'loan_amount', 'loan_term', 'capitalised_interest_term',
            'interest_rate', 'purpose', 'repayment_frequency',
            'application_type', 'application_type_other', 'product_id', 'estimated_settlement_date',
            'stage', 'branch_id', 'bd_id', 'valuer', 'quantity_surveyor', 'borrowers', 'guarantors',
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
    
    def create(self, validated_data):
        borrowers_data = validated_data.pop('borrowers', [])
        guarantors_data = validated_data.pop('guarantors', [])
        company_borrowers_data = validated_data.pop('company_borrowers', [])
        security_properties_data = validated_data.pop('security_properties', [])
        loan_requirements_data = validated_data.pop('loan_requirements', [])
        funding_calculation_input = validated_data.pop('funding_calculation_input', None)
        
        # Process new_borrowers data if present in the request
        new_borrowers = validated_data.pop('new_borrowers', [])
        
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
                    title=guarantor_data.get('title', ''),
                    first_name=guarantor_data.get('first_name', ''),
                    last_name=guarantor_data.get('last_name', ''),
                    date_of_birth=guarantor_data.get('date_of_birth'),
                    drivers_licence_no=guarantor_data.get('drivers_licence_no', ''),
                    home_phone=guarantor_data.get('home_phone', ''),
                    mobile=guarantor_data.get('mobile', ''),
                    email=guarantor_data.get('email', ''),
                    address_unit=guarantor_data.get('address_unit', ''),
                    address_street_no=guarantor_data.get('address_street_no', ''),
                    address_street_name=guarantor_data.get('address_street_name', ''),
                    address_suburb=guarantor_data.get('address_suburb', ''),
                    address_state=guarantor_data.get('address_state', ''),
                    address_postcode=guarantor_data.get('address_postcode', ''),
                    occupation=guarantor_data.get('occupation', ''),
                    employer_name=guarantor_data.get('employer_name', ''),
                    employment_type=guarantor_data.get('employment_type', ''),
                    annual_income=guarantor_data.get('annual_income', 0),
                    application=application,
                    created_by=validated_data.get('created_by')
                )
                # If borrower_id is provided, link the guarantor to the borrower
                borrower_id = guarantor_data.get('borrower_id')
                if borrower_id:
                    try:
                        borrower = Borrower.objects.get(id=borrower_id)
                        guarantor.borrower = borrower
                        guarantor.save()
                    except Borrower.DoesNotExist:
                        pass
            
            # Create company borrowers and link to application
            for company_data in company_borrowers_data:
                company_serializer = CompanyBorrowerSerializer(data=company_data)
                company_serializer.is_valid(raise_exception=True)
                company = company_serializer.save()
                application.borrowers.add(company)  # Add to borrowers since it's a Borrower model with is_company=True
            
            # Create security properties
            for security_property_data in security_properties_data:
                SecurityProperty.objects.create(
                    application=application,
                    **security_property_data
                )
            
            # Create loan requirements
            for loan_requirement_data in loan_requirements_data:
                LoanRequirement.objects.create(
                    application=application,
                    **loan_requirement_data
                )
            
            application.save()
            
            # Perform funding calculation if input is provided
            if funding_calculation_input and application.loan_amount and application.interest_rate and application.security_value:
                from ..services import calculate_funding
                try:
                    calculation_result, funding_history = calculate_funding(
                        application=application,
                        calculation_input=funding_calculation_input,
                        user=validated_data.get('created_by')
                    )
                    
                    # Create note about funding calculation
                    Note.objects.create(
                        application=application,
                        content=f"Initial funding calculation performed: Total fees ${calculation_result['total_fees']}, Funds available ${calculation_result['funds_available']}",
                        created_by=validated_data.get('created_by')
                    )
                except Exception as e:
                    # Log the error but don't fail the application creation
                    import logging
                    logger = logging.getLogger(__name__)
                    logger.error(f"Error performing initial funding calculation: {str(e)}")
            
            # Create notification for new application
            from users.models import Notification
            if application.bd_id:
                Notification.objects.create(
                    user_id=application.bd_id,  # Notify the BD
                    title=f"New Application: {application.reference_number}",
                    message=f"A new loan application has been submitted with reference {application.reference_number}",
                    notification_type="application_created",
                    related_object_id=application.id
                )
            
            return application


class ApplicationDetailSerializer(serializers.ModelSerializer):
    """
    Comprehensive serializer for application details
    """
    # Basic application fields are included by default
    
    # Related entities
    borrowers = BorrowerSerializer(many=True, read_only=True)
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
            
            # Related entities
            'borrowers', 'guarantors', 'broker', 'bd', 'branch',
            'valuer', 'quantity_surveyor', 'security_properties', 'loan_requirements',
            
            # Documents and notes
            'documents', 'notes',
            
            # Financial tracking
            'fees', 'repayments', 'ledger_entries',
            
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
    
    def get_documents(self, obj) -> list:
        documents = Document.objects.filter(application=obj)
        return DocumentSerializer(documents, many=True, context=self.context).data
    
    def get_notes(self, obj) -> list:
        notes = Note.objects.filter(application=obj).order_by('-created_at')
        return NoteSerializer(notes, many=True, context=self.context).data
    
    def get_fees(self, obj) -> list:
        fees = Fee.objects.filter(application=obj)
        return FeeSerializer(fees, many=True, context=self.context).data
    
    def get_repayments(self, obj) -> list:
        repayments = Repayment.objects.filter(application=obj).order_by('due_date')
        return RepaymentSerializer(repayments, many=True, context=self.context).data
    
    def get_ledger_entries(self, obj) -> list:
        ledger_entries = Ledger.objects.filter(application=obj).order_by('-transaction_date')
        return LedgerSerializer(ledger_entries, many=True, context=self.context).data
        
    def to_representation(self, instance):
        data = super().to_representation(instance)
        
        # Ensure all expected fields are present with defaults
        data['borrowers'] = data.get('borrowers', [])
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
    borrower_count = serializers.SerializerMethodField()
    borrower_name = serializers.SerializerMethodField()
    guarantor_name = serializers.SerializerMethodField()
    bdm_name = serializers.SerializerMethodField()
    security_address = serializers.SerializerMethodField()
    purpose = serializers.CharField(source='loan_purpose', read_only=True)
    product_name = serializers.SerializerMethodField()
    updated_at = serializers.DateTimeField(read_only=True)
    solvency_issues = serializers.SerializerMethodField()
    
    class Meta:
        model = Application
        fields = [
            'id', 'reference_number', 'borrower_name', 'stage', 'stage_display',
            'bdm_name', 'guarantor_name', 'purpose', 'product_name', 'security_address',
            'loan_amount', 'loan_term', 'capitalised_interest_term', 'estimated_settlement_date', 'updated_at', 'created_at',
            'application_type', 'borrower_count', 'solvency_issues'
        ]
    
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
                    names.append(borrower.company_name)
            else:
                name = f"{borrower.first_name} {borrower.last_name}".strip()
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
            name = f"{guarantor.first_name} {guarantor.last_name}".strip()
            if name:
                names.append(name)
        
        return ", ".join(names) if names else ""
    
    def get_bdm_name(self, obj) -> str:
        """Get the BDM name"""
        if hasattr(obj, 'bd') and obj.bd:
            return obj.bd.name
        return ""
    
    def get_security_address(self, obj) -> str:
        """Get the security property address"""
        # First try to get from security_properties
        security_properties = SecurityProperty.objects.filter(application=obj)
        if security_properties:
            prop = security_properties[0]
            address_parts = [
                prop.address_unit,
                prop.address_street_no,
                prop.address_street_name,
                prop.address_suburb,
                prop.address_state,
                prop.address_postcode
            ]
            address = " ".join(part for part in address_parts if part)
            return address
        
        # Fall back to legacy field
        return obj.security_address or ""
    
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
    borrowers = serializers.ListField(child=serializers.JSONField(), required=False)
    guarantors = serializers.ListField(child=serializers.JSONField(), required=False)
    company_borrowers = serializers.ListField(child=serializers.JSONField(), required=False)
    security_properties = SecurityPropertySerializer(many=True, required=False)
    loan_requirements = LoanRequirementSerializer(many=True, required=False)
    
    # Add funding calculation input fields
    funding_calculation_input = FundingCalculationInputSerializer(required=False)
    
    class Meta:
        model = Application
        fields = [
            'id', 'reference_number', 'loan_amount', 'loan_term', 'capitalised_interest_term',
            'interest_rate', 'purpose', 'repayment_frequency',
            'application_type', 'application_type_other', 'product_id', 'estimated_settlement_date',
            'stage', 'branch_id', 'bd_id', 'valuer', 'quantity_surveyor', 'borrowers', 'guarantors',
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
            # Make all fields optional for partial update
            field: {'required': False} for field in fields
        }
    
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
            
            # Handle borrowers update (many-to-many)
            if borrowers_data is not None:
                # Track borrowers to keep
                borrowers_to_keep = []
                
                # Process borrowers data
                for borrower_data in borrowers_data:
                    if 'id' in borrower_data:
                        # Update existing borrower
                        try:
                            borrower_id = borrower_data['id']
                            borrower = Borrower.objects.get(id=borrower_id)
                            # Update borrower with provided data
                            for attr, value in borrower_data.items():
                                if attr != 'id':  # Skip the ID field
                                    setattr(borrower, attr, value)
                            borrower.save()
                            borrowers_to_keep.append(borrower)
                        except Borrower.DoesNotExist:
                            # Create new borrower if ID doesn't exist
                            new_data = {k: v for k, v in borrower_data.items() if k != 'id'}
                            borrower_serializer = BorrowerSerializer(data=new_data)
                            borrower_serializer.is_valid(raise_exception=True)
                            borrower = borrower_serializer.save()
                            borrowers_to_keep.append(borrower)
                    else:
                        # Create new borrower
                        borrower_serializer = BorrowerSerializer(data=borrower_data)
                        borrower_serializer.is_valid(raise_exception=True)
                        borrower = borrower_serializer.save()
                        borrowers_to_keep.append(borrower)
                
                # Update the borrowers relationship
                instance.borrowers.set(borrowers_to_keep)
            
            # Handle guarantors update (many-to-many with application reference)
            if guarantors_data is not None:
                # Track guarantors to keep
                guarantors_to_keep = []
                
                # Process guarantors data
                for guarantor_data in guarantors_data:
                    if 'id' in guarantor_data:
                        # Update existing guarantor
                        try:
                            guarantor_id = guarantor_data['id']
                            guarantor = Guarantor.objects.get(id=guarantor_id)
                            # Update guarantor with provided data
                            for attr, value in guarantor_data.items():
                                if attr != 'id':  # Skip the ID field
                                    setattr(guarantor, attr, value)
                            guarantor.save()
                            guarantors_to_keep.append(guarantor)
                        except Guarantor.DoesNotExist:
                            # Create new guarantor if ID doesn't exist
                            new_data = {k: v for k, v in guarantor_data.items() if k != 'id'}
                            guarantor_serializer = GuarantorSerializer(data=new_data)
                            guarantor_serializer.is_valid(raise_exception=True)
                            guarantor = guarantor_serializer.save(application=instance)
                            guarantors_to_keep.append(guarantor)
                    else:
                        # Create new guarantor
                        guarantor_serializer = GuarantorSerializer(data=guarantor_data)
                        guarantor_serializer.is_valid(raise_exception=True)
                        guarantor = guarantor_serializer.save(application=instance)
                        guarantors_to_keep.append(guarantor)
                
                # Update the guarantors relationship
                instance.guarantors.set(guarantors_to_keep)
            
            # Handle company borrowers update
            if company_borrowers_data is not None:
                # Track company borrowers to keep
                company_borrowers_to_keep = []
                
                # Process company borrowers data
                for company_data in company_borrowers_data:
                    if 'id' in company_data:
                        # Update existing company borrower
                        try:
                            company_id = company_data['id']
                            company = Borrower.objects.get(id=company_id, is_company=True)
                            # Update company with provided data
                            for attr, value in company_data.items():
                                if attr != 'id':  # Skip the ID field
                                    setattr(company, attr, value)
                            company.save()
                            company_borrowers_to_keep.append(company)
                        except Borrower.DoesNotExist:
                            # Create new company borrower if ID doesn't exist
                            new_data = {k: v for k, v in company_data.items() if k != 'id'}
                            company_serializer = CompanyBorrowerSerializer(data=new_data)
                            company_serializer.is_valid(raise_exception=True)
                            company = company_serializer.save()
                            company_borrowers_to_keep.append(company)
                    else:
                        # Create new company borrower
                        company_serializer = CompanyBorrowerSerializer(data=company_data)
                        company_serializer.is_valid(raise_exception=True)
                        company = company_serializer.save()
                        company_borrowers_to_keep.append(company)
                
                # Get existing non-company borrowers
                individual_borrowers = list(instance.borrowers.filter(is_company=False))
                
                # Update the borrowers relationship to include both individual and company borrowers
                instance.borrowers.set(individual_borrowers + company_borrowers_to_keep)
            
            # Perform funding calculation if input is provided
            if funding_calculation_input:
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
                    import logging
                    logger = logging.getLogger(__name__)
                    logger.error(f"Error performing funding calculation during update: {str(e)}")
            
            return instance 