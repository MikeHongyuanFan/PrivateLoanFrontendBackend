from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views.application_views import ApplicationViewSet
from .views.valuer_qs_views import ValuerViewSet, QuantitySurveyorViewSet
from .views.pdf_generation import GenerateFilledFormView
from .views.funding_calculator_views import ManualFundingCalculationView
from .views.active_loan_views import ActiveLoanViewSet, ActiveLoanRepaymentViewSet, get_active_loan_by_application

# Create a router for ViewSets
router = DefaultRouter()
router.register(r'applications', ApplicationViewSet, basename='application')
router.register(r'valuers', ValuerViewSet, basename='valuer')
router.register(r'quantity-surveyors', QuantitySurveyorViewSet, basename='quantity-surveyor')
router.register(r'active-loans', ActiveLoanViewSet, basename='active-loan')
router.register(r'active-loan-repayments', ActiveLoanRepaymentViewSet, basename='active-loan-repayment')

urlpatterns = [
    # Include router URLs
    path('', include(router.urls)),
    
    # Enhanced application list endpoint
    path('enhanced-applications/', ApplicationViewSet.as_view({'get': 'enhanced_list'}), name='enhanced-application-list'),
    
    # Enhanced applications endpoint (alternative list view)
    path('enhanced-applications-alt/', ApplicationViewSet.as_view({'get': 'enhanced_applications'}), name='enhanced-applications-alt'),
    
    # Application creation with cascade
    path('create-with-cascade/', ApplicationViewSet.as_view({'post': 'create'}), name='application-list-create'),
    
    # Application validation
    path('validate-schema/', ApplicationViewSet.as_view({'post': 'validate_schema'}), name='validate-application-schema'),
    
    # Application signature
    path('<int:pk>/signature/', ApplicationViewSet.as_view({'post': 'signature'}), name='application-signature'),
    
    # Application stage update
    path('<int:pk>/stage/', ApplicationViewSet.as_view({'put': 'update_stage'}), name='application-stage-update'),
    
    # Application borrowers update
    path('<int:pk>/borrowers/', ApplicationViewSet.as_view({'put': 'borrowers'}), name='application-borrowers-update'),
    
    # Application sign
    path('<int:pk>/sign/', ApplicationViewSet.as_view({'post': 'sign'}), name='application-sign'),
    
    # Application loan extension
    path('<int:pk>/extend-loan/', ApplicationViewSet.as_view({'post': 'extend_loan'}), name='application-extend-loan'),
    
    # BD assignment management
    path('<int:pk>/assign-bd/', ApplicationViewSet.as_view({'post': 'assign_bd', 'put': 'assign_bd', 'delete': 'assign_bd'}), name='application-assign-bd'),
    
    # Funding calculation
    path('<int:pk>/funding-calculation/', ApplicationViewSet.as_view({'post': 'funding_calculation'}), name='application-funding-calculation'),
    
    # Funding calculation history
    path('<int:pk>/funding-calculation-history/', ApplicationViewSet.as_view({'get': 'funding_calculation_history'}), name='application-funding-calculation-history'),
    
    # Generate filled PDF form
    path('<int:application_id>/generate-pdf/', GenerateFilledFormView.as_view(), name='application-generate-pdf'),
    
    # Manual funding calculator
    path('manual-funding-calculator/', ManualFundingCalculationView.as_view(), name='manual-funding-calculator'),
    
    # Application partial update with cascade
    path('<int:pk>/partial-update-cascade/', ApplicationViewSet.as_view({'patch': 'partial_update_with_cascade'}), name='application-partial-update-cascade'),
    
    # Application retrieve with cascade
    path('<int:pk>/retrieve-cascade/', ApplicationViewSet.as_view({'get': 'retrieve_with_cascade'}), name='application-retrieve-cascade'),
    
    # Active loan endpoints - using ViewSet action instead of function-based view
    # The URL will be: /api/applications/active-loans/application/{application_id}/
]
