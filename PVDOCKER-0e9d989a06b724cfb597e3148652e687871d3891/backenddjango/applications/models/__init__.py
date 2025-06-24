# Application Models Package
"""
Loan application models organized into logical modules for better maintainability.

This package provides:
- Abstract base models for shared functionality
- Core application models
- Property and security models  
- Contact and professional service models
- Document and financial tracking models

All models maintain backward compatibility with existing schema and APIs.
"""

from .base import TimestampedModel, UserTrackingModel, BaseApplicationModel
from .core import Application
from .contacts import Valuer, QuantitySurveyor  
from .properties import SecurityProperty
from .requirements import LoanRequirement
from .documents import Document
from .financial import Fee, Repayment, FundingCalculationHistory, ActiveLoan, ActiveLoanRepayment

# Maintain backward compatibility - export all models at package level
__all__ = [
    # Base models
    'TimestampedModel',
    'UserTrackingModel', 
    'BaseApplicationModel',
    
    # Core models
    'Application',
    
    # Contact models
    'Valuer',
    'QuantitySurveyor',
    
    # Property models
    'SecurityProperty',
    
    # Requirement models
    'LoanRequirement',
    
    # Document models
    'Document',
    
    # Financial models
    'Fee',
    'Repayment',
    'FundingCalculationHistory',
    'ActiveLoan',
    'ActiveLoanRepayment',
] 