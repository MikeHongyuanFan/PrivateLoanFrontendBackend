# Application Services Package
# This file aggregates all services for easy importing

# Document and PDF services
from .documents import (
    generate_document,
    process_signature_data,
)

# Financial services
from .financial import (
    generate_repayment_schedule,
    create_standard_fees,
    calculate_funding,
    calculate_funding_manual,
    extend_loan,
)

# Application management services
from .applications import (
    update_application_stage,
    validate_application_schema,
)

# For backward compatibility - keep all the old imports working
__all__ = [
    # Document services
    'generate_document',
    'process_signature_data',
    
    # Financial services
    'generate_repayment_schedule',
    'create_standard_fees', 
    'calculate_funding',
    'calculate_funding_manual',
    'extend_loan',
    
    # Application services
    'update_application_stage',
    'validate_application_schema',
] 