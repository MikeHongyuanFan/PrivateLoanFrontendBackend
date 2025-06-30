"""
Professional Services Serializers

This module contains serializers for professional service providers 
in the loan application process, including valuers and quantity surveyors.
"""

from rest_framework import serializers
from ..models import Valuer, QuantitySurveyor
from users.serializers import UserSerializer


class ValuerSerializer(serializers.ModelSerializer):
    """
    Serializer for Valuer model with null/blank handling for minimal data creation
    """
    created_by_details = UserSerializer(source='created_by', read_only=True)
    application_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Valuer
        fields = [
            'id', 'company_name', 'contact_name', 'phone', 'email', 'address', 'notes', 
            'is_active', 'created_by', 'created_by_details', 'created_at', 'updated_at',
            'application_count'
        ]
        read_only_fields = ['created_by', 'created_at', 'updated_at']
        extra_kwargs = {
            # Make most fields optional and allow null/blank values for minimal data creation
            'company_name': {'required': False, 'allow_null': True, 'allow_blank': True},
            'contact_name': {'required': False, 'allow_null': True, 'allow_blank': True},
            'phone': {'required': False, 'allow_null': True, 'allow_blank': True},
            'email': {'required': False, 'allow_null': True, 'allow_blank': True},
            'address': {'required': False, 'allow_null': True, 'allow_blank': True},
            'notes': {'required': False, 'allow_null': True, 'allow_blank': True},
            'is_active': {'required': False, 'allow_null': True},
        }
    
    def get_application_count(self, obj):
        """Get the number of applications using this valuer"""
        if hasattr(obj, 'applications'):
            return obj.applications.count()
        return 0
    
    def create(self, validated_data):
        # Set the created_by field to the current user
        # Handle cases where request context might not be available
        if 'request' in self.context and self.context['request'].user:
            validated_data['created_by'] = self.context['request'].user
        elif 'created_by' in validated_data:
            # If created_by is already provided in the data, use it
            pass
        else:
            # Fallback: try to get user from context or use None
            validated_data['created_by'] = self.context.get('user', None)
        return super().create(validated_data)


class QuantitySurveyorSerializer(serializers.ModelSerializer):
    """
    Serializer for QuantitySurveyor model with null/blank handling for minimal data creation
    """
    created_by_details = UserSerializer(source='created_by', read_only=True)
    application_count = serializers.SerializerMethodField()
    
    class Meta:
        model = QuantitySurveyor
        fields = [
            'id', 'company_name', 'contact_name', 'phone', 'email', 'address', 'notes', 
            'is_active', 'created_by', 'created_by_details', 'created_at', 'updated_at',
            'application_count'
        ]
        read_only_fields = ['created_by', 'created_at', 'updated_at']
        extra_kwargs = {
            # Make most fields optional and allow null/blank values for minimal data creation
            'company_name': {'required': False, 'allow_null': True, 'allow_blank': True},
            'contact_name': {'required': False, 'allow_null': True, 'allow_blank': True},
            'phone': {'required': False, 'allow_null': True, 'allow_blank': True},
            'email': {'required': False, 'allow_null': True, 'allow_blank': True},
            'address': {'required': False, 'allow_null': True, 'allow_blank': True},
            'notes': {'required': False, 'allow_null': True, 'allow_blank': True},
            'is_active': {'required': False, 'allow_null': True},
        }
    
    def get_application_count(self, obj):
        """Get the number of applications using this quantity surveyor"""
        if hasattr(obj, 'applications'):
            return obj.applications.count()
        return 0
    
    def create(self, validated_data):
        # Set the created_by field to the current user
        # Handle cases where request context might not be available
        if 'request' in self.context and self.context['request'].user:
            validated_data['created_by'] = self.context['request'].user
        elif 'created_by' in validated_data:
            # If created_by is already provided in the data, use it
            pass
        else:
            # Fallback: try to get user from context or use None
            validated_data['created_by'] = self.context.get('user', None)
        return super().create(validated_data)


class ValuerListSerializer(serializers.ModelSerializer):
    """
    Simplified serializer for Valuer listing (dropdown options)
    """
    display_name = serializers.SerializerMethodField()
    
    class Meta:
        model = Valuer
        fields = ['id', 'company_name', 'contact_name', 'phone', 'email', 'display_name', 'is_active']
    
    def get_display_name(self, obj):
        return f"{obj.company_name} - {obj.contact_name}"


class QuantitySurveyorListSerializer(serializers.ModelSerializer):
    """
    Simplified serializer for QuantitySurveyor listing (dropdown options)
    """
    display_name = serializers.SerializerMethodField()
    
    class Meta:
        model = QuantitySurveyor
        fields = ['id', 'company_name', 'contact_name', 'phone', 'email', 'display_name', 'is_active']
    
    def get_display_name(self, obj):
        return f"{obj.company_name} - {obj.contact_name}"


class QSInfoSerializer(serializers.Serializer):
    """
    Serializer for quantity surveyor information with null/blank handling for minimal data creation
    """
    company_name = serializers.CharField(max_length=255, required=False, allow_blank=True, allow_null=True)
    contact_name = serializers.CharField(max_length=100, required=False, allow_blank=True, allow_null=True)
    phone = serializers.CharField(max_length=20, required=False, allow_blank=True, allow_null=True)
    email = serializers.EmailField(required=False, allow_blank=True, allow_null=True)
    notes = serializers.CharField(allow_blank=True, required=False, allow_null=True) 