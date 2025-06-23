from rest_framework import serializers
from .models import Broker, Branch, BDM
from users.serializers import UserSerializer


class BranchSerializer(serializers.ModelSerializer):
    """Serializer for branch information with null/blank handling for minimal data creation"""
    class Meta:
        model = Branch
        fields = ['id', 'name']  # Removed address, phone, email fields
        extra_kwargs = {
            # Make name field optional and allow null/blank values for minimal data creation
            'name': {'required': False, 'allow_null': True, 'allow_blank': True},
        }


class BDMSerializer(serializers.ModelSerializer):
    """Serializer for BDM information with null/blank handling for minimal data creation"""
    branch = BranchSerializer(read_only=True)
    branch_id = serializers.IntegerField(write_only=True, required=False, allow_null=True)
    
    class Meta:
        model = BDM
        fields = ['id', 'name', 'email', 'phone', 'branch', 'branch_id']
        extra_kwargs = {
            # Make most fields optional and allow null/blank values for minimal data creation
            'name': {'required': False, 'allow_null': True, 'allow_blank': True},
            'email': {'required': False, 'allow_null': True, 'allow_blank': True},
            'phone': {'required': False, 'allow_null': True, 'allow_blank': True},
        }
    
    def create(self, validated_data):
        branch_id = validated_data.pop('branch_id', None)
        
        # Handle branch association
        branch = None
        if branch_id:
            # Use existing branch if branch_id is provided
            try:
                branch = Branch.objects.get(id=branch_id)
            except Branch.DoesNotExist:
                raise serializers.ValidationError({"branch_id": "Branch with this ID does not exist"})
        
        # Create BDM instance
        bdm = BDM.objects.create(branch=branch, **validated_data)
        return bdm
        
    def update(self, instance, validated_data):
        branch_id = validated_data.pop('branch_id', None)
        
        # Handle branch association
        if branch_id:
            # Use existing branch if branch_id is provided
            try:
                branch = Branch.objects.get(id=branch_id)
                instance.branch = branch
            except Branch.DoesNotExist:
                raise serializers.ValidationError({"branch_id": "Branch with this ID does not exist"})
        
        # Update BDM fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance


class BrokerListSerializer(serializers.ModelSerializer):
    """Serializer for listing brokers with minimal information and null/blank handling"""
    class Meta:
        model = Broker
        fields = ['id', 'name', 'company', 'email', 'phone']
        extra_kwargs = {
            # Make most fields optional and allow null/blank values for minimal data creation
            'name': {'required': False, 'allow_null': True, 'allow_blank': True},
            'company': {'required': False, 'allow_null': True, 'allow_blank': True},
            'email': {'required': False, 'allow_null': True, 'allow_blank': True},
            'phone': {'required': False, 'allow_null': True, 'allow_blank': True},
        }


