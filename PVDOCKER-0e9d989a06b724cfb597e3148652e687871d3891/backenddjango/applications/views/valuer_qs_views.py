from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from ..models import Valuer, QuantitySurveyor
from ..serializers import (
    ValuerSerializer, QuantitySurveyorSerializer,
    ValuerListSerializer, QuantitySurveyorListSerializer
)
from users.permissions import IsAdmin, IsAdminOrBroker


class ValuerViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing valuers
    """
    queryset = Valuer.objects.all().order_by('company_name', 'contact_name')
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['company_name', 'contact_name', 'email', 'phone']
    ordering_fields = ['company_name', 'contact_name', 'created_at']
    
    def get_permissions(self):
        """
        Super user, accounts, and admin/broker users can manage valuers
        """
        user = getattr(self.request, 'user', None)
        if user and user.is_authenticated and getattr(user, 'role', None) in ['super_user', 'accounts']:
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsAuthenticated, IsAdminOrBroker]
        return [permission() for permission in permission_classes]
    
    def get_serializer_class(self):
        if self.action == 'list':
            # Use simplified serializer for listing (dropdown options)
            return ValuerListSerializer
        return ValuerSerializer
    
    def get_queryset(self):
        """
        Filter valuers based on user role and active status
        """
        user = self.request.user
        queryset = Valuer.objects.all().order_by('company_name', 'contact_name')
        
        # Super user and accounts can see all valuers
        if hasattr(user, 'role') and user.role in ['super_user', 'accounts']:
            pass  # No filtering needed
        # Admin can see all valuers
        elif user.role == 'admin':
            pass  # No filtering needed
        # Brokers can only see active valuers
        elif user.role == 'broker':
            queryset = queryset.filter(is_active=True)
        else:
            return queryset.none()
        
        # Filter by active status if requested
        is_active = self.request.query_params.get('is_active')
        if is_active is not None:
            queryset = queryset.filter(is_active=is_active.lower() == 'true')
        
        return queryset
    
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
    
    @action(detail=True, methods=['post'])
    def deactivate(self, request, pk=None):
        """
        Deactivate a valuer (soft delete)
        """
        valuer = self.get_object()
        valuer.is_active = False
        valuer.save()
        
        return Response({'status': 'Valuer deactivated successfully'})
    
    @action(detail=True, methods=['post'])
    def activate(self, request, pk=None):
        """
        Activate a valuer
        """
        valuer = self.get_object()
        valuer.is_active = True
        valuer.save()
        
        return Response({'status': 'Valuer activated successfully'})
    
    @action(detail=True, methods=['get'])
    def applications(self, request, pk=None):
        """
        Get all applications using this valuer
        """
        valuer = self.get_object()
        applications = valuer.applications.all()
        
        from ..serializers import ApplicationListSerializer
        serializer = ApplicationListSerializer(applications, many=True, context={'request': request})
        return Response(serializer.data)


class QuantitySurveyorViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing quantity surveyors
    """
    queryset = QuantitySurveyor.objects.all().order_by('company_name', 'contact_name')
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['company_name', 'contact_name', 'email', 'phone']
    ordering_fields = ['company_name', 'contact_name', 'created_at']
    
    def get_permissions(self):
        """
        Super user, accounts, and admin/broker users can manage quantity surveyors
        """
        user = getattr(self.request, 'user', None)
        if user and user.is_authenticated and getattr(user, 'role', None) in ['super_user', 'accounts']:
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsAuthenticated, IsAdminOrBroker]
        return [permission() for permission in permission_classes]
    
    def get_serializer_class(self):
        if self.action == 'list':
            # Use simplified serializer for listing (dropdown options)
            return QuantitySurveyorListSerializer
        return QuantitySurveyorSerializer
    
    def get_queryset(self):
        """
        Filter quantity surveyors based on user role and active status
        """
        user = self.request.user
        queryset = QuantitySurveyor.objects.all().order_by('company_name', 'contact_name')
        
        # Super user and accounts can see all quantity surveyors
        if hasattr(user, 'role') and user.role in ['super_user', 'accounts']:
            pass  # No filtering needed
        # Admin can see all quantity surveyors
        elif user.role == 'admin':
            pass  # No filtering needed
        # Brokers can only see active quantity surveyors
        elif user.role == 'broker':
            queryset = queryset.filter(is_active=True)
        else:
            return queryset.none()
        
        # Filter by active status if requested
        is_active = self.request.query_params.get('is_active')
        if is_active is not None:
            queryset = queryset.filter(is_active=is_active.lower() == 'true')
        
        return queryset
    
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
    
    @action(detail=True, methods=['post'])
    def deactivate(self, request, pk=None):
        """
        Deactivate a quantity surveyor (soft delete)
        """
        qs = self.get_object()
        qs.is_active = False
        qs.save()
        
        return Response({'status': 'Quantity Surveyor deactivated successfully'})
    
    @action(detail=True, methods=['post'])
    def activate(self, request, pk=None):
        """
        Activate a quantity surveyor
        """
        qs = self.get_object()
        qs.is_active = True
        qs.save()
        
        return Response({'status': 'Quantity Surveyor activated successfully'})
    
    @action(detail=True, methods=['get'])
    def applications(self, request, pk=None):
        """
        Get all applications using this quantity surveyor
        """
        qs = self.get_object()
        applications = qs.applications.all()
        
        from ..serializers import ApplicationListSerializer
        serializer = ApplicationListSerializer(applications, many=True, context={'request': request})
        return Response(serializer.data) 