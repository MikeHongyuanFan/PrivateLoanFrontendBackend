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
    Serializer for Valuer model
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
    
    def get_application_count(self, obj):
        """Get the number of applications using this valuer"""
        return obj.applications.count()
    
    def create(self, validated_data):
        # Set the created_by field to the current user
        validated_data['created_by'] = self.context['request'].user
        return super().create(validated_data)


class QuantitySurveyorSerializer(serializers.ModelSerializer):
    """
    Serializer for QuantitySurveyor model
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
    
    def get_application_count(self, obj):
        """Get the number of applications using this quantity surveyor"""
        return obj.applications.count()
    
    def create(self, validated_data):
        # Set the created_by field to the current user
        validated_data['created_by'] = self.context['request'].user
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
    Serializer for quantity surveyor information
    """
    company_name = serializers.CharField(max_length=255, required=False, allow_blank=True)
    contact_name = serializers.CharField(max_length=100, required=False, allow_blank=True)
    phone = serializers.CharField(max_length=20, required=False, allow_blank=True)
    email = serializers.EmailField(required=False, allow_blank=True)
    notes = serializers.CharField(allow_blank=True, required=False) 