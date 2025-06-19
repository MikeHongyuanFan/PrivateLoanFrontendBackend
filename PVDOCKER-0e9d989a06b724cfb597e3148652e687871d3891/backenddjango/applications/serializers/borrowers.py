"""
Borrower and Guarantor Serializers

This module contains serializers for borrowers, guarantors, company borrowers,
their assets, liabilities, and related financial information.
"""

from rest_framework import serializers
from borrowers.models import Borrower, Guarantor, Director, Asset, Liability
from ..validators import validate_company_borrower
from django.db import transaction


class AddressSerializer(serializers.Serializer):
    """
    Serializer for address information
    """
    street = serializers.CharField(max_length=255)
    city = serializers.CharField(max_length=100)
    state = serializers.CharField(max_length=100)
    postal_code = serializers.CharField(max_length=20)
    country = serializers.CharField(max_length=100)


class EmploymentInfoSerializer(serializers.Serializer):
    """
    Serializer for employment information
    """
    employer = serializers.CharField(max_length=255)
    position = serializers.CharField(max_length=100)
    income = serializers.DecimalField(max_digits=12, decimal_places=2)
    years_employed = serializers.DecimalField(max_digits=5, decimal_places=2)


class FinancialInfoSerializer(serializers.Serializer):
    """
    Serializer for borrower financial information
    """
    id = serializers.IntegerField(required=False)
    annual_income = serializers.DecimalField(max_digits=12, decimal_places=2, required=False)
    monthly_expenses = serializers.DecimalField(max_digits=12, decimal_places=2, required=False)
    employment_status = serializers.CharField(max_length=100, required=False)
    employment_start_date = serializers.DateField(required=False)


class DirectorSerializer(serializers.ModelSerializer):
    """
    Serializer for company directors
    """
    class Meta:
        model = Director
        fields = ['id', 'name', 'roles', 'director_id']


class AssetSerializer(serializers.ModelSerializer):
    """
    Serializer for borrower assets
    """
    class Meta:
        model = Asset
        fields = ['id', 'asset_type', 'description', 'value', 'amount_owing', 'to_be_refinanced', 'address', 'bg_type']


class LiabilitySerializer(serializers.ModelSerializer):
    """
    Serializer for borrower liabilities
    """
    class Meta:
        model = Liability
        fields = ['id', 'liability_type', 'description', 'amount', 'lender', 'monthly_payment', 'to_be_refinanced', 'bg_type']


class ApplicationLiabilitySerializer(serializers.ModelSerializer):
    """
    Serializer for application-specific liability information
    """
    class Meta:
        model = Liability
        fields = ['id', 'liability_type', 'description', 'amount', 'monthly_payment', 'bg_type']


class GuarantorAssetSerializer(serializers.ModelSerializer):
    """
    Serializer for guarantor assets
    """
    class Meta:
        model = Asset
        fields = ['id', 'asset_type', 'description', 'value', 'amount_owing', 'address', 'bg_type']
        
    def validate(self, data):
        """
        Validate that bg_type is provided and to_be_refinanced is not
        """
        if 'bg_type' not in data or not data['bg_type']:
            raise serializers.ValidationError({"bg_type": "bg_type is required for guarantor assets"})
        
        # Ensure to_be_refinanced is not set for guarantor assets
        data['to_be_refinanced'] = False
        
        return data


class CompanyAssetSerializer(serializers.ModelSerializer):
    """
    Serializer for company assets
    """
    class Meta:
        model = Asset
        fields = ['id', 'asset_type', 'description', 'value', 'amount_owing', 'to_be_refinanced', 'address']
        
    def validate(self, data):
        """
        Validate that bg_type is not provided
        """
        # Ensure bg_type is not set for company assets
        data['bg_type'] = None
        
        return data


class BorrowerSerializer(serializers.ModelSerializer):
    """
    Serializer for individual borrowers
    """
    address = serializers.SerializerMethodField()
    employment_info = serializers.SerializerMethodField()
    
    class Meta:
        model = Borrower
        fields = [
            'id', 'first_name', 'last_name', 'email', 'phone', 'date_of_birth',
            'address', 'employment_info', 'tax_id', 'marital_status',
            'residency_status', 'referral_source', 'tags'
        ]
    
    def get_address(self, obj) -> dict:
        return {
            'street': obj.residential_address or '',
            'city': '',
            'state': '',
            'postal_code': '',
            'country': ''
        }
    
    def get_employment_info(self, obj) -> dict:
        return {
            'employer': obj.employer_name or '',
            'position': obj.job_title or '',
            'income': obj.annual_income or 0,
            'years_employed': obj.employment_duration or 0
        }


class BorrowerUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for updating borrowers with ID preservation
    """
    id = serializers.IntegerField(required=True)
    
    class Meta:
        model = Borrower
        fields = [
            'id', 'first_name', 'last_name', 'email', 'phone', 'date_of_birth',
            'tax_id', 'marital_status', 'residency_status', 'referral_source', 'tags'
        ]
        extra_kwargs = {
            # Make all fields optional for partial update
            field: {'required': False} for field in fields if field != 'id'
        }
    
    def create(self, validated_data):
        address_data = validated_data.pop('address', None)
        employment_data = validated_data.pop('employment_info', None)
        
        borrower = Borrower.objects.create(**validated_data)
        
        # Create address and employment info if provided
        if address_data:
            borrower.residential_address = address_data.get('street', '')
        
        if employment_data:
            borrower.employer_name = employment_data.get('employer', '')
            borrower.job_title = employment_data.get('position', '')
            borrower.annual_income = employment_data.get('income', 0)
            borrower.employment_duration = employment_data.get('years_employed', 0)
        
        borrower.save()
        return borrower


class GuarantorSerializer(serializers.ModelSerializer):
    """
    Serializer for guarantor
    """
    address = AddressSerializer(required=False)
    employment_info = EmploymentInfoSerializer(required=False)
    financial_info = FinancialInfoSerializer(required=False)
    assets = GuarantorAssetSerializer(many=True, required=False, read_only=True)
    liabilities = ApplicationLiabilitySerializer(many=True, required=False, read_only=True)
    
    class Meta:
        model = Guarantor
        fields = [
            'id', 'first_name', 'last_name', 'email', 'mobile', 'home_phone', 'date_of_birth',
            'address', 'assets', 'liabilities', 'employment_info', 'financial_info'
        ]
    
    def to_representation(self, instance):
        data = super().to_representation(instance)
        
        # Calculate total asset value and total liability amount
        total_assets = sum([asset.get('value', 0) or 0 for asset in data.get('assets', [])])
        total_liabilities = sum([liability.get('amount', 0) or 0 for liability in data.get('liabilities', [])])
        
        data['total_assets'] = total_assets
        data['total_liabilities'] = total_liabilities
        
        return data
    
    def create(self, validated_data):
        with transaction.atomic():
            # Handle nested assets and liabilities
            assets_data = validated_data.pop('assets', [])
            liabilities_data = validated_data.pop('liabilities', [])
            
            guarantor = Guarantor.objects.create(**validated_data)
            
            # Create assets
            for asset_data in assets_data:
                asset_data['guarantor'] = guarantor
                Asset.objects.create(**asset_data)
            
            # Create liabilities
            for liability_data in liabilities_data:
                liability_data['guarantor'] = guarantor
                Liability.objects.create(**liability_data)
        
        return guarantor


class CompanyBorrowerSerializer(serializers.ModelSerializer):
    """
    Serializer for company borrower
    """
    directors = DirectorSerializer(many=True, required=False)
    address = AddressSerializer(required=False)
    assets = CompanyAssetSerializer(many=True, required=False)
    
    class Meta:
        model = Borrower
        fields = [
            'id', 'company_name', 'company_abn', 'company_acn', 'industry_type',
            'annual_company_income', 
            'registered_address_unit', 'registered_address_street_no', 'registered_address_street_name',
            'registered_address_suburb', 'registered_address_state', 'registered_address_postcode',
            'directors', 'address', 'assets'
        ]
    
    def validate(self, data):
        # Use the custom validator for company borrower
        errors = validate_company_borrower(data)
        if errors:
            raise serializers.ValidationError(errors)
        return data
    
    def create(self, validated_data):
        with transaction.atomic():
            # Handle nested data
            directors_data = validated_data.pop('directors', [])
            assets_data = validated_data.pop('assets', [])
            
            # Set borrower type to company
            validated_data['borrower_type'] = 'company'
            
            # Create the borrower
            borrower = Borrower.objects.create(**validated_data)
            
            # Create directors
            for director_data in directors_data:
                director_data['borrower'] = borrower
                Director.objects.create(**director_data)
            
            # Create assets
            for asset_data in assets_data:
                asset_data['borrower'] = borrower
                Asset.objects.create(**asset_data)
        
        return borrower 