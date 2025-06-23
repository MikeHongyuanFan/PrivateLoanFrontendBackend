from rest_framework import serializers
from .models import Document, Note, Fee, Repayment, Ledger, NoteComment


class DocumentSerializer(serializers.ModelSerializer):
    """
    Serializer for documents with enhanced application and borrower details
    """
    document_type_display = serializers.CharField(source='get_document_type_display', read_only=True)
    created_by_name = serializers.StringRelatedField(source='created_by')
    file_url = serializers.SerializerMethodField()
    
    # Application details
    application_reference = serializers.CharField(source='application.reference_number', read_only=True)
    application_stage = serializers.CharField(source='application.stage', read_only=True)
    
    # Borrower details
    borrower_name = serializers.SerializerMethodField()
    borrower_email = serializers.EmailField(source='borrower.email', read_only=True)
    borrower_address = serializers.SerializerMethodField()
    
    class Meta:
        model = Document
        fields = '__all__'
        read_only_fields = [
            'file_name', 'file_size', 'file_type', 'version', 
            'created_by', 'created_at', 'updated_at',
            'application_reference', 'application_stage',
            'borrower_name', 'borrower_email', 'borrower_address'
        ]
        extra_kwargs = {
            'title': {'required': False, 'allow_null': True, 'allow_blank': True},
            'description': {'required': False, 'allow_null': True, 'allow_blank': True},
            'document_type': {'required': False, 'allow_null': True, 'allow_blank': True},
            'file': {'required': False, 'allow_null': True},
            'application': {'required': False, 'allow_null': True},
            'borrower': {'required': False, 'allow_null': True},
        }
    
    def get_file_url(self, obj) -> str:
        if obj.file:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.file.url)
        return None
    
    def get_borrower_name(self, obj) -> str:
        if obj.borrower:
            if obj.borrower.is_company:
                return obj.borrower.company_name
            return f"{obj.borrower.first_name} {obj.borrower.last_name}"
        return None
    
    def get_borrower_address(self, obj) -> dict:
        if obj.borrower and hasattr(obj.borrower, 'address'):
            address = obj.borrower.address
            return {
                'street': address.street,
                'city': address.city,
                'state': address.state,
                'postal_code': address.postal_code,
                'country': address.country
            }
        return None


class NoteCommentSerializer(serializers.ModelSerializer):
    """
    Serializer for note comments with null/blank handling for minimal data creation
    """
    created_by_name = serializers.StringRelatedField(source='created_by')
    
    class Meta:
        model = NoteComment
        fields = ['id', 'note', 'content', 'created_by', 'created_by_name', 'created_at', 'updated_at']
        read_only_fields = ['created_by', 'created_at', 'updated_at']
        extra_kwargs = {
            # Make most fields optional and allow null/blank values for minimal data creation
            'content': {'required': False, 'allow_null': True, 'allow_blank': True},
            'note': {'required': False, 'allow_null': True},
        }


class NoteSerializer(serializers.ModelSerializer):
    """
    Serializer for notes with null/blank handling for minimal data creation
    """
    created_by_name = serializers.StringRelatedField(source='created_by')
    assigned_to_name = serializers.StringRelatedField(source='assigned_to')
    comments = NoteCommentSerializer(many=True, read_only=True)
    
    class Meta:
        model = Note
        fields = '__all__'
        read_only_fields = ['created_by', 'created_at', 'updated_at']
        extra_kwargs = {
            # Make most fields optional and allow null/blank values for minimal data creation
            'title': {'required': False, 'allow_null': True, 'allow_blank': True},
            'content': {'required': False, 'allow_null': True, 'allow_blank': True},
            'priority': {'required': False, 'allow_null': True, 'allow_blank': True},
            'category': {'required': False, 'allow_null': True, 'allow_blank': True},
            'application': {'required': False, 'allow_null': True},
            'borrower': {'required': False, 'allow_null': True},
            'guarantor': {'required': False, 'allow_null': True},
            'assigned_to': {'required': False, 'allow_null': True},
            'due_date': {'required': False, 'allow_null': True},
            'is_completed': {'required': False, 'allow_null': True},
            'completed_date': {'required': False, 'allow_null': True},
        }


