from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Borrower, Guarantor, Asset, Liability
from applications.serializers import CompanyAssetSerializer, GuarantorAssetSerializer
from rest_framework.permissions import IsAuthenticated
from .serializers import GuarantorSerializer, BorrowerListSerializer, BorrowerDetailSerializer
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q
from users.permissions import IsAdminOrBrokerOrBD

class BorrowerViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing borrowers
    """
    queryset = Borrower.objects.all()
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['first_name', 'last_name', 'email', 'company_name']
    filterset_fields = {
        'first_name': ['exact', 'icontains'],
        'last_name': ['exact', 'icontains'],
        'email': ['exact', 'icontains'],
        'is_company': ['exact'],
        'company_name': ['exact', 'icontains'],
        'created_at': ['gte', 'lte'],
    }
    ordering_fields = ['first_name', 'last_name', 'email', 'created_at', 'company_name']
    ordering = ['-created_at']
    
    def get_permissions(self):
        """
        Super user, accounts, and admin/broker/BD users can manage borrowers
        """
        user = getattr(self.request, 'user', None)
        if user and user.is_authenticated and getattr(user, 'role', None) in ['super_user', 'accounts']:
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsAuthenticated, IsAdminOrBrokerOrBD]
        return [permission() for permission in permission_classes]
    
    def get_serializer_class(self):
        if self.action == 'list':
            return BorrowerListSerializer
        return BorrowerDetailSerializer
    
    def get_queryset(self):
        """
        Filter borrowers based on user role
        """
        user = self.request.user
        queryset = super().get_queryset()
        
        # Super user and accounts can see all borrowers
        if hasattr(user, 'role') and user.role in ['super_user', 'accounts']:
            return queryset
        # Admin can see all borrowers
        elif user.role == 'admin':
            return queryset
        # Brokers can only see borrowers from their applications
        elif user.role == 'broker':
            return queryset.filter(applications__broker__user=user).distinct()
        # BDs can only see borrowers from their assigned applications
        elif user.role == 'bd':
            if hasattr(user, 'bdm_profile'):
                return queryset.filter(applications__bd=user.bdm_profile).distinct()
            return queryset.none()
        # Clients can only see their own borrower profile
        elif user.role == 'client':
            if hasattr(user, 'borrower_profile'):
                return queryset.filter(id=user.borrower_profile.id)
            return queryset.none()
        
        return queryset.none()

class BorrowerAssetViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing company borrower assets
    """
    serializer_class = CompanyAssetSerializer
    
    def get_permissions(self):
        """
        Super user, accounts, and admin/broker/BD users can manage borrower assets
        """
        user = getattr(self.request, 'user', None)
        if user and user.is_authenticated and getattr(user, 'role', None) in ['super_user', 'accounts']:
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsAuthenticated, IsAdminOrBrokerOrBD]
        return [permission() for permission in permission_classes]
    
    def get_queryset(self):
        """
        Get assets for a specific borrower based on user role
        """
        user = self.request.user
        borrower_id = self.kwargs.get('borrower_id')
        queryset = Asset.objects.filter(borrower_id=borrower_id)
        
        # Super user and accounts can see all assets
        if hasattr(user, 'role') and user.role in ['super_user', 'accounts']:
            return queryset
        # Admin can see all assets
        elif user.role == 'admin':
            return queryset
        # Brokers can only see assets from their applications' borrowers
        elif user.role == 'broker':
            return queryset.filter(borrower__applications__broker__user=user)
        # BDs can only see assets from their assigned applications' borrowers
        elif user.role == 'bd':
            if hasattr(user, 'bdm_profile'):
                return queryset.filter(borrower__applications__bd=user.bdm_profile)
            return queryset.none()
        # Clients can only see their own assets
        elif user.role == 'client':
            if hasattr(user, 'borrower_profile'):
                return queryset.filter(borrower=user.borrower_profile)
            return queryset.none()
        
        return queryset.none()
    
    def perform_create(self, serializer):
        """
        Create a new asset for a borrower
        """
        borrower_id = self.kwargs.get('borrower_id')
        borrower = Borrower.objects.get(id=borrower_id)
        serializer.save(borrower=borrower, created_by=self.request.user)


class GuarantorAssetViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing guarantor assets
    """
    serializer_class = GuarantorAssetSerializer
    
    def get_permissions(self):
        """
        Super user, accounts, and admin/broker/BD users can manage guarantor assets
        """
        user = getattr(self.request, 'user', None)
        if user and user.is_authenticated and getattr(user, 'role', None) in ['super_user', 'accounts']:
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsAuthenticated, IsAdminOrBrokerOrBD]
        return [permission() for permission in permission_classes]
    
    def get_queryset(self):
        """
        Get assets for a specific guarantor based on user role
        """
        user = self.request.user
        guarantor_id = self.kwargs.get('guarantor_id')
        queryset = Asset.objects.filter(guarantor_id=guarantor_id)
        
        # Super user and accounts can see all assets
        if hasattr(user, 'role') and user.role in ['super_user', 'accounts']:
            return queryset
        # Admin can see all assets
        elif user.role == 'admin':
            return queryset
        # Brokers can only see assets from their applications' guarantors
        elif user.role == 'broker':
            return queryset.filter(guarantor__application__broker__user=user)
        # BDs can only see assets from their assigned applications' guarantors
        elif user.role == 'bd':
            if hasattr(user, 'bdm_profile'):
                return queryset.filter(guarantor__application__bd=user.bdm_profile)
            return queryset.none()
        # Clients can only see assets from guarantors of their applications
        elif user.role == 'client':
            if hasattr(user, 'borrower_profile'):
                return queryset.filter(guarantor__application__borrowers=user.borrower_profile)
            return queryset.none()
        
        return queryset.none()
    
    def perform_create(self, serializer):
        """
        Create a new asset for a guarantor
        """
        guarantor_id = self.kwargs.get('guarantor_id')
        guarantor = Guarantor.objects.get(id=guarantor_id)
        serializer.save(guarantor=guarantor, created_by=self.request.user)


class GuarantorViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing guarantors
    """
    queryset = Guarantor.objects.all()
    serializer_class = GuarantorSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['first_name', 'last_name', 'email', 'company_name']
    filterset_fields = {
        'first_name': ['exact', 'icontains'],
        'last_name': ['exact', 'icontains'],
        'email': ['exact', 'icontains'],
        'guarantor_type': ['exact'],
        'company_name': ['exact', 'icontains'],
        'created_at': ['gte', 'lte'],
        'borrower': ['exact'],
        'application': ['exact'],
    }
    ordering_fields = ['first_name', 'last_name', 'email', 'created_at', 'company_name']
    ordering = ['-created_at']
    
    def get_permissions(self):
        """
        Super user, accounts, and admin/broker/BD users can manage guarantors
        """
        user = getattr(self.request, 'user', None)
        if user and user.is_authenticated and getattr(user, 'role', None) in ['super_user', 'accounts']:
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsAuthenticated, IsAdminOrBrokerOrBD]
        return [permission() for permission in permission_classes]
    
    def get_queryset(self):
        """
        Filter guarantors based on user role
        """
        user = self.request.user
        queryset = super().get_queryset()
        
        # Super user and accounts can see all guarantors
        if hasattr(user, 'role') and user.role in ['super_user', 'accounts']:
            return queryset
        # Admin can see all guarantors
        elif user.role == 'admin':
            return queryset
        # Brokers can only see guarantors from their applications
        elif user.role == 'broker':
            return queryset.filter(application__broker__user=user)
        # BDs can only see guarantors from their assigned applications
        elif user.role == 'bd':
            if hasattr(user, 'bdm_profile'):
                return queryset.filter(application__bd=user.bdm_profile)
            return queryset.none()
        # Clients can only see guarantors from their applications
        elif user.role == 'client':
            if hasattr(user, 'borrower_profile'):
                return queryset.filter(application__borrowers=user.borrower_profile)
            return queryset.none()
        
        return queryset.none()
