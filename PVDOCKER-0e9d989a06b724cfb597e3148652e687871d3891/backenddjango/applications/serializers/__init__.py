# Application Serializers Package
# This file aggregates all serializers for easy importing

# Application serializers
from .application import (
    ApplicationCreateSerializer,
    ApplicationDetailSerializer,
    ApplicationListSerializer,
    ApplicationPartialUpdateSerializer,
    ApplicationStageUpdateSerializer,
    ApplicationBorrowerSerializer,
    ApplicationSignatureSerializer,
    LoanExtensionSerializer,
    GeneratePDFSerializer,
    AssignBDSerializer
)

# Borrower and Guarantor serializers
from .borrowers import (
    BorrowerSerializer,
    GuarantorSerializer,
    CompanyBorrowerSerializer,
    DirectorSerializer,
    AssetSerializer,
    LiabilitySerializer,
    ApplicationLiabilitySerializer,
    AddressSerializer,
    EmploymentInfoSerializer,
    FinancialInfoSerializer,
    GuarantorAssetSerializer,
    CompanyAssetSerializer
)

# Professional services serializers
from .professionals import (
    ValuerSerializer,
    ValuerListSerializer,
    QuantitySurveyorSerializer,
    QuantitySurveyorListSerializer,
    QSInfoSerializer
)

# Property and loan related serializers
from .property import (
    SecurityPropertySerializer,
    LoanRequirementSerializer
)

# Financial and calculation serializers
from .funding import (
    FundingCalculationInputSerializer,
    ManualFundingCalculationSerializer,
    FundingCalculationHistorySerializer,
    FundingCalculationResultSerializer
)

# Utility serializers
from .utils import (
    SolvencyEnquiriesSerializer
)

# For backward compatibility - keep all the old imports working
__all__ = [
    # Application
    'ApplicationCreateSerializer',
    'ApplicationDetailSerializer', 
    'ApplicationListSerializer',
    'ApplicationPartialUpdateSerializer',
    'ApplicationStageUpdateSerializer',
    'ApplicationBorrowerSerializer',
    'ApplicationSignatureSerializer',
    'LoanExtensionSerializer',
    'GeneratePDFSerializer',
    'AssignBDSerializer',
    
    # Borrowers
    'BorrowerSerializer',
    'GuarantorSerializer', 
    'CompanyBorrowerSerializer',
    'DirectorSerializer',
    'AssetSerializer',
    'LiabilitySerializer',
    'ApplicationLiabilitySerializer',
    'AddressSerializer',
    'EmploymentInfoSerializer',
    'FinancialInfoSerializer',
    'GuarantorAssetSerializer',
    'CompanyAssetSerializer',
    
    # Professionals
    'ValuerSerializer',
    'ValuerListSerializer',
    'QuantitySurveyorSerializer',
    'QuantitySurveyorListSerializer',
    'QSInfoSerializer',
    
    # Property
    'SecurityPropertySerializer',
    'LoanRequirementSerializer',
    
    # Funding
    'FundingCalculationInputSerializer',
    'ManualFundingCalculationSerializer', 
    'FundingCalculationHistorySerializer',
    'FundingCalculationResultSerializer',
    
    # Utils
    'SolvencyEnquiriesSerializer',
] 