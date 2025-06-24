from django.contrib import admin
from .models import Application, SecurityProperty, LoanRequirement, Document, Fee, Repayment, FundingCalculationHistory, Valuer, QuantitySurveyor, ActiveLoan, ActiveLoanRepayment


class SecurityPropertyInline(admin.TabularInline):
    model = SecurityProperty
    extra = 0


class LoanRequirementInline(admin.TabularInline):
    model = LoanRequirement
    extra = 0


class DocumentInline(admin.TabularInline):
    model = Document
    extra = 0


class FeeInline(admin.TabularInline):
    model = Fee
    extra = 0


class RepaymentInline(admin.TabularInline):
    model = Repayment
    extra = 0


class FundingCalculationHistoryInline(admin.TabularInline):
    model = FundingCalculationHistory
    extra = 0
    readonly_fields = ('created_at', 'created_by')


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('reference_number', 'stage', 'loan_amount', 'created_at', 'updated_at')
    list_filter = ('stage', 'application_type', 'loan_purpose')
    search_fields = ('reference_number', 'purpose', 'security_address')
    readonly_fields = ('reference_number', 'created_at', 'updated_at', 'stage_history')
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('reference_number', 'stage', 'stage_history', 'application_type', 'purpose')
        }),
        ('Loan Details', {
            'fields': ('loan_amount', 'loan_term', 'capitalised_interest_term', 'interest_rate', 'repayment_frequency', 
                      'product_id', 'estimated_settlement_date')
        }),
        ('Loan Purpose', {
            'fields': ('loan_purpose', 'additional_comments', 'prior_application', 'prior_application_details')
        }),
        ('Exit Strategy', {
            'fields': ('exit_strategy', 'exit_strategy_details')
        }),
        ('General Solvency Enquiries', {
            'fields': ('has_pending_litigation', 'has_unsatisfied_judgements', 'has_been_bankrupt',
                      'has_been_refused_credit', 'has_outstanding_ato_debt', 'has_outstanding_tax_returns',
                      'has_payment_arrangements', 'solvency_enquiries_details')
        }),
        ('Relationships', {
            'fields': ('broker', 'branch', 'bd', 'valuer', 'quantity_surveyor', 'borrowers', 'guarantors')
        }),
        ('Security Property (Legacy)', {
            'fields': ('security_address', 'security_type', 'security_value')
        }),
        ('Valuer Information', {
            'fields': ('valuer_company_name', 'valuer_contact_name', 'valuer_phone', 'valuer_email',
                      'valuation_date', 'valuation_amount')
        }),
        ('Quantity Surveyor Information', {
            'fields': ('qs_company_name', 'qs_contact_name', 'qs_phone', 'qs_email', 'qs_report_date')
        }),
        ('Signature and Document', {
            'fields': ('signed_by', 'signature_date', 'uploaded_pdf_path')
        }),
        ('Metadata', {
            'fields': ('created_by', 'created_at', 'updated_at')
        }),
    )
    
    inlines = [
        SecurityPropertyInline,
        LoanRequirementInline,
        DocumentInline,
        FeeInline,
        RepaymentInline,
        FundingCalculationHistoryInline,
    ]
    
    def save_model(self, request, obj, form, change):
        if not change:  # If creating a new object
            obj.created_by = request.user
        super().save_model(request, obj, form, change)


@admin.register(SecurityProperty)
class SecurityPropertyAdmin(admin.ModelAdmin):
    list_display = ('get_address', 'property_type', 'estimated_value', 'application')
    list_filter = ('property_type', 'occupancy')
    search_fields = ('address_street_name', 'address_suburb', 'address_postcode')
    
    def get_address(self, obj):
        address_parts = [
            obj.address_unit,
            obj.address_street_no,
            obj.address_street_name,
            obj.address_suburb,
            obj.address_state,
            obj.address_postcode
        ]
        return ' '.join(filter(None, address_parts))
    get_address.short_description = 'Address'


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ('document_type', 'description', 'application', 'uploaded_at', 'uploaded_by')
    list_filter = ('document_type', 'uploaded_at')
    search_fields = ('description',)
    date_hierarchy = 'uploaded_at'


@admin.register(Fee)
class FeeAdmin(admin.ModelAdmin):
    list_display = ('fee_type', 'amount', 'due_date', 'status', 'application')
    list_filter = ('fee_type', 'status', 'due_date')
    search_fields = ('notes',)
    date_hierarchy = 'due_date'


