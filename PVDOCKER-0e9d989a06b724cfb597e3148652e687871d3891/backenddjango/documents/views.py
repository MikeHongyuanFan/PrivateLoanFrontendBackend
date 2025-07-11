from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
from rest_framework.parsers import MultiPartParser, FormParser
from django_filters.rest_framework import DjangoFilterBackend
from django.utils import timezone
from .models import Document, Note, Fee, Repayment, Ledger, NoteComment
from .serializers import (
    DocumentSerializer,
    NoteSerializer,
    FeeSerializer,
    RepaymentSerializer,
    LedgerSerializer,
    ApplicationLedgerSerializer,
    NoteCommentSerializer
)
from .filters import DocumentFilter, NoteFilter, FeeFilter, RepaymentFilter, NoteCommentFilter
from users.permissions import IsAdmin, IsAdminOrBroker, IsAdminOrBD, IsAdminOrBrokerOrBD, CanAccessNote
from django.http import FileResponse
import os
from django.db.models import Q
from applications.models import Application
from django.db.models import Sum, F


class DocumentViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing documents with enhanced search capabilities
    """
    queryset = Document.objects.all().order_by('-created_at')
    serializer_class = DocumentSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = DocumentFilter
    search_fields = [
        'title', 'description', 'file_name',
        'application__reference_number',
        'borrower__first_name', 'borrower__last_name',
        'borrower__email',
        'borrower__residential_address',
        'borrower__mailing_address',
        'borrower__registered_address_street_no',
        'borrower__registered_address_street_name',
        'borrower__registered_address_suburb',
        'borrower__registered_address_state',
        'borrower__registered_address_postcode',
        'borrower__company_address'
    ]
    ordering_fields = ['created_at', 'updated_at', 'title']
    parser_classes = [MultiPartParser, FormParser]
    
    def get_permissions(self):
        user = getattr(self.request, 'user', None)
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            # Super user, accounts, and admin/broker/BD users can manage documents
            if user and user.is_authenticated and getattr(user, 'role', None) in ['super_user', 'accounts']:
                permission_classes = [IsAuthenticated]
            else:
                permission_classes = [IsAdminOrBrokerOrBD]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]
    
    def get_queryset(self):
        # Get base queryset with optimized joins
        queryset = super().get_queryset().select_related(
            'application',
            'borrower',
            'created_by'
        ).prefetch_related(
            'application__borrowers'
        )
        
        # Apply role-based filtering
        user = self.request.user
        if not hasattr(user, 'role') or user.role not in ['super_user', 'accounts', 'admin']:
            if user.role == 'broker':
                queryset = queryset.filter(application__broker__user=user)
            elif user.role == 'bd':
                if hasattr(user, 'bdm_profile'):
                    queryset = queryset.filter(application__bd=user.bdm_profile)
                else:
                    return queryset.none()
            elif user.role == 'client':
                if hasattr(user, 'borrower_profile'):
                    queryset = queryset.filter(
                        Q(application__borrowers=user.borrower_profile) |
                        Q(borrower=user.borrower_profile)
                    )
                else:
                    return queryset.none()
            else:
                return queryset.none()
        
        # Get search parameters
        search_query = self.request.query_params.get('search', '')
        app_search = self.request.query_params.get('application_search', '')
        borrower_search = self.request.query_params.get('borrower_search', '')
        
        # Create filter instance
        document_filter = self.filterset_class()
        
        # Apply search filters if provided
        if search_query:
            queryset = document_filter.search_filter(queryset, 'search', search_query)
        if app_search:
            queryset = document_filter.application_search_filter(queryset, 'application_search', app_search)
        if borrower_search:
            queryset = document_filter.borrower_search_filter(queryset, 'borrower_search', borrower_search)
        
        return queryset.distinct()
    
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
    
    @action(detail=True, methods=['get'])
    def download(self, request, pk=None):
        """
        Download a document
        """
        document = self.get_object()
        file_path = document.file.path
        
        if os.path.exists(file_path):
            return FileResponse(open(file_path, 'rb'), as_attachment=True, filename=document.file_name)
        else:
            return Response({'error': 'File not found'}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=True, methods=['get'])
    def preview(self, request, pk=None):
        """
        Preview a document in the browser
        """
        document = self.get_object()
        file_path = document.file.path
        
        if not os.path.exists(file_path):
            return Response({'error': 'File not found'}, status=status.HTTP_404_NOT_FOUND)
        
        # Get file extension to determine content type
        file_extension = os.path.splitext(document.file_name)[1].lower()
        
        # Define content types for different file types
        content_types = {
            '.pdf': 'application/pdf',
            '.jpg': 'image/jpeg',
            '.jpeg': 'image/jpeg',
            '.png': 'image/png',
            '.gif': 'image/gif',
            '.txt': 'text/plain',
            '.html': 'text/html',
            '.htm': 'text/html',
        }
        
        content_type = content_types.get(file_extension, 'application/octet-stream')
        
        # For PDFs and images, serve directly for preview
        if file_extension in ['.pdf', '.jpg', '.jpeg', '.png', '.gif']:
            return FileResponse(
                open(file_path, 'rb'),
                content_type=content_type,
                filename=document.file_name
            )
        
        # For other file types, return a message suggesting download
        return Response({
            'error': 'Preview not available for this file type',
            'file_type': file_extension,
            'suggestion': 'Use the download function for this file type'
        }, status=status.HTTP_400_BAD_REQUEST)


class DocumentCreateVersionView(GenericAPIView):
    """
    API endpoint for creating a new version of a document
    """
    serializer_class = DocumentSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]
    
    def get_permissions(self):
        user = getattr(self.request, 'user', None)
        # Super user, accounts, and admin/broker/BD users can create document versions
        if user and user.is_authenticated and getattr(user, 'role', None) in ['super_user', 'accounts']:
            return [IsAuthenticated()]
        return [IsAdminOrBrokerOrBD()]
    
    def post(self, request, pk):
        try:
            document = Document.objects.get(pk=pk)
        except Document.DoesNotExist:
            return Response({'error': 'Document not found'}, status=status.HTTP_404_NOT_FOUND)
        
        # Create a new document with the same metadata but new file
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            new_document = serializer.save(
                title=document.title,
                description=document.description,
                document_type=document.document_type,
                application=document.application,
                borrower=document.borrower,
                created_by=request.user,
                version=document.version + 1,
                previous_version=document
            )
            return Response(self.get_serializer(new_document).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class NoteViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing notes
    """
    queryset = Note.objects.all().order_by('-created_at')
    serializer_class = NoteSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = NoteFilter
    search_fields = ['title', 'content']
    ordering_fields = ['created_at', 'updated_at', 'title', 'remind_date']
    
    def get_permissions(self):
        user = getattr(self.request, 'user', None)
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            # Super user, accounts, and admin/broker/BD users can manage notes
            if user and user.is_authenticated and getattr(user, 'role', None) in ['super_user', 'accounts']:
                permission_classes = [IsAuthenticated]
            else:
                permission_classes = [IsAdminOrBrokerOrBD]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]
    
    def get_queryset(self):
        user = self.request.user
        queryset = super().get_queryset()
        
        # Super user and accounts can see all notes
        if hasattr(user, 'role') and user.role in ['super_user', 'accounts']:
            return queryset
        
        # Filter notes based on user role
        if user.role == 'admin':
            return queryset
        elif user.role == 'broker':
            return queryset.filter(application__broker__user=user)
        elif user.role == 'bd':
            # Check if user has a BDM profile
            if hasattr(user, 'bdm_profile'):
                return queryset.filter(application__bd=user.bdm_profile)
            return queryset.none()
        elif user.role == 'client':
            # Clients can only see notes associated with their borrower profile
            if hasattr(user, 'borrower_profile'):
                return queryset.filter(
                    application__borrowers=user.borrower_profile
                ) | queryset.filter(
                    borrower=user.borrower_profile
                )
        
        return queryset.none()
    
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
    
    @action(detail=True, methods=['get'])
    def comments(self, request, pk=None):
        """
        Get all comments for a note
        """
        note = self.get_object()
        comments = note.comments.all()
        serializer = NoteCommentSerializer(comments, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def add_comment(self, request, pk=None):
        """
        Add a comment to a note
        """
        note = self.get_object()
        # Create a copy of the request data to avoid modifying the original
        data = request.data.copy()
        # Add the note ID to the data
        data['note'] = note.id
        serializer = NoteCommentSerializer(data=data)
        
        if serializer.is_valid():
            serializer.save(note=note, created_by=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class NoteCommentViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing note comments
    """
    queryset = NoteComment.objects.all().order_by('created_at')
    serializer_class = NoteCommentSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = NoteCommentFilter
    search_fields = ['content']
    ordering_fields = ['created_at']
    
    def get_permissions(self):
        user = getattr(self.request, 'user', None)
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            # Super user, accounts, and admin/broker/BD users can manage note comments
            if user and user.is_authenticated and getattr(user, 'role', None) in ['super_user', 'accounts']:
                permission_classes = [IsAuthenticated]
            else:
                permission_classes = [IsAdminOrBrokerOrBD]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]
    
    def get_queryset(self):
        user = self.request.user
        queryset = super().get_queryset()
        
        # Super user and accounts can see all note comments
        if hasattr(user, 'role') and user.role in ['super_user', 'accounts']:
            return queryset
        
        # Filter comments based on user role
        if user.role == 'admin':
            return queryset
        elif user.role == 'broker':
            return queryset.filter(note__application__broker__user=user)
        elif user.role == 'bd':
            # Check if user has a BDM profile
            if hasattr(user, 'bdm_profile'):
                return queryset.filter(note__application__bd=user.bdm_profile)
            return queryset.none()
        elif user.role == 'client':
            # Clients can only see comments associated with their borrower profile
            if hasattr(user, 'borrower_profile'):
                return queryset.filter(
                    note__application__borrowers=user.borrower_profile
                ) | queryset.filter(
                    note__borrower=user.borrower_profile
                )
        
        return queryset.none()
    
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class FeeViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing fees
    """
    queryset = Fee.objects.all().order_by('due_date')
    serializer_class = FeeSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = FeeFilter
    search_fields = ['description']
    ordering_fields = ['due_date', 'paid_date', 'amount', 'fee_type']
    
    def get_permissions(self):
        user = getattr(self.request, 'user', None)
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            # Super user, accounts, and admin/broker/BD users can manage fees
            if user and user.is_authenticated and getattr(user, 'role', None) in ['super_user', 'accounts']:
                permission_classes = [IsAuthenticated]
            else:
                permission_classes = [IsAdminOrBD]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]
    
    def get_queryset(self):
        user = self.request.user
        queryset = super().get_queryset()
        
        # Filter fees based on user role
        if user.role == 'admin':
            return queryset
        elif user.role == 'broker':
            return queryset.filter(application__broker__user=user)
        elif user.role == 'bd':
            # Check if user has a BDM profile
            if hasattr(user, 'bdm_profile'):
                return queryset.filter(application__bd=user.bdm_profile)
            return queryset.none()
        elif user.role == 'client':
            # Clients can only see fees associated with their borrower profile
            if hasattr(user, 'borrower_profile'):
                return queryset.filter(application__borrowers=user.borrower_profile)
        
        return queryset.none()
    
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
    
    @action(detail=True, methods=['get'])
    def download_invoice(self, request, pk=None):
        """
        Download a fee invoice
        """
        fee = self.get_object()
        
        if not fee.invoice:
            return Response({'error': 'No invoice file found for this fee'}, status=status.HTTP_404_NOT_FOUND)
        
        file_path = fee.invoice.path
        
        if os.path.exists(file_path):
            return FileResponse(open(file_path, 'rb'), as_attachment=True, filename=os.path.basename(fee.invoice.name))
        else:
            return Response({'error': 'Invoice file not found'}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=True, methods=['get'])
    def preview_invoice(self, request, pk=None):
        """
        Preview a fee invoice in the browser
        """
        fee = self.get_object()
        
        if not fee.invoice:
            return Response({'error': 'No invoice file found for this fee'}, status=status.HTTP_404_NOT_FOUND)
        
        file_path = fee.invoice.path
        
        if not os.path.exists(file_path):
            return Response({'error': 'Invoice file not found'}, status=status.HTTP_404_NOT_FOUND)
        
        # Get file extension to determine content type
        file_extension = os.path.splitext(fee.invoice.name)[1].lower()
        
        # Define content types for different file types
        content_types = {
            '.pdf': 'application/pdf',
            '.jpg': 'image/jpeg',
            '.jpeg': 'image/jpeg',
            '.png': 'image/png',
            '.gif': 'image/gif',
            '.txt': 'text/plain',
            '.html': 'text/html',
            '.htm': 'text/html',
        }
        
        content_type = content_types.get(file_extension, 'application/octet-stream')
        
        # For PDFs and images, serve directly for preview
        if file_extension in ['.pdf', '.jpg', '.jpeg', '.png', '.gif']:
            return FileResponse(
                open(file_path, 'rb'),
                content_type=content_type,
                filename=os.path.basename(fee.invoice.name)
            )
        
        # For other file types, return a message suggesting download
        return Response({
            'error': 'Preview not available for this file type',
            'file_type': file_extension,
            'suggestion': 'Use the download function for this file type'
        }, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'])
    def compliance(self, request):
        """
        Get fee compliance statistics for dashboard
        """
        queryset = self.get_queryset()
        
        # Calculate statistics
        total_fees = queryset.count()
        total_amount_due = queryset.aggregate(total=Sum('amount'))['total'] or 0
        total_amount_paid = queryset.filter(paid_date__isnull=False).aggregate(total=Sum('amount'))['total'] or 0
        
        # Count paid fees
        paid_fees = queryset.filter(paid_date__isnull=False).count()
        paid_on_time = queryset.filter(
            paid_date__isnull=False,
            paid_date__lte=F('due_date')
        ).count()
        paid_late = paid_fees - paid_on_time
        
        # Count overdue fees
        today = timezone.now().date()
        missed = queryset.filter(
            paid_date__isnull=True,
            due_date__lt=today
        ).count()
        
        return Response({
            'total_fees': total_fees,
            'total_amount_due': total_amount_due,
            'total_amount_paid': total_amount_paid,
            'paid_on_time': paid_on_time,
            'paid_late': paid_late,
            'missed': missed
        })


class FeeMarkPaidView(GenericAPIView):
    """
    API endpoint for marking a fee as paid
    """
    serializer_class = FeeSerializer
    permission_classes = [IsAuthenticated]
    
    def get_permissions(self):
        user = getattr(self.request, 'user', None)
        # Super user, accounts, and admin/BD users can mark fees as paid
        if user and user.is_authenticated and getattr(user, 'role', None) in ['super_user', 'accounts']:
            return [IsAuthenticated()]
        return [IsAdminOrBD()]
    
    def get_queryset(self):
        """
        Filter fees based on user permissions
        """
        user = self.request.user
        queryset = Fee.objects.all()
        
        # Apply role-based filtering
        if user.role == 'admin':
            return queryset
        elif user.role == 'broker':
            return queryset.filter(application__broker__user=user)
        elif user.role == 'bd':
            # Check if user has a BDM profile
            if hasattr(user, 'bdm_profile'):
                return queryset.filter(application__bd=user.bdm_profile)
            return queryset.none()
        elif user.role == 'client':
            # Clients can only see fees associated with their borrower profile
            if hasattr(user, 'borrower_profile'):
                return queryset.filter(application__borrowers=user.borrower_profile)
        
        return queryset.none()
    
    def post(self, request, pk):
        try:
            # Get the fee with proper permission filtering
            fee = self.get_queryset().get(pk=pk)
        except Fee.DoesNotExist:
            return Response({'error': 'Fee not found or you do not have permission to access it'}, status=status.HTTP_404_NOT_FOUND)
        
        try:
            # Mark the fee as paid
            paid_date = request.data.get('paid_date')
            if paid_date:
                # Convert string date to date object if needed
                if isinstance(paid_date, str):
                    from datetime import datetime
                    paid_date = datetime.strptime(paid_date, '%Y-%m-%d').date()
            else:
                paid_date = timezone.now().date()
            
            fee.paid_date = paid_date
            fee.save()
            
            return Response(self.get_serializer(fee).data)
        except Exception as e:
            return Response({'error': f'Failed to mark fee as paid: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class RepaymentViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing repayments
    """
    queryset = Repayment.objects.all().order_by('due_date')
    serializer_class = RepaymentSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = RepaymentFilter
    ordering_fields = ['due_date', 'paid_date', 'amount']
    
    def get_permissions(self):
        user = getattr(self.request, 'user', None)
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            # Super user, accounts, and admin/BD users can manage repayments
            if user and user.is_authenticated and getattr(user, 'role', None) in ['super_user', 'accounts']:
                permission_classes = [IsAuthenticated]
            else:
                permission_classes = [IsAdminOrBD]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]
    
    def get_queryset(self):
        user = self.request.user
        queryset = super().get_queryset()
        
        # Filter repayments based on user role
        if user.role == 'admin':
            return queryset
        elif user.role == 'broker':
            return queryset.filter(application__broker__user=user)
        elif user.role == 'bd':
            # Check if user has a BDM profile
            if hasattr(user, 'bdm_profile'):
                return queryset.filter(application__bd=user.bdm_profile)
            return queryset.none()
        elif user.role == 'client':
            # Clients can only see repayments associated with their borrower profile
            if hasattr(user, 'borrower_profile'):
                return queryset.filter(application__borrowers=user.borrower_profile)
        
        return queryset.none()
    
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
    
    @action(detail=True, methods=['get'])
    def download_invoice(self, request, pk=None):
        """
        Download a repayment invoice
        """
        repayment = self.get_object()
        
        if not repayment.invoice:
            return Response({'error': 'No invoice file found for this repayment'}, status=status.HTTP_404_NOT_FOUND)
        
        file_path = repayment.invoice.path
        
        if os.path.exists(file_path):
            return FileResponse(open(file_path, 'rb'), as_attachment=True, filename=os.path.basename(repayment.invoice.name))
        else:
            return Response({'error': 'Invoice file not found'}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=True, methods=['get'])
    def preview_invoice(self, request, pk=None):
        """
        Preview a repayment invoice in the browser
        """
        repayment = self.get_object()
        
        if not repayment.invoice:
            return Response({'error': 'No invoice file found for this repayment'}, status=status.HTTP_404_NOT_FOUND)
        
        file_path = repayment.invoice.path
        
        if not os.path.exists(file_path):
            return Response({'error': 'Invoice file not found'}, status=status.HTTP_404_NOT_FOUND)
        
        # Get file extension to determine content type
        file_extension = os.path.splitext(repayment.invoice.name)[1].lower()
        
        # Define content types for different file types
        content_types = {
            '.pdf': 'application/pdf',
            '.jpg': 'image/jpeg',
            '.jpeg': 'image/jpeg',
            '.png': 'image/png',
            '.gif': 'image/gif',
            '.txt': 'text/plain',
            '.html': 'text/html',
            '.htm': 'text/html',
        }
        
        content_type = content_types.get(file_extension, 'application/octet-stream')
        
        # For PDFs and images, serve directly for preview
        if file_extension in ['.pdf', '.jpg', '.jpeg', '.png', '.gif']:
            return FileResponse(
                open(file_path, 'rb'),
                content_type=content_type,
                filename=os.path.basename(repayment.invoice.name)
            )
        
        # For other file types, return a message suggesting download
        return Response({
            'error': 'Preview not available for this file type',
            'file_type': file_extension,
            'suggestion': 'Use the download function for this file type'
        }, status=status.HTTP_400_BAD_REQUEST)


class RepaymentMarkPaidView(GenericAPIView):
    """
    API endpoint for marking a repayment as paid
    """
    serializer_class = RepaymentSerializer
    permission_classes = [IsAuthenticated]
    
    def get_permissions(self):
        user = getattr(self.request, 'user', None)
        # Super user, accounts, and admin/BD users can mark repayments as paid
        if user and user.is_authenticated and getattr(user, 'role', None) in ['super_user', 'accounts']:
            return [IsAuthenticated()]
        return [IsAdminOrBD()]
    
    def get_queryset(self):
        """
        Filter repayments based on user permissions
        """
        user = self.request.user
        queryset = Repayment.objects.all()
        
        # Apply role-based filtering
        if user.role == 'admin':
            return queryset
        elif user.role == 'broker':
            return queryset.filter(application__broker__user=user)
        elif user.role == 'bd':
            # Check if user has a BDM profile
            if hasattr(user, 'bdm_profile'):
                return queryset.filter(application__bd=user.bdm_profile)
            return queryset.none()
        elif user.role == 'client':
            # Clients can only see repayments associated with their borrower profile
            if hasattr(user, 'borrower_profile'):
                return queryset.filter(application__borrowers=user.borrower_profile)
        
        return queryset.none()
    
    def post(self, request, pk):
        try:
            # Get the repayment with proper permission filtering
            repayment = self.get_queryset().get(pk=pk)
        except Repayment.DoesNotExist:
            return Response({'error': 'Repayment not found or you do not have permission to access it'}, status=status.HTTP_404_NOT_FOUND)
        
        try:
            # Mark the repayment as paid
            paid_date = request.data.get('paid_date')
            if paid_date:
                # Convert string date to date object if needed
                if isinstance(paid_date, str):
                    from datetime import datetime
                    paid_date = datetime.strptime(paid_date, '%Y-%m-%d').date()
            else:
                paid_date = timezone.now().date()
            
            repayment.paid_date = paid_date
            repayment.save()
            
            return Response(self.get_serializer(repayment).data)
        except Exception as e:
            return Response({'error': f'Failed to mark repayment as paid: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ApplicationLedgerView(GenericAPIView):
    """
    API endpoint for getting the ledger for an application
    """
    permission_classes = [IsAuthenticated]
    serializer_class = ApplicationLedgerSerializer
    
    def get(self, request, application_id):
        # Check if the user has access to this application
        user = request.user
        
        if user.role == 'admin':
            pass  # Admin has access to all applications
        elif user.role == 'broker':
            if not Application.objects.filter(id=application_id, broker__user=user).exists():
                return Response({'error': 'You do not have access to this application'}, status=status.HTTP_403_FORBIDDEN)
        elif user.role == 'bd':
            # Check if user has a BDM profile
            if hasattr(user, 'bdm_profile'):
                if not Application.objects.filter(id=application_id, bd=user.bdm_profile).exists():
                    return Response({'error': 'You do not have access to this application'}, status=status.HTTP_403_FORBIDDEN)
            else:
                return Response({'error': 'You do not have access to this application'}, status=status.HTTP_403_FORBIDDEN)
        elif user.role == 'client':
            if hasattr(user, 'borrower_profile'):
                if not Application.objects.filter(id=application_id, borrowers=user.borrower_profile).exists():
                    return Response({'error': 'You do not have access to this application'}, status=status.HTTP_403_FORBIDDEN)
            else:
                return Response({'error': 'You do not have access to this application'}, status=status.HTTP_403_FORBIDDEN)
        else:
            return Response({'error': 'You do not have access to this application'}, status=status.HTTP_403_FORBIDDEN)
        
        # Get the application
        try:
            application = Application.objects.get(pk=application_id)
        except Application.DoesNotExist:
            return Response({'error': 'Application not found'}, status=status.HTTP_404_NOT_FOUND)
        
        # Get the ledger entries
        ledger_entries = Ledger.objects.filter(application=application).order_by('-transaction_date')
        
        # Get the fees and repayments
        fees = Fee.objects.filter(application=application).order_by('due_date')
        repayments = Repayment.objects.filter(application=application).order_by('due_date')
        
        # Serialize the data
        serializer = ApplicationLedgerSerializer({
            'application': application,
            'ledger_entries': ledger_entries,
            'fees': fees,
            'repayments': repayments
        })
        
        return Response(serializer.data)
