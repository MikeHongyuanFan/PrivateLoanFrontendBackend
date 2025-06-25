from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from .models import Broker, Branch, BDM
from .serializers import (
    BrokerListSerializer,
    BrokerDetailSerializer,
    BranchSerializer,
    BDMSerializer,
    BrokerDropdownSerializer,
    BDMDropdownSerializer,
    BranchDropdownSerializer
)
from .filters import BrokerFilter, BranchFilter, BDMFilter
from users.permissions import IsAdmin, IsAdminOrBD, IsSuperUserOrAccounts, CanModifyCommissionAccount
from django.db.models import Count, Sum
from rest_framework.views import APIView


class BranchViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing branches
    """
    queryset = Branch.objects.all().order_by('name')
    serializer_class = BranchSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_class = BranchFilter
    search_fields = ['name']
    
    def get_permissions(self):
        user = getattr(self.request, 'user', None)
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            # Super user, accounts, and admin users can manage branches
            if user and user.is_authenticated and getattr(user, 'role', None) in ['super_user', 'accounts', 'admin']:
                permission_classes = [IsAuthenticated]
            else:
                permission_classes = [IsAuthenticated, IsAdmin]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]
    
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
    
    @action(detail=True, methods=['get'])
    def brokers(self, request, pk=None):
        """
        Get all brokers for a branch
        """
        branch = self.get_object()
        brokers = branch.branch_brokers.all()
        serializer = BrokerListSerializer(brokers, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def bdms(self, request, pk=None):
        """
        Get all BDMs for a branch
        """
        branch = self.get_object()
        bdms = branch.branch_bdms.all()
        serializer = BDMSerializer(bdms, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def applications(self, request, pk=None):
        """
        Get all applications for a branch
        """
        branch = self.get_object()
        from applications.serializers import ApplicationListSerializer
        applications = branch.branch_applications.all().order_by('-created_at')
        serializer = ApplicationListSerializer(applications, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def dropdown(self, request):
        """
        Get all branches in dropdown format for application creation
        """
        queryset = self.get_queryset().filter(is_active=True) if hasattr(Branch, 'is_active') else self.get_queryset()
        serializer = BranchDropdownSerializer(queryset, many=True)
        return Response(serializer.data)


class BrokerViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing brokers
    """
    queryset = Broker.objects.all().order_by('name')
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = BrokerFilter
    search_fields = ['name', 'company', 'email', 'phone']
    ordering_fields = ['name', 'created_at']
    
    def get_serializer_class(self):
        if self.action == 'list':
            return BrokerListSerializer
        return BrokerDetailSerializer
    
    def get_permissions(self):
        user = getattr(self.request, 'user', None)
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            # Super user, accounts, and admin users can manage brokers
            if user and user.is_authenticated and getattr(user, 'role', None) in ['super_user', 'accounts', 'admin']:
                permission_classes = [IsAuthenticated]
            else:
                permission_classes = [IsAuthenticated, IsAdmin]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]
    
    def get_queryset(self):
        user = self.request.user
        queryset = super().get_queryset()
        
        # Super user and accounts can see all brokers
        if hasattr(user, 'role') and user.role in ['super_user', 'accounts']:
            return queryset
        
        # Filter brokers based on user role
        if user.role == 'admin':
            return queryset
        elif user.role == 'bd':
            # BD users can see brokers assigned to their BDM profile
            if hasattr(user, 'bdm_profile'):
                return queryset.filter(bdms__id=user.bdm_profile.id)
            return queryset.none()
        elif user.role == 'broker':
            # Brokers can only see their own profile
            if hasattr(user, 'broker_profile'):
                return queryset.filter(id=user.broker_profile.id)
        
        return queryset.none()
    
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
    
    @action(detail=True, methods=['get'])
    def applications(self, request, pk=None):
        """
        Get all applications for a broker
        """
        broker = self.get_object()
        from applications.serializers import ApplicationListSerializer
        applications = broker.broker_applications.all().order_by('-created_at')
        serializer = ApplicationListSerializer(applications, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def related_borrowers(self, request, pk=None):
        """
        Get all borrowers related to a broker through applications
        """
        broker = self.get_object()
        from borrowers.serializers import BorrowerListSerializer
        
        # Get unique borrowers from all applications this broker is associated with
        borrower_ids = broker.broker_applications.values_list('borrowers__id', flat=True).distinct()
        
        # Filter out None values
        borrower_ids = [bid for bid in borrower_ids if bid is not None]
        
        if not borrower_ids:
            return Response([])
            
        # Get the borrower objects
        from borrowers.models import Borrower
        borrowers = Borrower.objects.filter(id__in=borrower_ids)
        
        # Serialize the borrowers
        serializer = BorrowerListSerializer(borrowers, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def stats(self, request, pk=None):
        """
        Get statistics for a broker
        """
        broker = self.get_object()
        
        # Get applications for this broker
        applications = broker.broker_applications.all()
        
        # Calculate statistics
        total_applications = applications.count()
        total_loan_amount = applications.aggregate(Sum('loan_amount'))['loan_amount__sum'] or 0
        
        # Applications by stage
        applications_by_stage = applications.values('stage').annotate(count=Count('id'))
        stage_stats = {item['stage']: item['count'] for item in applications_by_stage}
        
        # Applications by type
        applications_by_type = applications.values('application_type').annotate(count=Count('id'))
        type_stats = {item['application_type']: item['count'] for item in applications_by_type}
        
        return Response({
            'total_applications': total_applications,
            'total_loan_amount': total_loan_amount,
            'applications_by_stage': stage_stats,
            'applications_by_type': type_stats
        })
    
    @action(detail=False, methods=['get'])
    def dropdown(self, request):
        """
        Get all brokers in dropdown format for application creation
        """
        queryset = self.get_queryset()
        # For admins, show all brokers; for others, follow existing permissions
        if request.user.role == 'admin':
            queryset = Broker.objects.all().order_by('name')
        serializer = BrokerDropdownSerializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def lock_commission_account(self, request, pk=None):
        """
        Lock the commission account for a broker
        Only super user and accounts can lock commission accounts
        """
        broker = self.get_object()
        
        if not request.user.can_modify_commission_account():
            return Response(
                {"error": "Only super user and accounts can lock commission accounts"},
                status=status.HTTP_403_FORBIDDEN
            )
        
        try:
            broker.lock_commission_account(request.user)
            return Response({
                "message": "Commission account locked successfully",
                "commission_account_locked": True,
                "commission_account_locked_by": request.user.email,
                "commission_account_locked_at": broker.commission_account_locked_at
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {"error": f"Failed to lock commission account: {str(e)}"},
                status=status.HTTP_400_BAD_REQUEST
            )
    
    @action(detail=True, methods=['post'])
    def unlock_commission_account(self, request, pk=None):
        """
        Unlock the commission account for a broker
        Only super user and accounts can unlock commission accounts
        """
        broker = self.get_object()
        
        if not request.user.can_modify_commission_account():
            return Response(
                {"error": "Only super user and accounts can unlock commission accounts"},
                status=status.HTTP_403_FORBIDDEN
            )
        
        try:
            broker.unlock_commission_account(request.user)
            return Response({
                "message": "Commission account unlocked successfully",
                "commission_account_locked": False,
                "commission_account_locked_by": None,
                "commission_account_locked_at": None
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {"error": f"Failed to unlock commission account: {str(e)}"},
                status=status.HTTP_400_BAD_REQUEST
            )

    def list(self, request, *args, **kwargs):
        """Override list method to add debugging"""
        queryset = self.filter_queryset(self.get_queryset())
        
        # Debug: Check if brokers have branches
        for broker in queryset[:5]:  # Check first 5 brokers
            print(f"DEBUG: Broker {broker.id} ({broker.name}) - branch: {broker.branch}")
            if broker.branch:
                print(f"DEBUG: Broker {broker.id} branch name: {broker.branch.name}")
        
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class BDMViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing BDMs
    """
    queryset = BDM.objects.all().order_by('name')
    serializer_class = BDMSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_class = BDMFilter
    search_fields = ['name', 'email', 'phone']
    
    def get_permissions(self):
        user = getattr(self.request, 'user', None)
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            # Super user, accounts, and admin users can manage BDMs
            if user and user.is_authenticated and getattr(user, 'role', None) in ['super_user', 'accounts', 'admin']:
                permission_classes = [IsAuthenticated]
            else:
                permission_classes = [IsAuthenticated, IsAdmin]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]
    
    def get_queryset(self):
        user = self.request.user
        queryset = super().get_queryset()
        
        # Super user and accounts can see all BDMs
        if hasattr(user, 'role') and user.role in ['super_user', 'accounts']:
            return queryset
        
        # Filter BDMs based on user role
        if user.role == 'admin':
            return queryset
        elif user.role == 'bd':
            # BDs can only see their own profile
            if hasattr(user, 'bdm_profile'):
                return queryset.filter(id=user.bdm_profile.id)
        
        return queryset.none()
    
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
    
    @action(detail=False, methods=['post'])
    def create_with_branch(self, request):
        """
        Create a BDM with branch information in a single request
        """
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(created_by=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['get'])
    def applications(self, request, pk=None):
        """
        Get all applications for a BDM
        """
        bdm = self.get_object()
        from applications.serializers import ApplicationListSerializer
        applications = bdm.bdm_applications.all().order_by('-created_at')
        serializer = ApplicationListSerializer(applications, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def brokers(self, request, pk=None):
        """
        Get all brokers assigned to a BDM
        """
        bdm = self.get_object()
        brokers = bdm.bdm_brokers.all().order_by('name')
        serializer = BrokerListSerializer(brokers, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['post'])
    def claim_application(self, request):
        """
        Allow a BD to claim an unassigned application
        """
        # Ensure user is a BD
        if request.user.role != 'bd':
            return Response(
                {"error": "Only Business Developers can claim applications"},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Validate input
        application_id = request.data.get('application_id')
        if not application_id:
            return Response(
                {"error": "application_id is required"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Get the application
        from applications.models import Application
        try:
            application = Application.objects.get(id=application_id)
        except Application.DoesNotExist:
            return Response(
                {"error": "Application not found"},
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Check if application is already assigned
        if application.assigned_bd:
            return Response(
                {"error": "Application is already assigned to a BD"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Assign the application to the BD
        application.assigned_bd = request.user
        application.save()
        
        # Create notification for the BD
        from users.models import Notification
        Notification.objects.create(
            user=request.user,
            title=f"Application Claimed: {application.reference_number}",
            message=f"You have successfully claimed application {application.reference_number}",
            notification_type="application_status",
            related_object_id=application.id
        )
        
        # Create a note about the claim
        from documents.models import Note
        Note.objects.create(
            application=application,
            content=f"Application claimed by BD: {request.user.get_full_name() or request.user.email}",
            created_by=request.user
        )
        
        return Response({"message": "Application claimed successfully"}, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['get'])
    def dropdown(self, request):
        """
        Get all BDMs in dropdown format for application creation
        """
        queryset = self.get_queryset()
        # For admins, show all BDMs; for others, follow existing permissions
        if request.user.role == 'admin':
            queryset = BDM.objects.all().order_by('name')
        serializer = BDMDropdownSerializer(queryset, many=True)
        return Response(serializer.data)