class FeeSerializer(serializers.ModelSerializer):
    """
    Serializer for fees with null/blank handling for minimal data creation
    """
    fee_type_display = serializers.CharField(source='get_fee_type_display', read_only=True)
    created_by_name = serializers.StringRelatedField(source='created_by')
    status = serializers.SerializerMethodField()
    invoice_url = serializers.SerializerMethodField()
    
    class Meta:
        model = Fee
        fields = '__all__'
        read_only_fields = ['created_by', 'created_at', 'updated_at']
        extra_kwargs = {
            # Make most fields optional and allow null/blank values for minimal data creation
            'fee_type': {'required': False, 'allow_null': True, 'allow_blank': True},
            'amount': {'required': False, 'allow_null': True},
            'description': {'required': False, 'allow_null': True, 'allow_blank': True},
            'due_date': {'required': False, 'allow_null': True},
            'paid_date': {'required': False, 'allow_null': True},
            'paid_amount': {'required': False, 'allow_null': True},
            'invoice': {'required': False, 'allow_null': True},
            'application': {'required': False, 'allow_null': True},
            'borrower': {'required': False, 'allow_null': True},
            'notes': {'required': False, 'allow_null': True, 'allow_blank': True},
        }
    
    def get_status(self, obj) -> str:
        if obj.paid_date:
            return 'paid'
        return 'pending'
    
    def get_invoice_url(self, obj) -> str:
        if obj.invoice:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.invoice.url)
        return None


class RepaymentSerializer(serializers.ModelSerializer):
    """
    Serializer for repayments with null/blank handling for minimal data creation
    """
    created_by_name = serializers.StringRelatedField(source='created_by')
    status = serializers.SerializerMethodField()
    invoice_url = serializers.SerializerMethodField()
    
    class Meta:
        model = Repayment
        fields = '__all__'
        read_only_fields = ['created_by', 'created_at', 'updated_at', 'reminder_sent', 'overdue_3_day_sent', 'overdue_7_day_sent', 'overdue_10_day_sent']
        extra_kwargs = {
            # Make most fields optional and allow null/blank values for minimal data creation
            'amount': {'required': False, 'allow_null': True},
            'due_date': {'required': False, 'allow_null': True},
            'paid_date': {'required': False, 'allow_null': True},
            'paid_amount': {'required': False, 'allow_null': True},
            'description': {'required': False, 'allow_null': True, 'allow_blank': True},
            'payment_method': {'required': False, 'allow_null': True, 'allow_blank': True},
            'invoice': {'required': False, 'allow_null': True},
            'application': {'required': False, 'allow_null': True},
            'notes': {'required': False, 'allow_null': True, 'allow_blank': True},
        }
    
    def get_status(self, obj) -> str:
        if obj.paid_date:
            return 'paid'
        
        from datetime import date
        today = date.today()
        
        if obj.due_date and obj.due_date < today:
            days_overdue = (today - obj.due_date).days
            return f'overdue_{days_overdue}_days'
        
        if obj.due_date:
            days_until_due = (obj.due_date - today).days
            if days_until_due <= 7:
                return f'due_soon_{days_until_due}_days'
        
        return 'scheduled'
    
    def get_invoice_url(self, obj) -> str:
        if obj.invoice:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.invoice.url)
        return None


class LedgerSerializer(serializers.ModelSerializer):
    """
    Serializer for ledger entries with null/blank handling for minimal data creation
    """
    transaction_type_display = serializers.CharField(source='get_transaction_type_display', read_only=True)
    related_fee_type = serializers.CharField(source='related_fee.get_fee_type_display', read_only=True)
    created_by_name = serializers.StringRelatedField(source='created_by')
    
    class Meta:
        model = Ledger
        fields = [
            'id', 'application', 'transaction_type', 'transaction_type_display',
            'amount', 'description', 'transaction_date', 'related_fee',
            'related_fee_type', 'related_repayment', 'created_by', 'created_by_name', 'created_at'
        ]
        extra_kwargs = {
            # Make most fields optional and allow null/blank values for minimal data creation
            'transaction_type': {'required': False, 'allow_null': True, 'allow_blank': True},
            'amount': {'required': False, 'allow_null': True},
            'description': {'required': False, 'allow_null': True, 'allow_blank': True},
            'transaction_date': {'required': False, 'allow_null': True},
            'application': {'required': False, 'allow_null': True},
            'related_fee': {'required': False, 'allow_null': True},
            'related_repayment': {'required': False, 'allow_null': True},
        }


class ApplicationLedgerSerializer(serializers.Serializer):
    """
    Serializer for application ledger summary
    """
    ledger_entries = LedgerSerializer(many=True)
    total_funded = serializers.DecimalField(max_digits=15, decimal_places=2)
    total_repaid = serializers.DecimalField(max_digits=15, decimal_places=2)
    total_fees = serializers.DecimalField(max_digits=15, decimal_places=2)
    balance = serializers.DecimalField(max_digits=15, decimal_places=2)