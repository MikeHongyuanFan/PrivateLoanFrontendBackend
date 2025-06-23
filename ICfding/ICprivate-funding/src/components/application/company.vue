<template>
    <div class="content">
        <!-- Enhanced Borrower Summary from Cascade Data -->
        <div v-if="summary && summary.length > 0" class="borrower_summary">
            <div class="summary_header">
                <h2>📊 Borrower Overview ({{ summary.length }} borrower{{ summary.length > 1 ? 's' : '' }})</h2>
            </div>
            <div class="borrower_cards">
                <div v-for="(borrower, index) in summary" :key="index" class="borrower_card">
                    <div class="borrower_info">
                        <h3>{{ borrower.is_company ? borrower.company_name : `${borrower.first_name} ${borrower.last_name}` }}</h3>
                        <p class="borrower_type">{{ borrower.is_company ? 'Company' : 'Individual' }}</p>
                        <p class="email">{{ borrower.email }}</p>
                    </div>
                    <div class="financial_summary">
                        <div class="financial_item">
                            <span class="label">Assets:</span>
                            <span class="value">${{ borrower.total_assets?.toLocaleString() || '0' }}</span>
                        </div>
                        <div class="financial_item">
                            <span class="label">Liabilities:</span>
                            <span class="value">${{ borrower.total_liabilities?.toLocaleString() || '0' }}</span>
                        </div>
                        <div class="financial_item">
                            <span class="label">Net Worth:</span>
                            <span class="value" :class="{ 'positive': borrower.net_worth >= 0, 'negative': borrower.net_worth < 0 }">
                                ${{ borrower.net_worth?.toLocaleString() || '0' }}
                            </span>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- Company Borrower Details (existing) -->
        <div v-if="hasCompanyData" class="company_section">
            <div class="part"><h1>Company Borrower Details</h1></div>
            <div v-for="(company, index) in detail.company_borrowers" :key="index" class="company_detail">
                <div class="company_header">
                    <h3>Company {{ index + 1 }}: {{ company.company_name || 'Unnamed Company' }}</h3>
                </div>
                <div class="form">
                    <div class="item">
                        <p class="title">Company Name</p>
                        <p>{{ company.company_name || '-' }}</p>
                    </div>
                    <div class="item">
                        <p class="title">ABN</p>
                        <p>{{ company.company_abn || '-' }}</p>
                    </div>
                    <div class="item">
                        <p class="title">ACN</p>
                        <p>{{ company.company_acn || '-' }}</p>
                    </div>
                    <div class="item">
                        <p class="title">Industry Type</p>
                        <p>{{ company.industry_type || '-' }}</p>
                    </div>
                    <div class="item">
                        <p class="title">Contact Number</p>
                        <p>{{ company.contact_number || '-' }}</p>
                    </div>
                    <div class="item">
                        <p class="title">Annual Company Income</p>
                        <p>{{ formatCurrency(company.annual_company_income) }}</p>
                    </div>
                    <div class="item">
                        <p class="title">Is the company a Trustee?</p>
                        <p>{{ status(company.is_trustee) }}</p>
                    </div>
                    <div class="item">
                        <p class="title">Is the company a Trustee for an SMSF?</p>
                        <p>{{ status(company.is_smsf_trustee) }}</p>
                    </div>
                    <div class="item">
                        <p class="title">Trustee Name</p>
                        <p>{{ company.trustee_name || '-' }}</p>
                    </div>
                </div>
                
                <!-- Directors for this company -->
                <div v-if="company.directors && company.directors.length > 0" class="part">
                    <h1>Directors</h1>
                </div>
                <div v-if="company.directors && company.directors.length > 0" class="form">
                    <div v-for="(director, dirIndex) in company.directors" :key="dirIndex" class="director_group">
                        <div class="item">
                            <p class="title">Name</p>
                            <p>{{ director.name || '-' }}</p>
                        </div>
                        <div class="item">
                            <p class="title">Position</p>
                            <p>{{ director.roles || '-' }}</p>
                        </div>
                        <div class="item">
                            <p class="title">Director ID</p>
                            <p>{{ director.director_id || '-' }}</p>
                        </div>
                    </div>
                </div>
                
                <!-- Registered Address for this company -->
                <div class="part"><h1>Registered Address</h1></div>
                <div class="item">
                    <p class="title">Full Address</p>
                    <p>{{ formatCompanyAddress(company) || '-' }}</p>
                </div>
            </div>
        </div>

        <!-- Fallback to legacy company data if no company_borrowers array -->
        <div v-else-if="hasLegacyCompanyData" class="company_section">
            <div class="part"><h1>Company Borrower Details (Legacy)</h1></div>
            <div class="form">
                <div class="item">
                    <p class="title">Company Name</p>
                    <p>{{ detail.company_name || '-' }}</p>
                </div>
                <div class="item">
                    <p class="title">ABN</p>
                    <p>{{ detail.company_abn || '-' }}</p>
                </div>
                <div class="item">
                    <p class="title">ACN</p>
                    <p>{{ detail.company_acn || '-' }}</p>
                </div>
                <div class="item">
                    <p class="title">Industry Type</p>
                    <p>{{ detail.industry_type || '-' }}</p>
                </div>
                <div class="item">
                    <p class="title">Contact Number</p>
                    <p>{{ detail.contact_number || '-' }}</p>
                </div>
                <div class="item">
                    <p class="title">Annual Company Income</p>
                    <p>{{ formatCurrency(detail.annual_company_income) }}</p>
                </div>
                <div class="item">
                    <p class="title">Is the company a Trustee?</p>
                    <p>{{ status(detail.is_trustee) }}</p>
                </div>
                <div class="item">
                    <p class="title">Is the company a Trustee for an SMSF?</p>
                    <p>{{ status(detail.is_smsf_trustee) }}</p>
                </div>
                <div class="item">
                    <p class="title">Trustee Name</p>
                    <p>{{ detail.trustee_name || '-' }}</p>
                </div>
            </div>
            <div class="part"><h1>Position Held</h1></div>
            <div class="form">
                <div class="item">
                    <p class="title">Name</p>
                    <p>{{ detail.name1 || '-' }}</p>
                </div>
                <div class="item">
                    <p class="title">Position</p>
                    <p>{{ detail.position1 || '-' }}</p>
                </div>
                <div class="item">
                    <p class="title">Director ID</p>
                    <p>{{ detail.id1 || '-' }}</p>
                </div>
                <div class="item">
                    <p class="title">Name</p>
                    <p>{{ detail.name2 || '-' }}</p>
                </div>
                <div class="item">
                    <p class="title">Position</p>
                    <p>{{ detail.position2 || '-' }}</p>
                </div>
                <div class="item">
                    <p class="title">Director ID</p>
                    <p>{{ detail.id2 || '-' }}</p>
                </div>
            </div>
            <div class="part"><h1>Registered Address</h1></div>
            <div class="item">
                <p class="title">Full Address</p>
                <p>{{ formatAddress(detail) || '-' }}</p>
            </div>
        </div>

        <!-- Individual Borrowers from Cascade Data -->
        <div v-if="detail.borrowers && detail.borrowers.length > 0" class="borrowers_section">
            <div class="part"><h1>Individual Borrower Details</h1></div>
            <div v-for="(borrower, index) in detail.borrowers" :key="index" class="borrower_detail">
                <div class="borrower_header">
                    <h3>Borrower {{ index + 1 }}: {{ borrower.first_name }} {{ borrower.last_name }}</h3>
                </div>
                <div class="form">
                    <div class="item">
                        <p class="title">First Name</p>
                        <p>{{ borrower.first_name || '-' }}</p>
                    </div>
                    <div class="item">
                        <p class="title">Last Name</p>
                        <p>{{ borrower.last_name || '-' }}</p>
                    </div>
                    <div class="item">
                        <p class="title">Email</p>
                        <p>{{ borrower.email || '-' }}</p>
                    </div>
                    <div class="item">
                        <p class="title">Phone</p>
                        <p>{{ borrower.phone || '-' }}</p>
                    </div>
                    <div class="item">
                        <p class="title">Date of Birth</p>
                        <p>{{ borrower.date_of_birth || '-' }}</p>
                    </div>
                    <div class="item">
                        <p class="title">Marital Status</p>
                        <p>{{ borrower.marital_status || '-' }}</p>
                    </div>
                    <div class="item">
                        <p class="title">Tax ID</p>
                        <p>{{ borrower.tax_id || '-' }}</p>
                    </div>
                    <div class="item">
                        <p class="title">Residency Status</p>
                        <p>{{ borrower.residency_status || '-' }}</p>
                    </div>
                    <div class="item">
                        <p class="title">Referral Source</p>
                        <p>{{ borrower.referral_source || '-' }}</p>
                    </div>
                </div>
                
                <!-- Employment Information -->
                <div v-if="borrower.employment_info" class="part">
                    <h4>Employment Information</h4>
                </div>
                <div v-if="borrower.employment_info" class="form">
                    <div class="item">
                        <p class="title">Employer</p>
                        <p>{{ borrower.employment_info.employer || '-' }}</p>
                    </div>
                    <div class="item">
                        <p class="title">Position</p>
                        <p>{{ borrower.employment_info.position || '-' }}</p>
                    </div>
                    <div class="item">
                        <p class="title">Annual Income</p>
                        <p>{{ formatCurrency(borrower.employment_info.income) }}</p>
                    </div>
                    <div class="item">
                        <p class="title">Years Employed</p>
                        <p>{{ borrower.employment_info.years_employed || '-' }}</p>
                    </div>
                </div>

                <!-- Address Information -->
                <div v-if="borrower.address || borrower.residential_address" class="part">
                    <h4>Address Information</h4>
                </div>
                <div v-if="borrower.address || borrower.residential_address" class="form">
                    <!-- Debug info (remove in production) -->
                    <div v-if="true" class="debug-info" style="grid-column: 1 / 4; background: #f0f0f0; padding: 10px; margin-bottom: 10px; font-size: 0.7rem;">
                        <p><strong>Debug:</strong> address: {{ JSON.stringify(borrower.address) }}</p>
                        <p><strong>Debug:</strong> residential_address: {{ borrower.residential_address }}</p>
                        <p><strong>Debug:</strong> hasStructuredAddress: {{ hasStructuredAddress(borrower.address) }}</p>
                    </div>
                    
                    <!-- Show structured address if available and has content -->
                    <div v-if="borrower.address && hasStructuredAddress(borrower.address)" class="structured_address">
                        <div class="item">
                            <p class="title">Street Address</p>
                            <p>{{ borrower.address.street || '-' }}</p>
                        </div>
                        <div class="item">
                            <p class="title">City</p>
                            <p>{{ borrower.address.city || '-' }}</p>
                        </div>
                        <div class="item">
                            <p class="title">State</p>
                            <p>{{ borrower.address.state || '-' }}</p>
                        </div>
                        <div class="item">
                            <p class="title">Postal Code</p>
                            <p>{{ borrower.address.postal_code || '-' }}</p>
                        </div>
                        <div class="item">
                            <p class="title">Country</p>
                            <p>{{ borrower.address.country || '-' }}</p>
                        </div>
                    </div>
                    
                    <!-- Fallback to raw address if structured address is empty or incomplete -->
                    <div v-else-if="borrower.residential_address" class="raw_address">
                        <div class="item">
                            <p class="title">Full Address</p>
                            <p>{{ borrower.residential_address || '-' }}</p>
                        </div>
                    </div>
                    
                    <!-- Show mailing address if different from residential -->
                    <div v-if="borrower.mailing_address && borrower.mailing_address !== borrower.residential_address" class="mailing_address">
                        <div class="item">
                            <p class="title">Mailing Address</p>
                            <p>{{ borrower.mailing_address || '-' }}</p>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- No Data Message -->
        <div v-if="!hasCompanyData && !hasLegacyCompanyData && (!detail.borrowers || detail.borrowers.length === 0)" class="no_data">
            <p>No borrower details available</p>
        </div>
    </div>
