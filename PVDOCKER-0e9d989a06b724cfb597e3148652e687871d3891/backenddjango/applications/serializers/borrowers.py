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
    Serializer for address information with optional fields for minimal data creation
    """
    street = serializers.CharField(max_length=255, required=False, allow_null=True, allow_blank=True)
    city = serializers.CharField(max_length=100, required=False, allow_null=True, allow_blank=True)
    state = serializers.CharField(max_length=100, required=False, allow_null=True, allow_blank=True)
    postal_code = serializers.CharField(max_length=20, required=False, allow_null=True, allow_blank=True)
    country = serializers.CharField(max_length=100, required=False, allow_null=True, allow_blank=True)


class EmploymentInfoSerializer(serializers.Serializer):
    """
    Serializer for employment information with optional fields for minimal data creation
    """
    employer = serializers.CharField(max_length=255, required=False, allow_null=True, allow_blank=True)
    position = serializers.CharField(max_length=100, required=False, allow_null=True, allow_blank=True)
    income = serializers.DecimalField(max_digits=12, decimal_places=2, required=False, allow_null=True)
    years_employed = serializers.DecimalField(max_digits=5, decimal_places=2, required=False, allow_null=True)


class FinancialInfoSerializer(serializers.Serializer):
    """
    Serializer for borrower financial information with optional fields for minimal data creation
    """
    id = serializers.IntegerField(required=False)
    annual_income = serializers.DecimalField(max_digits=12, decimal_places=2, required=False, allow_null=True)
    monthly_expenses = serializers.DecimalField(max_digits=12, decimal_places=2, required=False, allow_null=True)
    employment_status = serializers.CharField(max_length=100, required=False, allow_null=True, allow_blank=True)
    employment_start_date = serializers.DateField(required=False, allow_null=True)


class DirectorSerializer(serializers.ModelSerializer):
    """
    Serializer for company directors with optional fields for minimal data creation
    """
    class Meta:
        model = Director
        fields = ['id', 'name', 'roles', 'director_id']
        extra_kwargs = {
            # Make most fields optional and allow null/blank values for minimal data creation
            'name': {'required': False, 'allow_null': True, 'allow_blank': True},
            'roles': {'required': False, 'allow_null': True, 'allow_blank': True},
            'director_id': {'required': False, 'allow_null': True, 'allow_blank': True},
        }


class AssetSerializer(serializers.ModelSerializer):
    """
    Unified serializer for all assets (borrower, guarantor, company) using the same Asset table
    """
    class Meta:
        model = Asset
        fields = ['id', 'asset_type', 'description', 'value', 'amount_owing', 'to_be_refinanced', 'address', 'bg_type']
        extra_kwargs = {
            # Make most fields optional and allow null/blank values for minimal data creation
            'asset_type': {'required': False, 'allow_null': True, 'allow_blank': True},
            'description': {'required': False, 'allow_null': True, 'allow_blank': True},
            'value': {'required': False, 'allow_null': True},
            'amount_owing': {'required': False, 'allow_null': True},
            'to_be_refinanced': {'required': False, 'allow_null': True},
            'address': {'required': False, 'allow_null': True, 'allow_blank': True},
            'bg_type': {'required': False, 'allow_null': True, 'allow_blank': True},
        }
    
    def validate(self, data):
        """
        Validate asset data based on context (guarantor vs company)
        """
        # Determine context from the instance or creation data
        is_guarantor_asset = False
        is_company_asset = False
        
        # Check if this is for a guarantor (from context or existing instance)
        if hasattr(self, 'instance') and self.instance:
            is_guarantor_asset = bool(self.instance.guarantor)
            is_company_asset = bool(self.instance.borrower and self.instance.borrower.is_company)
        elif hasattr(self, 'context') and 'guarantor' in self.context:
            is_guarantor_asset = True
        elif hasattr(self, 'context') and 'company_borrower' in self.context:
            is_company_asset = True
        
        # Apply validation rules based on context
        if is_guarantor_asset:
            # For guarantor assets: ensure to_be_refinanced is False, set default bg_type
            data['to_be_refinanced'] = False
            if 'bg_type' not in data or not data['bg_type']:
                data['bg_type'] = 'BG1'  # Default to BG1 if not specified
        elif is_company_asset:
            # For company assets: ensure bg_type is None
            data['bg_type'] = None
        
        return data

    def to_representation(self, instance):
        """
        Customize representation based on asset type
        """
        data = super().to_representation(instance)
        
        # Remove fields that shouldn't be shown based on context
        if instance.guarantor:
            # For guarantor assets, don't show to_be_refinanced
            data.pop('to_be_refinanced', None)
        elif instance.borrower and instance.borrower.is_company:
            # For company assets, don't show bg_type
            data.pop('bg_type', None)
        
        return data


class LiabilitySerializer(serializers.ModelSerializer):
    """
    Unified serializer for all liabilities (borrower, guarantor, company) using the same Liability table
    """
    class Meta:
        model = Liability
        fields = ['id', 'liability_type', 'description', 'amount', 'lender', 'monthly_payment', 'to_be_refinanced', 'bg_type']
        extra_kwargs = {
            # Make most fields optional and allow null/blank values for minimal data creation
            'liability_type': {'required': False, 'allow_null': True, 'allow_blank': True},
            'description': {'required': False, 'allow_null': True, 'allow_blank': True},
            'amount': {'required': False, 'allow_null': True},
            'lender': {'required': False, 'allow_null': True, 'allow_blank': True},
            'monthly_payment': {'required': False, 'allow_null': True},
            'to_be_refinanced': {'required': False, 'allow_null': True},
            'bg_type': {'required': False, 'allow_null': True, 'allow_blank': True},
        }
    
    def validate(self, data):
        """
        Validate liability data based on context (guarantor vs company)
        """
        # Determine context from the instance or creation data
        is_guarantor_liability = False
        
        # Check if this is for a guarantor (from context or existing instance)
        if hasattr(self, 'instance') and self.instance:
            is_guarantor_liability = bool(self.instance.guarantor)
        elif hasattr(self, 'context') and 'guarantor' in self.context:
            is_guarantor_liability = True
        
        # Apply validation rules based on context
        if is_guarantor_liability:
            # For guarantor liabilities: set default bg_type if not provided
            if 'bg_type' not in data or not data['bg_type']:
                data['bg_type'] = 'bg1'  # Default to bg1 if not specified
        
        return data


# Keep these as aliases for backward compatibility during transition
GuarantorAssetSerializer = AssetSerializer
CompanyAssetSerializer = AssetSerializer
ApplicationLiabilitySerializer = LiabilitySerializer


class BorrowerSerializer(serializers.ModelSerializer):
    """
    Serializer for individual borrowers with null/blank handling for minimal data creation
    """
    address = serializers.SerializerMethodField()
    employment_info = serializers.SerializerMethodField()
    assets = AssetSerializer(many=True, read_only=True)
    liabilities = LiabilitySerializer(many=True, read_only=True)
    
    class Meta:
        model = Borrower
        fields = [
            'id', 'first_name', 'last_name', 'email', 'phone', 'date_of_birth',
            'address', 'employment_info', 'tax_id', 'marital_status',
            'residency_status', 'referral_source', 'tags', 'assets', 'liabilities',
            # Direct employment fields  
            'employment_type', 'employer_name', 'job_title', 'annual_income', 
            'employment_duration', 'employer_address',
            # Additional financial fields
            'other_income', 'monthly_expenses', 'mailing_address'
        ]
        extra_kwargs = {
            # Make most fields optional and allow null/blank values for minimal data creation
            'first_name': {'required': False, 'allow_null': True, 'allow_blank': True},
            'last_name': {'required': False, 'allow_null': True, 'allow_blank': True},
            'email': {'required': False, 'allow_null': True, 'allow_blank': True},
            'phone': {'required': False, 'allow_null': True, 'allow_blank': True},
            'date_of_birth': {'required': False, 'allow_null': True},
            'tax_id': {'required': False, 'allow_null': True, 'allow_blank': True},
            'marital_status': {'required': False, 'allow_null': True, 'allow_blank': True},
            'residency_status': {'required': False, 'allow_null': True, 'allow_blank': True},
            'referral_source': {'required': False, 'allow_null': True, 'allow_blank': True},
            'tags': {'required': False, 'allow_null': True, 'allow_blank': True},
            'mailing_address': {'required': False, 'allow_null': True, 'allow_blank': True},
            # Employment fields
            'employment_type': {'required': False, 'allow_null': True, 'allow_blank': True},
            'employer_name': {'required': False, 'allow_null': True, 'allow_blank': True},
            'job_title': {'required': False, 'allow_null': True, 'allow_blank': True},
            'annual_income': {'required': False, 'allow_null': True},
            'employment_duration': {'required': False, 'allow_null': True},
            'employer_address': {'required': False, 'allow_null': True, 'allow_blank': True},
            # Financial fields
            'other_income': {'required': False, 'allow_null': True},
            'monthly_expenses': {'required': False, 'allow_null': True},
        }
    
    def get_address(self, obj) -> dict:
        # Try to parse structured address from residential_address if it contains delimiters
        if obj.residential_address:
            # Simple parsing - you can enhance this logic
            address_parts = obj.residential_address.split(', ') if ', ' in obj.residential_address else [obj.residential_address]
            
            return {
                'street': address_parts[0] if len(address_parts) > 0 else '',
                'city': address_parts[1] if len(address_parts) > 1 else '',
                'state': address_parts[2] if len(address_parts) > 2 else '',
                'postal_code': address_parts[3] if len(address_parts) > 3 else '',
                'country': address_parts[4] if len(address_parts) > 4 else ''
            }
        
        return {
            'street': '',
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
    
    def create(self, validated_data):
        """
        Create borrower with proper created_by attribution
        """
        # Handle nested address and employment data if provided
        address_data = validated_data.pop('address', None)
        employment_data = validated_data.pop('employment_info', None)
        
        # Ensure is_company is False for individual borrowers
        validated_data['is_company'] = False
        
        # Set created_by if not already provided and available from context
        if 'created_by' not in validated_data and hasattr(self, 'context') and 'request' in self.context:
            validated_data['created_by'] = self.context['request'].user
        
        # Create the borrower instance
        borrower = super().create(validated_data)
        
        # Handle nested address data
        if address_data:
            # Combine structured address data into residential_address field
            address_parts = []
            if address_data.get('street'):
                address_parts.append(address_data.get('street'))
            if address_data.get('city'):
                address_parts.append(address_data.get('city'))
            if address_data.get('state'):
                address_parts.append(address_data.get('state'))
            if address_data.get('postal_code'):
                address_parts.append(address_data.get('postal_code'))
            if address_data.get('country'):
                address_parts.append(address_data.get('country'))
            
            if address_parts:
                borrower.residential_address = ', '.join(address_parts)
                borrower.save()
        
        # Handle nested employment data
        if employment_data:
            if employment_data.get('employer'):
                borrower.employer_name = employment_data.get('employer', '')
            if employment_data.get('position'):
                borrower.job_title = employment_data.get('position', '')
            if employment_data.get('income') is not None:
                borrower.annual_income = employment_data.get('income')
            if employment_data.get('years_employed') is not None:
                borrower.employment_duration = employment_data.get('years_employed')
            borrower.save()
        
        return borrower
    
    def update(self, instance, validated_data):
        """
        Update borrower with support for nested address and employment data
        """
        import logging
        logger = logging.getLogger(__name__)
        
        logger.info(f"Updating borrower {instance.id} with data: {list(validated_data.keys())}")
        
        # Handle nested address and employment data if provided
        address_data = validated_data.pop('address', None)
        employment_data = validated_data.pop('employment_info', None)
        
        if address_data:
            logger.info(f"Processing nested address data: {address_data}")
        if employment_data:
            logger.info(f"Processing nested employment data: {employment_data}")
        
        # Log direct field updates
        address_fields = ['residential_address', 'mailing_address']
        employment_fields = ['employment_type', 'employer_name', 'job_title', 'annual_income', 'employment_duration', 'employer_address']
        
        for field in address_fields + employment_fields:
            if field in validated_data:
                logger.info(f"Direct field update - {field}: {validated_data.get(field)}")
        
        # Update instance with regular fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        # Handle nested address data
        if address_data:
            # Combine structured address data into residential_address field
            address_parts = []
            if address_data.get('street'):
                address_parts.append(address_data.get('street'))
            if address_data.get('city'):
                address_parts.append(address_data.get('city'))
            if address_data.get('state'):
                address_parts.append(address_data.get('state'))
            if address_data.get('postal_code'):
                address_parts.append(address_data.get('postal_code'))
            if address_data.get('country'):
                address_parts.append(address_data.get('country'))
            
            if address_parts:
                instance.residential_address = ', '.join(address_parts)
                logger.info(f"Updated residential_address from nested data: {instance.residential_address}")
        
        # Handle nested employment data
        if employment_data:
            if 'employer' in employment_data:
                instance.employer_name = employment_data.get('employer', '')
                logger.info(f"Updated employer_name from nested data: {instance.employer_name}")
            if 'position' in employment_data:
                instance.job_title = employment_data.get('position', '')
                logger.info(f"Updated job_title from nested data: {instance.job_title}")
            if 'income' in employment_data:
                instance.annual_income = employment_data.get('income')
                logger.info(f"Updated annual_income from nested data: {instance.annual_income}")
            if 'years_employed' in employment_data:
                instance.employment_duration = employment_data.get('years_employed')
                logger.info(f"Updated employment_duration from nested data: {instance.employment_duration}")
        
        instance.save()
        logger.info(f"Borrower {instance.id} update completed. Address: {instance.residential_address}, Employer: {instance.employer_name}")
        return instance


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
    Serializer for guarantor with null/blank handling for minimal data creation
    """
    address = AddressSerializer(required=False)
    employment_info = EmploymentInfoSerializer(required=False)
    financial_info = FinancialInfoSerializer(required=False)
    assets = AssetSerializer(many=True, required=False)
    liabilities = LiabilitySerializer(many=True, required=False)
    
    class Meta:
        model = Guarantor
        fields = [
            'id', 'guarantor_type', 'title', 'first_name', 'last_name', 'email', 'mobile',
            'date_of_birth', 'drivers_licence_no', 'home_phone', 
            'address_unit', 'address_street_no', 'address_street_name', 
            'address_suburb', 'address_state', 'address_postcode', 'address',
            'occupation', 'employer_name', 'employment_type', 'annual_income',
            'company_name', 'company_abn', 'company_acn',
            'employment_info', 'financial_info', 'assets', 'liabilities'
        ]
        extra_kwargs = {
            # Make most fields optional and allow null/blank values for minimal data creation
            'guarantor_type': {'required': False, 'allow_null': True, 'allow_blank': True},
            'title': {'required': False, 'allow_null': True, 'allow_blank': True},
            'first_name': {'required': False, 'allow_null': True, 'allow_blank': True},
            'last_name': {'required': False, 'allow_null': True, 'allow_blank': True},
            'email': {'required': False, 'allow_null': True, 'allow_blank': True},
            'mobile': {'required': False, 'allow_null': True, 'allow_blank': True},
            'date_of_birth': {'required': False, 'allow_null': True},
            'drivers_licence_no': {'required': False, 'allow_null': True, 'allow_blank': True},
            'home_phone': {'required': False, 'allow_null': True, 'allow_blank': True},
            'address_unit': {'required': False, 'allow_null': True, 'allow_blank': True},
            'address_street_no': {'required': False, 'allow_null': True, 'allow_blank': True},
            'address_street_name': {'required': False, 'allow_null': True, 'allow_blank': True},
            'address_suburb': {'required': False, 'allow_null': True, 'allow_blank': True},
            'address_state': {'required': False, 'allow_null': True, 'allow_blank': True},
            'address_postcode': {'required': False, 'allow_null': True, 'allow_blank': True},
            'address': {'required': False, 'allow_null': True, 'allow_blank': True},
            'occupation': {'required': False, 'allow_null': True, 'allow_blank': True},
            'employer_name': {'required': False, 'allow_null': True, 'allow_blank': True},
            'employment_type': {'required': False, 'allow_null': True, 'allow_blank': True},
            'annual_income': {'required': False, 'allow_null': True},
            'company_name': {'required': False, 'allow_null': True, 'allow_blank': True},
            'company_abn': {'required': False, 'allow_null': True, 'allow_blank': True},
            'company_acn': {'required': False, 'allow_null': True, 'allow_blank': True},
        }
    
    def to_representation(self, instance):
        data = super().to_representation(instance)
        
        # Calculate total asset value and total liability amount with safe type conversion
        total_assets = 0
        for asset in data.get('assets', []):
            value = asset.get('value', 0)
            try:
                # Convert to float first, then to Decimal if needed
                if value is None:
                    value = 0
                elif isinstance(value, str):
                    value = float(value) if value.strip() else 0
                total_assets += value
            except (ValueError, TypeError):
                total_assets += 0
        
        total_liabilities = 0
        for liability in data.get('liabilities', []):
            amount = liability.get('amount', 0)
            try:
                # Convert to float first, then to Decimal if needed
                if amount is None:
                    amount = 0
                elif isinstance(amount, str):
                    amount = float(amount) if amount.strip() else 0
                total_liabilities += amount
            except (ValueError, TypeError):
                total_liabilities += 0
        
        data['total_assets'] = total_assets
        data['total_liabilities'] = total_liabilities
        
        return data
    
    def create(self, validated_data):
        with transaction.atomic():
            # Handle nested assets and liabilities
            assets_data = validated_data.pop('assets', [])
            liabilities_data = validated_data.pop('liabilities', [])
            
            # Get created_by for nested objects
            created_by = validated_data.get('created_by') or (
                self.context['request'].user if hasattr(self, 'context') and 'request' in self.context else None
            )
            
            # Create the guarantor first
            guarantor = Guarantor.objects.create(**validated_data)
            
            # Create assets with enhanced error handling
            assets_created = 0
            for asset_data in assets_data:
                try:
                    asset_data['guarantor'] = guarantor
                    if created_by:
                        asset_data['created_by'] = created_by
                    Asset.objects.create(**asset_data)
                    assets_created += 1
                except Exception as e:
                    print(f"Error creating guarantor asset: {e}")
                    # Continue with other assets even if one fails
                    continue
            
            # Create liabilities with enhanced error handling
            liabilities_created = 0
            for liability_data in liabilities_data:
                try:
                    liability_data['guarantor'] = guarantor
                    if created_by:
                        liability_data['created_by'] = created_by
                    Liability.objects.create(**liability_data)
                    liabilities_created += 1
                except Exception as e:
                    print(f"Error creating guarantor liability: {e}")
                    # Continue with other liabilities even if one fails
                    continue
            
            print(f"Guarantor created with {assets_created} assets and {liabilities_created} liabilities")
        
        return guarantor

    def update(self, instance, validated_data):
        """
        Update guarantor with assets and liabilities
        """
        with transaction.atomic():
            # Handle nested assets and liabilities
            assets_data = validated_data.pop('assets', [])
            liabilities_data = validated_data.pop('liabilities', [])
            
            # Get created_by for nested objects
            created_by = validated_data.get('created_by') or (
                self.context['request'].user if hasattr(self, 'context') and 'request' in self.context else None
            )
            
            # Update guarantor fields
            for attr, value in validated_data.items():
                setattr(instance, attr, value)
            instance.save()
            
            # Handle assets - replace existing ones
            if assets_data is not None:  # Only update if assets data is provided
                # Delete existing assets
                instance.assets.all().delete()
                
                # Create new assets
                assets_created = 0
                for asset_data in assets_data:
                    try:
                        asset_data['guarantor'] = instance
                        if created_by:
                            asset_data['created_by'] = created_by
                        Asset.objects.create(**asset_data)
                        assets_created += 1
                    except Exception as e:
                        print(f"Error updating guarantor asset: {e}")
                        continue
                
                print(f"Updated guarantor assets: {assets_created} created")
            
            # Handle liabilities - replace existing ones
            if liabilities_data is not None:  # Only update if liabilities data is provided
                # Delete existing liabilities
                instance.liabilities.all().delete()
                
                # Create new liabilities
                liabilities_created = 0
                for liability_data in liabilities_data:
                    try:
                        liability_data['guarantor'] = instance
                        if created_by:
                            liability_data['created_by'] = created_by
                        Liability.objects.create(**liability_data)
                        liabilities_created += 1
                    except Exception as e:
                        print(f"Error updating guarantor liability: {e}")
                        continue
                
                print(f"Updated guarantor liabilities: {liabilities_created} created")
        
        return instance