@admin.register(Repayment)
class RepaymentAdmin(admin.ModelAdmin):
    list_display = ('due_date', 'amount', 'status', 'paid_date', 'application')
    list_filter = ('status', 'due_date', 'paid_date')
    search_fields = ('notes',)
    date_hierarchy = 'due_date'


@admin.register(FundingCalculationHistory)
class FundingCalculationHistoryAdmin(admin.ModelAdmin):
    list_display = ('application', 'created_by', 'created_at')
    list_filter = ('created_at',)
    readonly_fields = ('created_at', 'created_by')
    date_hierarchy = 'created_at'


@admin.register(Valuer)
class ValuerAdmin(admin.ModelAdmin):
    list_display = ('company_name', 'contact_name', 'phone', 'email', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('company_name', 'contact_name', 'email', 'phone')
    readonly_fields = ('created_by', 'created_at', 'updated_at')
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('company_name', 'contact_name', 'phone', 'email')
        }),
        ('Additional Information', {
            'fields': ('address', 'notes', 'is_active')
        }),
        ('Metadata', {
            'fields': ('created_by', 'created_at', 'updated_at')
        }),
    )
    
    def save_model(self, request, obj, form, change):
        if not change:  # If creating a new object
            obj.created_by = request.user
        super().save_model(request, obj, form, change)


@admin.register(QuantitySurveyor)
class QuantitySurveyorAdmin(admin.ModelAdmin):
    list_display = ('company_name', 'contact_name', 'phone', 'email', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('company_name', 'contact_name', 'email', 'phone')
    readonly_fields = ('created_by', 'created_at', 'updated_at')
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('company_name', 'contact_name', 'phone', 'email')
        }),
        ('Additional Information', {
            'fields': ('address', 'notes', 'is_active')
        }),
        ('Metadata', {
            'fields': ('created_by', 'created_at', 'updated_at')
        }),
    )
    
    def save_model(self, request, obj, form, change):
        if not change:  # If creating a new object
            obj.created_by = request.user
        super().save_model(request, obj, form, change)


class ActiveLoanRepaymentInline(admin.TabularInline):
    model = ActiveLoanRepayment
    extra = 0
    readonly_fields = ('is_late', 'created_at')


@admin.register(ActiveLoan)
class ActiveLoanAdmin(admin.ModelAdmin):
    list_display = ('application', 'settlement_date', 'loan_expiry_date', 'interest_payments_required', 'is_active', 'days_until_expiry')
    list_filter = ('is_active', 'interest_payments_required', 'interest_payment_frequency', 'settlement_date', 'loan_expiry_date')
    search_fields = ('application__reference_number', 'application__borrowers__first_name', 'application__borrowers__last_name')
    readonly_fields = ('created_at', 'updated_at', 'days_until_expiry', 'days_until_next_payment', 'next_interest_payment_date')
    date_hierarchy = 'settlement_date'
    
    fieldsets = (
        ('Application Details', {
            'fields': ('application',)
        }),
        ('Loan Information', {
            'fields': ('settlement_date', 'capitalised_interest_months', 'loan_expiry_date', 'is_active')
        }),
        ('Interest Payment Details', {
            'fields': ('interest_payments_required', 'interest_payment_frequency', 'interest_payment_due_dates')
        }),
        ('Computed Fields', {
            'fields': ('days_until_expiry', 'days_until_next_payment', 'next_interest_payment_date')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at')
        }),
    )
    
    inlines = [ActiveLoanRepaymentInline]
    
    def days_until_expiry(self, obj):
        days = obj.days_until_expiry
        if days is None:
            return 'N/A'
        elif days < 0:
            return f'{abs(days)} days overdue'
        elif days == 0:
            return 'Due today'
        else:
            return f'{days} days remaining'
    days_until_expiry.short_description = 'Days Until Expiry'


@admin.register(ActiveLoanRepayment)
class ActiveLoanRepaymentAdmin(admin.ModelAdmin):
    list_display = ('active_loan', 'repayment_type', 'amount', 'payment_date', 'due_date', 'is_late', 'created_at')
    list_filter = ('repayment_type', 'is_late', 'payment_date', 'due_date')
    search_fields = ('active_loan__application__reference_number', 'reference_number', 'notes')
    readonly_fields = ('is_late', 'created_at', 'updated_at')
    date_hierarchy = 'payment_date'
    
    fieldsets = (
        ('Loan Information', {
            'fields': ('active_loan',)
        }),
        ('Repayment Details', {
            'fields': ('repayment_type', 'amount', 'payment_date', 'due_date', 'reference_number')
        }),
        ('Status', {
            'fields': ('is_late', 'notes')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at')
        }),
    )
