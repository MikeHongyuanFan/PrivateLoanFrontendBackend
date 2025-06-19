"""
Funding and Financial Calculation Serializers

This module contains serializers for funding calculations, financial history,
and calculation results related to loan applications.
"""

from rest_framework import serializers
from ..models import FundingCalculationHistory
from users.serializers import UserSerializer


class FundingCalculationInputSerializer(serializers.Serializer):
    """
    Serializer for funding calculation input fields
    """
    establishment_fee_rate = serializers.DecimalField(max_digits=5, decimal_places=2, required=False)
    capped_interest_months = serializers.IntegerField(min_value=1, default=9, required=False)
    monthly_line_fee_rate = serializers.DecimalField(max_digits=5, decimal_places=2, required=False)
    brokerage_fee_rate = serializers.DecimalField(max_digits=5, decimal_places=2, required=False)
    application_fee = serializers.DecimalField(max_digits=10, decimal_places=2, required=False)
    due_diligence_fee = serializers.DecimalField(max_digits=10, decimal_places=2, required=False)
    legal_fee_before_gst = serializers.DecimalField(max_digits=10, decimal_places=2, required=False)
    valuation_fee = serializers.DecimalField(max_digits=10, decimal_places=2, required=False)
    monthly_account_fee = serializers.DecimalField(max_digits=10, decimal_places=2, required=False)
    working_fee = serializers.DecimalField(max_digits=10, decimal_places=2, required=False, default=0)


class ManualFundingCalculationSerializer(serializers.Serializer):
    """
    Serializer for manual funding calculation with application parameters
    """
    loan_amount = serializers.DecimalField(max_digits=12, decimal_places=2, required=True)
    interest_rate = serializers.DecimalField(max_digits=5, decimal_places=2, required=True)
    security_value = serializers.DecimalField(max_digits=12, decimal_places=2, required=True)
    
    # Include all funding calculation input fields
    establishment_fee_rate = serializers.DecimalField(max_digits=5, decimal_places=2, required=True)
    capped_interest_months = serializers.IntegerField(min_value=1, default=9)
    monthly_line_fee_rate = serializers.DecimalField(max_digits=5, decimal_places=2, required=True)
    brokerage_fee_rate = serializers.DecimalField(max_digits=5, decimal_places=2, required=True)
    application_fee = serializers.DecimalField(max_digits=10, decimal_places=2, required=True)
    due_diligence_fee = serializers.DecimalField(max_digits=10, decimal_places=2, required=True)
    legal_fee_before_gst = serializers.DecimalField(max_digits=10, decimal_places=2, required=True)
    valuation_fee = serializers.DecimalField(max_digits=10, decimal_places=2, required=True)
    monthly_account_fee = serializers.DecimalField(max_digits=10, decimal_places=2, required=True)
    working_fee = serializers.DecimalField(max_digits=10, decimal_places=2, required=False, default=0)


class FundingCalculationHistorySerializer(serializers.ModelSerializer):
    """
    Serializer for funding calculation history
    """
    created_by_details = UserSerializer(source='created_by', read_only=True)
    
    class Meta:
        model = FundingCalculationHistory
        fields = [
            'id', 'application', 'calculation_input', 'calculation_result', 
            'created_by', 'created_by_details', 'created_at'
        ]
        read_only_fields = ['created_by', 'created_at']


class FundingCalculationResultSerializer(serializers.Serializer):
    """
    Serializer for funding calculation result
    """
    establishment_fee = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    capped_interest = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    line_fee = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    brokerage_fee = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    legal_fee = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    application_fee = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    due_diligence_fee = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    valuation_fee = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    monthly_account_fee = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    working_fee = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    total_fees = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    funds_available = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True) 