class BrokerDetailSerializer(serializers.ModelSerializer):
    """Serializer for detailed broker information with null/blank handling for minimal data creation"""
    branch = BranchSerializer(read_only=True)
    branch_id = serializers.IntegerField(write_only=True, required=False, allow_null=True)
    bdms = BDMSerializer(many=True, read_only=True)
    bdm_ids = serializers.ListField(
        child=serializers.IntegerField(),
        write_only=True,
        required=False,
        allow_empty=True
    )
    created_by = UserSerializer(read_only=True)
    commission_account_locked_by = UserSerializer(read_only=True)
    
    class Meta:
        model = Broker
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at', 'created_by', 'commission_account_locked_by', 'commission_account_locked_at']
        extra_kwargs = {
            # Make most fields optional and allow null/blank values for minimal data creation
            'name': {'required': False, 'allow_null': True, 'allow_blank': True},
            'company': {'required': False, 'allow_null': True, 'allow_blank': True},
            'email': {'required': False, 'allow_null': True, 'allow_blank': True},
            'phone': {'required': False, 'allow_null': True, 'allow_blank': True},
            'address': {'required': False, 'allow_null': True, 'allow_blank': True},
            'abn': {'required': False, 'allow_null': True, 'allow_blank': True},
            'acn': {'required': False, 'allow_null': True, 'allow_blank': True},
            'aggregator': {'required': False, 'allow_null': True, 'allow_blank': True},
            'credit_rep_number': {'required': False, 'allow_null': True, 'allow_blank': True},
            'commission_structure': {'required': False, 'allow_null': True, 'allow_blank': True},
            'notes': {'required': False, 'allow_null': True, 'allow_blank': True},
            'is_active': {'required': False, 'allow_null': True},
            'user': {'required': False, 'allow_null': True},
            'branch_id': {'required': False, 'allow_null': True},
        }
    
    def validate(self, data):
        """
        Validate commission account modifications based on user permissions
        """
        request = self.context.get('request')
        if not request or not request.user:
            return data
        
        # Check if this is an update operation
        if self.instance:
            # If commission account is locked, only super user/accounts can modify
            if self.instance.commission_account_locked and not request.user.can_modify_commission_account():
                commission_fields = ['commission_bank_name', 'commission_account_name', 'commission_account_number', 'commission_bsb']
                for field in commission_fields:
                    if field in data:
                        raise serializers.ValidationError({
                            field: f"Commission account is locked. Only super user and accounts can modify this field."
                        })
            
            # If commission account has data and is not locked, only super user/accounts can modify
            elif self.instance.has_commission_account_data() and not request.user.can_modify_commission_account():
                commission_fields = ['commission_bank_name', 'commission_account_name', 'commission_account_number', 'commission_bsb']
                for field in commission_fields:
                    if field in data:
                        raise serializers.ValidationError({
                            field: f"Commission account has been entered. Only super user and accounts can modify this field."
                        })
        
        return data
    
    def create(self, validated_data):
        branch_id = validated_data.pop('branch_id', None)
        bdm_ids = validated_data.pop('bdm_ids', [])
        
        # Handle branch association
        branch = None
        if branch_id:
            try:
                branch = Branch.objects.get(id=branch_id)
            except Branch.DoesNotExist:
                raise serializers.ValidationError({"branch_id": "Branch with this ID does not exist"})
        
        # Create broker instance
        broker = Broker.objects.create(branch=branch, **validated_data)
        
        # Handle BDM assignments
        if bdm_ids:
            try:
                bdms = BDM.objects.filter(id__in=bdm_ids)
                broker.bdms.set(bdms)
            except Exception as e:
                # If BDM assignment fails, still create the broker but log the error
                print(f"Warning: Failed to assign BDMs to broker {broker.id}: {e}")
        
        # Auto-lock commission account if data is entered and user is not super user/accounts
        request = self.context.get('request')
        if request and request.user and not request.user.can_modify_commission_account():
            if broker.has_commission_account_data():
                broker.lock_commission_account(request.user)
        
        return broker
    
    def update(self, instance, validated_data):
        branch_id = validated_data.pop('branch_id', None)
        bdm_ids = validated_data.pop('bdm_ids', None)
        
        # Handle branch association
        if branch_id is not None:  # Allow setting to None to remove branch
            if branch_id:
                try:
                    branch = Branch.objects.get(id=branch_id)
                    instance.branch = branch
                except Branch.DoesNotExist:
                    raise serializers.ValidationError({"branch_id": "Branch with this ID does not exist"})
            else:
                instance.branch = None
        
        # Handle BDM assignments
        if bdm_ids is not None:  # Allow clearing BDMs by passing empty list
            try:
                if bdm_ids:
                    bdms = BDM.objects.filter(id__in=bdm_ids)
                    instance.bdms.set(bdms)
                else:
                    instance.bdms.clear()
            except Exception as e:
                # If BDM assignment fails, still update the broker but log the error
                print(f"Warning: Failed to update BDM assignments for broker {instance.id}: {e}")
        
        # Update broker fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        
        # Auto-lock commission account if data is entered and user is not super user/accounts
        request = self.context.get('request')
        if request and request.user and not request.user.can_modify_commission_account():
            if instance.has_commission_account_data() and not instance.commission_account_locked:
                instance.lock_commission_account(request.user)
        
        return instance


# Lightweight serializers for dropdown usage
class BrokerDropdownSerializer(serializers.ModelSerializer):
    """Lightweight serializer for broker dropdown selection"""
    display_name = serializers.SerializerMethodField()
    
    class Meta:
        model = Broker
        fields = ['id', 'name', 'company', 'display_name']
    
    def get_display_name(self, obj):
        """Create a display name combining name and company"""
        if obj.name and obj.company:
            return f"{obj.name} - {obj.company}"
        return obj.name or obj.company or f"Broker #{obj.id}"


class BDMDropdownSerializer(serializers.ModelSerializer):
    """Lightweight serializer for BDM dropdown selection"""
    display_name = serializers.SerializerMethodField()
    branch_name = serializers.CharField(source='branch.name', read_only=True)
    
    class Meta:
        model = BDM
        fields = ['id', 'name', 'email', 'display_name', 'branch_name']
    
    def get_display_name(self, obj):
        """Create a display name with branch info"""
        if obj.branch:
            return f"{obj.name} - {obj.branch.name}"
        return obj.name or f"BDM #{obj.id}"


class BranchDropdownSerializer(serializers.ModelSerializer):
    """Lightweight serializer for branch dropdown selection"""
    display_name = serializers.SerializerMethodField()
    
    class Meta:
        model = Branch
        fields = ['id', 'name', 'display_name']
    
    def get_display_name(self, obj):
        """Create a display name - just the branch name"""
        return obj.name or f"Branch #{obj.id}"
