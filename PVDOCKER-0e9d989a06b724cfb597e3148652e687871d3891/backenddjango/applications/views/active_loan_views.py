"""
Views for Active Loan management.

This module contains views for managing active loans, including
loan creation, updates, repayment tracking, and alert management.
"""

from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.db.models import Q, Count, Sum
from rest_framework import viewsets, status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from applications.models import ActiveLoan, ActiveLoanRepayment, Application
from applications.serializers import (
    ActiveLoanSerializer,
    ActiveLoanCreateSerializer,
    ActiveLoanSummarySerializer,
    ActiveLoanRepaymentSerializer
)


class ActiveLoanViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing active loans.
    
    Provides CRUD operations for active loans with specialized
    endpoints for alerts, repayments, and status updates.
    """
    
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """Get queryset with proper filtering and ordering."""
        queryset = ActiveLoan.objects.select_related('application').prefetch_related('repayments')
        
        # Filter by active status
        if self.action == 'list':
            is_active = self.request.query_params.get('is_active', 'true')
            if is_active.lower() == 'true':
                queryset = queryset.filter(is_active=True)
            elif is_active.lower() == 'false':
                queryset = queryset.filter(is_active=False)
        
        # Filter by alert status
        alert_status = self.request.query_params.get('alert_status')
        if alert_status:
            today = timezone.now().date()
            if alert_status == 'expiry_critical':
                # Loans expiring within 7 days
                expiry_threshold = today + timezone.timedelta(days=7)
                queryset = queryset.filter(loan_expiry_date__lte=expiry_threshold, loan_expiry_date__gte=today)
            elif alert_status == 'expiry_warning':
                # Loans expiring within 30 days
                expiry_threshold = today + timezone.timedelta(days=30)
                queryset = queryset.filter(loan_expiry_date__lte=expiry_threshold, loan_expiry_date__gte=today)
            elif alert_status == 'payment_due':
                # Loans with payments due within 14 days
                queryset = queryset.filter(interest_payments_required=True)
        
        return queryset.order_by('-created_at')
    
    def get_serializer_class(self):
        """Return appropriate serializer based on action."""
        if self.action == 'create':
            return ActiveLoanCreateSerializer
        elif self.action == 'list':
            return ActiveLoanSummarySerializer
        return ActiveLoanSerializer
    
    def create(self, request, *args, **kwargs):
        """Create a new active loan from a settled application."""
        print("=== CREATE ACTIVE LOAN DEBUG ===")
        print("Request data:", request.data)
        
        serializer = self.get_serializer(data=request.data)
        
        if not serializer.is_valid():
            print("Validation errors:", serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        # Check if application is already an active loan
        application_id = serializer.validated_data['application'].id
        if ActiveLoan.objects.filter(application_id=application_id).exists():
            return Response(
                {'error': 'This application already has an active loan.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        active_loan = serializer.save()
        
        # Return full serialized data
        response_serializer = ActiveLoanSerializer(active_loan)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)
    
    @action(detail=False, methods=['get'])
    def alerts(self, request):
        """Get loans requiring alerts (expiry and payment reminders)."""
        today = timezone.now().date()
        
        # Loans expiring within 30 days
        expiry_alerts = ActiveLoan.objects.filter(
            is_active=True,
            loan_expiry_date__lte=today + timezone.timedelta(days=30),
            loan_expiry_date__gte=today
        ).select_related('application')
        
        # Loans with interest payments due within 14 days
        payment_alerts = []
        for loan in ActiveLoan.objects.filter(is_active=True, interest_payments_required=True):
            next_payment = loan.next_interest_payment_date
            if next_payment and (next_payment - today).days <= 14:
                payment_alerts.append(loan)
        
        return Response({
            'expiry_alerts': ActiveLoanSummarySerializer(expiry_alerts, many=True).data,
            'payment_alerts': ActiveLoanSummarySerializer(payment_alerts, many=True).data,
            'total_alerts': len(expiry_alerts) + len(payment_alerts)
        })
    
    @action(detail=False, methods=['get'])
    def dashboard(self, request):
        """Get dashboard statistics for active loans."""
        today = timezone.now().date()
        
        # Basic counts
        total_active = ActiveLoan.objects.filter(is_active=True).count()
        total_inactive = ActiveLoan.objects.filter(is_active=False).count()
        
        # Alert counts
        expiry_critical = ActiveLoan.objects.filter(
            is_active=True,
            loan_expiry_date__lte=today + timezone.timedelta(days=7),
            loan_expiry_date__gte=today
        ).count()
        
        expiry_warning = ActiveLoan.objects.filter(
            is_active=True,
            loan_expiry_date__lte=today + timezone.timedelta(days=30),
            loan_expiry_date__gt=today + timezone.timedelta(days=7)
        ).count()
        
        # Payment alerts
        payment_due_count = 0
        for loan in ActiveLoan.objects.filter(is_active=True, interest_payments_required=True):
            next_payment = loan.next_interest_payment_date
            if next_payment and (next_payment - today).days <= 14:
                payment_due_count += 1
        
        # Total loan value
        total_loan_value = ActiveLoan.objects.filter(
            is_active=True
        ).aggregate(
            total=Sum('application__loan_amount')
        )['total'] or 0
        
        return Response({
            'total_active_loans': total_active,
            'total_inactive_loans': total_inactive,
            'total_loan_value': total_loan_value,
            'alerts': {
                'expiry_critical': expiry_critical,
                'expiry_warning': expiry_warning,
                'payment_due': payment_due_count,
                'total_alerts': expiry_critical + expiry_warning + payment_due_count
            }
        })
    
    @action(detail=True, methods=['post'])
    def deactivate(self, request, pk=None):
        """Deactivate an active loan."""
        active_loan = self.get_object()
        active_loan.is_active = False
        active_loan.save()
        
        serializer = self.get_serializer(active_loan)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def reactivate(self, request, pk=None):
        """Reactivate an inactive loan."""
        active_loan = self.get_object()
        active_loan.is_active = True
        active_loan.save()
        
        serializer = self.get_serializer(active_loan)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get', 'post'])
    def repayments(self, request, pk=None):
        """Manage repayments for an active loan."""
        active_loan = self.get_object()
        
        if request.method == 'GET':
            repayments = active_loan.repayments.all().order_by('-payment_date')
            serializer = ActiveLoanRepaymentSerializer(repayments, many=True)
            return Response(serializer.data)
        
        elif request.method == 'POST':
            data = request.data.copy()
            data['active_loan'] = active_loan.id
            
            serializer = ActiveLoanRepaymentSerializer(data=data)
            serializer.is_valid(raise_exception=True)
            repayment = serializer.save()
            
            return Response(
                ActiveLoanRepaymentSerializer(repayment).data,
                status=status.HTTP_201_CREATED
            )
    
    @action(detail=True, methods=['post'])
    def send_alert(self, request, pk=None):
        """
        Send an immediate alert for this active loan.
        
        Expected payload:
        {
            "alert_type": "payment|expiry|manual",
            "message": "Custom message (optional)",
            "user_id": "Specific user ID (optional)"
        }
        """
        try:
            active_loan = self.get_object()
            
            alert_type = request.data.get('alert_type', 'manual')
            message = request.data.get('message')
            user_id = request.data.get('user_id')
            
            # Validate alert type
            valid_types = ['payment', 'expiry', 'manual']
            if alert_type not in valid_types:
                return Response(
                    {'error': f'Invalid alert_type. Must be one of: {valid_types}'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Send the alert using Celery task
            from applications.tasks import send_immediate_active_loan_alert
            task_result = send_immediate_active_loan_alert.delay(
                active_loan.id, 
                alert_type, 
                message, 
                user_id
            )
            
            return Response({
                'message': 'Alert sent successfully',
                'task_id': task_result.id,
                'alert_type': alert_type,
                'loan_reference': active_loan.application.reference_number
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response(
                {'error': f'Failed to send alert: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @action(detail=False, methods=['get'], url_path='application/(?P<application_id>[^/.]+)')
    def by_application(self, request, application_id=None):
        """Get active loan data for a specific application."""
        try:
            application = get_object_or_404(Application, id=application_id)
            
            # Check if application has an active loan
            try:
                active_loan = ActiveLoan.objects.get(application=application)
                serializer = ActiveLoanSerializer(active_loan)
                return Response(serializer.data)
            except ActiveLoan.DoesNotExist:
                return Response(
                    {'message': 'No active loan found for this application'},
                    status=status.HTTP_404_NOT_FOUND
                )
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class ActiveLoanRepaymentViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing active loan repayments.
    
    Provides CRUD operations for repayments with filtering
    and reporting capabilities.
    """
    
    serializer_class = ActiveLoanRepaymentSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """Get queryset with proper filtering."""
        queryset = ActiveLoanRepayment.objects.select_related('active_loan__application')
        
        # Filter by active loan
        active_loan_id = self.request.query_params.get('active_loan')
        if active_loan_id:
            queryset = queryset.filter(active_loan_id=active_loan_id)
        
        # Filter by repayment type
        repayment_type = self.request.query_params.get('repayment_type')
        if repayment_type:
            queryset = queryset.filter(repayment_type=repayment_type)
        
        # Filter by late payments
        is_late = self.request.query_params.get('is_late')
        if is_late and is_late.lower() == 'true':
            queryset = queryset.filter(is_late=True)
        
        return queryset.order_by('-payment_date')


# Function-based view for getting active loan by application ID
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_active_loan_by_application(request, application_id):
    """Get active loan data for a specific application."""
    try:
        application = get_object_or_404(Application, id=application_id)
        
        # Check if application has an active loan
        try:
            active_loan = ActiveLoan.objects.get(application=application)
            serializer = ActiveLoanSerializer(active_loan)
            return Response(serializer.data)
        except ActiveLoan.DoesNotExist:
            return Response(
                {'message': 'No active loan found for this application'},
                status=status.HTTP_404_NOT_FOUND
            )
    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        ) 