</template>

<script setup>
    import { computed } from 'vue'

    const { detail, summary } = defineProps({
        detail: {
            type: Object,
            required: true,
            default: () => ({})
        },
        summary: {
            type: Array,
            required: false,
            default: () => []
        }
    })

    const hasCompanyData = computed(() => {
        return detail.company_borrowers && detail.company_borrowers.length > 0
    })

    const hasLegacyCompanyData = computed(() => {
        return !hasCompanyData.value && (
            detail.company_name || detail.company_abn || detail.company_acn || 
            detail.industry_type || detail.contact_number || detail.annual_company_income
        )
    })

    const status = (st) => {
        if (st === true) {
            return "Yes"
        } else {
            return "No"
        }
    }

    const formatCurrency = (value) => {
        if (!value) return '-'
        return new Intl.NumberFormat('en-AU', {
            style: 'currency',
            currency: 'AUD'
        }).format(value)
    }

    const formatAddress = (detail) => {
        if (!detail) return '-'
        const parts = [
            detail.registered_address_unit,
            detail.registered_address_street_no,
            detail.registered_address_street_name,
            detail.registered_address_suburb
        ]
        return parts.filter(Boolean).join(' ')
    }

    const formatCompanyAddress = (company) => {
        if (!company) return '-'
        const parts = [
            company.registered_address_unit,
            company.registered_address_street_no,
            company.registered_address_street_name,
            company.registered_address_suburb
        ]
        return parts.filter(Boolean).join(' ')
    }

    const hasStructuredAddress = (address) => {
        // Check if address object exists and has any meaningful content
        if (!address) return false;
        
        // Check if any of the structured fields have content
        const hasContent = address.street || address.city || address.state || address.postal_code || address.country;
        
        // Also check if the address object has any non-empty string values
        const hasNonEmptyValues = Object.values(address).some(value => 
            value && typeof value === 'string' && value.trim() !== ''
        );
        
        return hasContent || hasNonEmptyValues;
    }