class CompanyBorrowerSerializer(serializers.ModelSerializer):
    """
    Serializer for company borrower with null/blank handling for minimal data creation
    """
    directors = DirectorSerializer(many=True, required=False)
    address = AddressSerializer(required=False)
    assets = AssetSerializer(many=True, required=False)
    liabilities = LiabilitySerializer(many=True, required=False)
    
    class Meta:
        model = Borrower
        fields = [
            'id', 'company_name', 'company_abn', 'company_acn', 'industry_type',
            'annual_company_income', 'is_company',
            'registered_address_unit', 'registered_address_street_no', 'registered_address_street_name',
            'registered_address_suburb', 'registered_address_state', 'registered_address_postcode',
            'directors', 'address', 'assets', 'liabilities'
        ]
        extra_kwargs = {
            # Make most fields optional and allow null/blank values for minimal data creation
            'company_name': {'required': False, 'allow_null': True, 'allow_blank': True},
            'company_abn': {'required': False, 'allow_null': True, 'allow_blank': True},
            'company_acn': {'required': False, 'allow_null': True, 'allow_blank': True},
            'industry_type': {'required': False, 'allow_null': True, 'allow_blank': True},
            'annual_company_income': {'required': False, 'allow_null': True},
            'registered_address_unit': {'required': False, 'allow_null': True, 'allow_blank': True},
            'registered_address_street_no': {'required': False, 'allow_null': True, 'allow_blank': True},
            'registered_address_street_name': {'required': False, 'allow_null': True, 'allow_blank': True},
            'registered_address_suburb': {'required': False, 'allow_null': True, 'allow_blank': True},
            'registered_address_state': {'required': False, 'allow_null': True, 'allow_blank': True},
            'registered_address_postcode': {'required': False, 'allow_null': True, 'allow_blank': True},
        }
    
    def to_internal_value(self, data):
        # Filter out empty nested objects before validation
        if isinstance(data, dict):
            # Make a copy to avoid modifying the original data
            data = data.copy()
            
            # Filter out empty directors
            if 'directors' in data and isinstance(data['directors'], list):
                data['directors'] = [
                    director for director in data['directors'] 
                    if isinstance(director, dict) and director.get('name') and str(director.get('name', '')).strip()
                ]
            
            # Filter out empty/invalid assets
            if 'assets' in data and isinstance(data['assets'], list):
                valid_assets = []
                for asset in data['assets']:
                    if isinstance(asset, dict):
                        asset_type = asset.get('asset_type', '').strip()
                        if asset_type and asset_type in [choice[0] for choice in Asset.ASSET_TYPE_CHOICES]:
                            # Convert to_be_refinanced to proper boolean
                            to_be_refinanced = asset.get('to_be_refinanced', False)
                            if isinstance(to_be_refinanced, str):
                                if to_be_refinanced.lower() in ['true', '1', 'yes']:
                                    asset['to_be_refinanced'] = True
                                else:
                                    asset['to_be_refinanced'] = False
                            valid_assets.append(asset)
                data['assets'] = valid_assets
            
            # Filter out empty/invalid liabilities
            if 'liabilities' in data and isinstance(data['liabilities'], list):
                valid_liabilities = []
                for liability in data['liabilities']:
                    if isinstance(liability, dict):
                        liability_type = liability.get('liability_type', '').strip()
                        if liability_type and liability_type in [choice[0] for choice in Liability.LIABILITY_TYPE_CHOICES]:
                            # Convert to_be_refinanced to proper boolean
                            to_be_refinanced = liability.get('to_be_refinanced', False)
                            if isinstance(to_be_refinanced, str):
                                if to_be_refinanced.lower() in ['true', '1', 'yes']:
                                    liability['to_be_refinanced'] = True
                                else:
                                    liability['to_be_refinanced'] = False
                            valid_liabilities.append(liability)
                data['liabilities'] = valid_liabilities
        
        return super().to_internal_value(data)

    def validate(self, data):
        # Filter out empty nested objects before validation
        # Filter out empty directors
        if 'directors' in data:
            data['directors'] = [
                director for director in data['directors'] 
                if director.get('name') and str(director.get('name', '')).strip()
            ]
        
        # Filter out empty/invalid assets
        if 'assets' in data:
            valid_assets = []
            for asset in data['assets']:
                asset_type = asset.get('asset_type', '').strip()
                if asset_type and asset_type in [choice[0] for choice in Asset.ASSET_TYPE_CHOICES]:
                    # Convert to_be_refinanced to proper boolean
                    to_be_refinanced = asset.get('to_be_refinanced', False)
                    if isinstance(to_be_refinanced, str):
                        if to_be_refinanced.lower() in ['true', '1', 'yes']:
                            asset['to_be_refinanced'] = True
                        else:
                            asset['to_be_refinanced'] = False
                    valid_assets.append(asset)
            data['assets'] = valid_assets
        
        # Filter out empty/invalid liabilities
        if 'liabilities' in data:
            valid_liabilities = []
            for liability in data['liabilities']:
                liability_type = liability.get('liability_type', '').strip()
                if liability_type and liability_type in [choice[0] for choice in Liability.LIABILITY_TYPE_CHOICES]:
                    # Convert to_be_refinanced to proper boolean
                    to_be_refinanced = liability.get('to_be_refinanced', False)
                    if isinstance(to_be_refinanced, str):
                        if to_be_refinanced.lower() in ['true', '1', 'yes']:
                            liability['to_be_refinanced'] = True
                        else:
                            liability['to_be_refinanced'] = False
                    valid_liabilities.append(liability)
            data['liabilities'] = valid_liabilities
        
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
            liabilities_data = validated_data.pop('liabilities', [])
            
            # Set is_company flag to True for company borrowers
            validated_data['is_company'] = True
            
            # Set created_by if not already provided and available from context
            if 'created_by' not in validated_data and hasattr(self, 'context') and 'request' in self.context:
                validated_data['created_by'] = self.context['request'].user
            
            # Create the borrower
            borrower = Borrower.objects.create(**validated_data)
            
            # Get created_by for nested objects
            created_by = validated_data.get('created_by') or (
                self.context['request'].user if hasattr(self, 'context') and 'request' in self.context else None
            )
            
            # Create directors (already filtered in validate method)
            for director_data in directors_data:
                director_data['borrower'] = borrower
                if created_by:
                    director_data['created_by'] = created_by
                Director.objects.create(**director_data)
            
            # Create assets (already filtered in validate method)
            for asset_data in assets_data:
                asset_data['borrower'] = borrower
                if created_by:
                    asset_data['created_by'] = created_by
                Asset.objects.create(**asset_data)
            
            # Create liabilities (already filtered in validate method)
            for liability_data in liabilities_data:
                liability_data['borrower'] = borrower
                if created_by:
                    liability_data['created_by'] = created_by
                Liability.objects.create(**liability_data)
        
        return borrower
    
    def update(self, instance, validated_data):
        """
        Update company borrower instance with nested directors, assets, and liabilities
        """
        with transaction.atomic():
            # Handle nested data
            directors_data = validated_data.pop('directors', None)
            assets_data = validated_data.pop('assets', None)
            liabilities_data = validated_data.pop('liabilities', None)
            
            # Update main borrower fields
            for attr, value in validated_data.items():
                setattr(instance, attr, value)
            instance.save()
            
            # Update directors if provided
            if directors_data is not None:
                # Clear existing directors and create new ones
                instance.directors.all().delete()
                for director_data in directors_data:
                    director_data['borrower'] = instance
                    Director.objects.create(**director_data)
            
            # Update assets if provided
            if assets_data is not None:
                # Clear existing assets and create new ones
                instance.assets.all().delete()
                for asset_data in assets_data:
                    asset_data['borrower'] = instance
                    Asset.objects.create(**asset_data)
            
            # Update liabilities if provided
            if liabilities_data is not None:
                # Clear existing liabilities and create new ones
                instance.liabilities.all().delete()
                for liability_data in liabilities_data:
                    liability_data['borrower'] = instance
                    Liability.objects.create(**liability_data)
        
        return instance 