"""
Django models for loan applications.

REFACTORED STRUCTURE - Backward Compatibility Layer
===================================================

This module has been refactored into logical sub-modules for better maintainability:

- models/base.py - Abstract base models for shared functionality
- models/core.py - Main Application model  
- models/contacts.py - Valuer and QuantitySurveyor models
- models/properties.py - SecurityProperty model
- models/requirements.py - LoanRequirement model
- models/documents.py - Document model
- models/financial.py - Fee, Repayment, FundingCalculationHistory models

All existing functionality is preserved. Imports and references from serializers,
views, and other modules will continue to work exactly as before.

For new development, you can import directly from sub-modules:
    from applications.models.core import Application
    from applications.models.contacts import Valuer, QuantitySurveyor
    
Or continue using the traditional approach:
    from applications.models import Application, Valuer, QuantitySurveyor
"""

# Import all models from the new modular structure
# This ensures 100% backward compatibility
from .models.base import (
    TimestampedModel,
    UserTrackingModel, 
    BaseApplicationModel
)

from .models.core import (
    Application,
    generate_reference_number
)

from .models.contacts import (
    Valuer,
    QuantitySurveyor
)

from .models.properties import (
    SecurityProperty
)

from .models.requirements import (
    LoanRequirement
)

from .models.documents import (
    Document
)

from .models.financial import (
    Fee,
    Repayment,
    FundingCalculationHistory
)

# Maintain the original __all__ list for explicit exports
__all__ = [
    # Core models
    'Application',
    'generate_reference_number',
    
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
    
    # Base models (available but typically not imported directly)
    'TimestampedModel',
    'UserTrackingModel',
    'BaseApplicationModel',
]

# Optional: Provide migration guidance
"""
MIGRATION NOTES:
===============

Schema Changes: None - all field definitions remain identical
Foreign Keys: All relationships preserved with same related_names
Choices: All choice fields maintain same values and labels
Validation: All validators and constraints preserved

This refactoring is purely organizational - no database migrations needed.
"""