</script>

<style scoped>
    .content {
        padding: 20px;
        border-radius: 6px;
        background: #FFF;
        display: flex;
        flex-direction: column;
        gap: 20px;
    }
    
    /* Borrower Summary Styles */
    .borrower_summary {
        background: #F8F9FA;
        border: 1px solid #E8EBEE;
        border-radius: 8px;
        padding: 15px;
        margin-bottom: 20px;
    }
    .summary_header h2 {
        color: #384144;
        font-size: 1.1rem;
        font-weight: 600;
        margin: 0 0 15px 0;
    }
    .borrower_cards {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
        gap: 15px;
    }
    .borrower_card {
        background: #FFF;
        border: 1px solid #E8EBEE;
        border-radius: 6px;
        padding: 15px;
        display: flex;
        flex-direction: column;
        gap: 12px;
    }
    .borrower_info h3 {
        color: #384144;
        font-size: 0.9rem;
        font-weight: 600;
        margin: 0 0 5px 0;
    }
    .borrower_type {
        color: #2984DE;
        font-size: 0.7rem;
        font-weight: 600;
        margin: 0 0 3px 0;
    }
    .email {
        color: #666;
        font-size: 0.7rem;
        margin: 0;
    }
    .financial_summary {
        display: flex;
        flex-direction: column;
        gap: 8px;
    }
    .financial_item {
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    .financial_item .label {
        font-size: 0.7rem;
        color: #666;
        font-weight: 500;
    }
    .financial_item .value {
        font-size: 0.75rem;
        font-weight: 600;
        color: #384144;
    }
    .financial_item .value.positive {
        color: #14A105;
    }
    .financial_item .value.negative {
        color: #E74C3C;
    }
    
    /* Existing styles */
    .form {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 20px;
    }
    .item {
        display: flex;
        flex-direction: column;
        gap: 10px;
    }
    p {
        color: #384144;
        font-feature-settings: 'liga' off, 'clig' off;
        font-size: 0.75rem;
        font-style: normal;
        font-weight: 600;
        line-height: 140%;
        margin: 0;
    }
    .title {
        color: #7A858E;
    }
    .part {
        padding: 20px 0;
        border-top: 1.5px solid #E8EBEE;
    }
    .part:first-child {
        border-top: none;
        padding-top: 0;
    }
    h1 {
        color: #384144;
        font-feature-settings: 'liga' off, 'clig' off;
        font-size: 0.9rem;
        font-style: normal;
        font-weight: 600;
        line-height: normal;
        margin: 0;
    }
    h4 {
        color: #384144;
        font-size: 0.8rem;
        font-weight: 600;
        margin: 0;
    }
    
    /* Individual borrower styles */
    .borrowers_section {
        border-top: 1.5px solid #E8EBEE;
        padding-top: 20px;
    }
    .borrower_detail {
        margin-bottom: 30px;
        padding: 15px;
        background: #FAFAFA;
        border-radius: 6px;
        border: 1px solid #E8EBEE;
    }
    .borrower_header h3 {
        color: #2984DE;
        font-size: 0.9rem;
        font-weight: 600;
        margin: 0 0 15px 0;
    }
    
    /* No data message */
    .no_data {
        text-align: center;
        padding: 40px;
        color: #666;
        font-style: italic;
    }
    
    /* Responsive adjustments */
    @media (max-width: 768px) {
        .form {
            grid-template-columns: 1fr;
        }
        .borrower_cards {
            grid-template-columns: 1fr;
        }
    }
</style>