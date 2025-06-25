<template>
    <div class="content">
        <!-- Company Borrower Details -->
        <div v-if="hasCompanyData" class="section">
            <div class="section-header">
                <h2>Company Borrower Details</h2>
            </div>
            <div v-for="(company, index) in detail.company_borrowers" :key="index" class="company-card">
                <div class="card-header">
                    <h3>Company {{ index + 1 }}: {{ company.company_name || 'Unnamed Company' }}</h3>
                </div>
                
                <div class="card-content">
                    <div class="info-grid">
                        <div class="info-group">
                            <h4>Company Information</h4>
                            <div class="info-row">
                                <span class="label">Company Name:</span>
                                <span class="value">{{ company.company_name || '-' }}</span>
                            </div>
                            <div class="info-row">
                                <span class="label">ABN:</span>
                                <span class="value">{{ company.company_abn || '-' }}</span>
                            </div>
                            <div class="info-row">
                                <span class="label">ACN:</span>
                                <span class="value">{{ company.company_acn || '-' }}</span>
                            </div>
                            <div class="info-row">
                                <span class="label">Industry Type:</span>
                                <span class="value">{{ company.industry_type || '-' }}</span>
                            </div>
                            <div class="info-row">
                                <span class="label">Contact Number:</span>
                                <span class="value">{{ company.contact_number || '-' }}</span>
                            </div>
                            <div class="info-row">
                                <span class="label">Annual Income:</span>
                                <span class="value">{{ formatCurrency(company.annual_company_income) }}</span>
                            </div>
                        </div>
                        
                        <div class="info-group">
                            <h4>Trustee Information</h4>
                            <div class="info-row">
                                <span class="label">Is Trustee:</span>
                                <span class="value">{{ status(company.is_trustee) }}</span>
                            </div>
                            <div class="info-row">
                                <span class="label">SMSF Trustee:</span>
                                <span class="value">{{ status(company.is_smsf_trustee) }}</span>
                            </div>
                            <div class="info-row">
                                <span class="label">Trustee Name:</span>
                                <span class="value">{{ company.trustee_name || '-' }}</span>
                            </div>
                        </div>
                        
                        <div class="info-group">
                            <h4>Registered Address</h4>
                            <div class="info-row">
                                <span class="label">Address:</span>
                                <span class="value">{{ formatCompanyAddress(company) || '-' }}</span>
                            </div>
                        </div>
                    </div>
                    
                    <!-- Directors Section -->
                    <div v-if="company.directors && company.directors.length > 0" class="directors-section">
                        <h4>Directors</h4>
                        <div class="directors-grid">
                            <div v-for="(director, dirIndex) in company.directors" :key="dirIndex" class="director-card">
                                <div class="director-header">
                                    <h5>Director {{ dirIndex + 1 }}</h5>
                                </div>
                                <div class="info-row">
                                    <span class="label">Name:</span>
                                    <span class="value">{{ director.name || '-' }}</span>
                                </div>
                                <div class="info-row">
                                    <span class="label">Position:</span>
                                    <span class="value">{{ director.roles || '-' }}</span>
                                </div>
                                <div class="info-row">
                                    <span class="label">Director ID:</span>
                                    <span class="value">{{ director.director_id || '-' }}</span>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- Fallback to legacy company data -->
        <div v-else-if="hasLegacyCompanyData" class="section">
            <div class="section-header">
                <h2>Company Borrower Details (Legacy)</h2>
            </div>
            <div class="company-card">
                <div class="card-content">
                    <div class="info-grid">
                        <div class="info-group">
                            <h4>Company Information</h4>
                            <div class="info-row">
                                <span class="label">Company Name:</span>
                                <span class="value">{{ detail.company_name || '-' }}</span>
                            </div>
                            <div class="info-row">
                                <span class="label">ABN:</span>
                                <span class="value">{{ detail.company_abn || '-' }}</span>
                            </div>
                            <div class="info-row">
                                <span class="label">ACN:</span>
                                <span class="value">{{ detail.company_acn || '-' }}</span>
                            </div>
                            <div class="info-row">
                                <span class="label">Industry Type:</span>
                                <span class="value">{{ detail.industry_type || '-' }}</span>
                            </div>
                            <div class="info-row">
                                <span class="label">Contact Number:</span>
                                <span class="value">{{ detail.contact_number || '-' }}</span>
                            </div>
                            <div class="info-row">
                                <span class="label">Annual Income:</span>
                                <span class="value">{{ formatCurrency(detail.annual_company_income) }}</span>
                            </div>
                        </div>
                        
                        <div class="info-group">
                            <h4>Trustee Information</h4>
                            <div class="info-row">
                                <span class="label">Is Trustee:</span>
                                <span class="value">{{ status(detail.is_trustee) }}</span>
                            </div>
                            <div class="info-row">
                                <span class="label">SMSF Trustee:</span>
                                <span class="value">{{ status(detail.is_smsf_trustee) }}</span>
                            </div>
                            <div class="info-row">
                                <span class="label">Trustee Name:</span>
                                <span class="value">{{ detail.trustee_name || '-' }}</span>
                            </div>
                        </div>
                        
                        <div class="info-group">
                            <h4>Registered Address</h4>
                            <div class="info-row">
                                <span class="label">Address:</span>
                                <span class="value">{{ formatAddress(detail) || '-' }}</span>
                            </div>
                        </div>
                    </div>
                    
                    <!-- Directors Section -->
                    <div class="directors-section">
                        <h4>Directors</h4>
                        <div class="directors-grid">
                            <div class="director-card">
                                <div class="director-header">
                                    <h5>Director 1</h5>
                                </div>
                                <div class="info-row">
                                    <span class="label">Name:</span>
                                    <span class="value">{{ detail.name1 || '-' }}</span>
                                </div>
                                <div class="info-row">
                                    <span class="label">Position:</span>
                                    <span class="value">{{ detail.position1 || '-' }}</span>
                                </div>
                                <div class="info-row">
                                    <span class="label">Director ID:</span>
                                    <span class="value">{{ detail.id1 || '-' }}</span>
                                </div>
                            </div>
                            <div class="director-card">
                                <div class="director-header">
                                    <h5>Director 2</h5>
                                </div>
                                <div class="info-row">
                                    <span class="label">Name:</span>
                                    <span class="value">{{ detail.name2 || '-' }}</span>
                                </div>
                                <div class="info-row">
                                    <span class="label">Position:</span>
                                    <span class="value">{{ detail.position2 || '-' }}</span>
                                </div>
                                <div class="info-row">
                                    <span class="label">Director ID:</span>
                                    <span class="value">{{ detail.id2 || '-' }}</span>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- Individual Borrowers -->
        <div v-if="detail.borrowers && detail.borrowers.length > 0" class="section">
            <div class="section-header">
                <h2>Individual Borrower Details</h2>
            </div>
            <div v-for="(borrower, index) in detail.borrowers" :key="index" class="borrower-card">
                <div class="card-header">
                    <h3>Borrower {{ index + 1 }}: {{ borrower.first_name }} {{ borrower.last_name }}</h3>
                </div>
                
                <div class="card-content">
                    <div class="info-grid">
                        <div class="info-group">
                            <h4>Personal Information</h4>
                            <div class="info-row">
                                <span class="label">First Name:</span>
                                <span class="value">{{ borrower.first_name || '-' }}</span>
                            </div>
                            <div class="info-row">
                                <span class="label">Last Name:</span>
                                <span class="value">{{ borrower.last_name || '-' }}</span>
                            </div>
                            <div class="info-row">
                                <span class="label">Email:</span>
                                <span class="value">{{ borrower.email || '-' }}</span>
                            </div>
                            <div class="info-row">
                                <span class="label">Home Phone:</span>
                                <span class="value">{{ borrower.home_phone || '-' }}</span>
                            </div>
                            <div class="info-row">
                                <span class="label">Mobile Phone:</span>
                                <span class="value">{{ borrower.mobile || '-' }}</span>
                            </div>
                            <div class="info-row">
                                <span class="label">Date of Birth:</span>
                                <span class="value">{{ borrower.date_of_birth || '-' }}</span>
                            </div>
                        </div>
                        
                        <div class="info-group">
                            <h4>Employment Information</h4>
                            <div class="info-row">
                                <span class="label">Occupation:</span>
                                <span class="value">{{ borrower.occupation || '-' }}</span>
                            </div>
                            <div class="info-row">
                                <span class="label">Employer Name:</span>
                                <span class="value">{{ borrower.employer_name || '-' }}</span>
                            </div>
                            <div class="info-row">
                                <span class="label">Employment Type:</span>
                                <span class="value">{{ borrower.employment_type || '-' }}</span>
                            </div>
                            <div class="info-row">
                                <span class="label">Annual Income:</span>
                                <span class="value">{{ formatCurrency(borrower.annual_income) }}</span>
                            </div>
                        </div>
                        
                        <div class="info-group">
                            <h4>Address Information</h4>
                            <div class="info-row">
                                <span class="label">Unit Number:</span>
                                <span class="value">{{ borrower.address_unit || '-' }}</span>
                            </div>
                            <div class="info-row">
                                <span class="label">Street Number:</span>
                                <span class="value">{{ borrower.address_street_no || '-' }}</span>
                            </div>
                            <div class="info-row">
                                <span class="label">Street Name:</span>
                                <span class="value">{{ borrower.address_street_name || '-' }}</span>
                            </div>
                            <div class="info-row">
                                <span class="label">Suburb:</span>
                                <span class="value">{{ borrower.address_suburb || '-' }}</span>
                            </div>
                            <div class="info-row">
                                <span class="label">State:</span>
                                <span class="value">{{ borrower.address_state || '-' }}</span>
                            </div>
                            <div class="info-row">
                                <span class="label">Postcode:</span>
                                <span class="value">{{ borrower.address_postcode || '-' }}</span>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- No Data Message -->
        <div v-if="!hasCompanyData && !hasLegacyCompanyData && (!detail.borrowers || detail.borrowers.length === 0)" class="no-data">
            <div class="no-data-content">
                <p>No borrower details available</p>
            </div>
        </div>
    </div>
</template>

<script setup>
    import { computed } from 'vue'

    const { detail } = defineProps({
        detail: {
            type: Object,
            required: true,
            default: () => ({})
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
        min-height: 250px;      
    }

    .section {
        margin-bottom: 30px;
    }

    .section-header {
        margin-bottom: 20px;
    }

    .section-header h2 {
        margin: 0;
        color: #384144;
        font-feature-settings: 'liga' off, 'clig' off;
        font-size: 0.9rem;
        font-style: normal;
        font-weight: 500;
        line-height: 12px;
    }

    .company-card, .borrower-card {
        margin-bottom: 20px;
    }

    .card-header {
        margin-bottom: 15px;
    }

    .card-header h3 {
        margin: 0;
        color: #384144;
        font-feature-settings: 'liga' off, 'clig' off;
        font-size: 0.9rem;
        font-style: normal;
        font-weight: 500;
        line-height: 12px;
    }

    .card-content {
        margin-bottom: 20px;
    }

    .info-grid {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 20px;
        margin-bottom: 20px;
    }

    .info-group {
        display: flex;
        flex-direction: column;
        gap: 10px;
    }

    .info-group h4 {
        margin: 0;
        color: #384144;
        font-feature-settings: 'liga' off, 'clig' off;
        font-size: 0.9rem;
        font-style: normal;
        font-weight: 500;
        line-height: 12px;
    }

    .info-row {
        display: flex;
        flex-direction: column;
        gap: 10px;
    }

    .label {
        color: #7A858E;
        font-feature-settings: 'liga' off, 'clig' off;
        font-size: 0.75rem;
        font-style: normal;
        font-weight: 500;
        line-height: 12px;
        margin: 0;
    }

    .value {
        color: #384144;
        font-feature-settings: 'liga' off, 'clig' off;
        font-size: 0.75rem;
        font-style: normal;
        font-weight: 600;
        line-height: 140%;
        margin: 0;
    }

    .directors-section {
        margin-top: 20px;
    }

    .directors-section h4 {
        margin: 0 0 15px 0;
        color: #384144;
        font-feature-settings: 'liga' off, 'clig' off;
        font-size: 0.9rem;
        font-style: normal;
        font-weight: 500;
        line-height: 12px;
    }

    .directors-grid {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 20px;
    }

    .director-card {
        display: flex;
        flex-direction: column;
        gap: 10px;
    }

    .director-header {
        margin-bottom: 10px;
    }

    .director-header h5 {
        margin: 0;
        color: #384144;
        font-feature-settings: 'liga' off, 'clig' off;
        font-size: 0.9rem;
        font-style: normal;
        font-weight: 500;
        line-height: 12px;
    }

    .director-card .info-row {
        display: flex;
        flex-direction: column;
        gap: 10px;
    }

    .director-card .label {
        color: #7A858E;
        font-feature-settings: 'liga' off, 'clig' off;
        font-size: 0.75rem;
        font-style: normal;
        font-weight: 500;
        line-height: 12px;
        margin: 0;
    }

    .director-card .value {
        color: #384144;
        font-feature-settings: 'liga' off, 'clig' off;
        font-size: 0.75rem;
        font-style: normal;
        font-weight: 600;
        line-height: 140%;
        margin: 0;
    }

    .no-data {
        text-align: center;
        padding: 40px;
        color: #666;
        font-style: italic;
    }

    .no-data-content p {
        margin: 0;
        color: #384144;
        font-feature-settings: 'liga' off, 'clig' off;
        font-size: 0.75rem;
        font-style: normal;
        font-weight: 600;
        line-height: 140%;
    }

    /* Responsive adjustments */
    @media (max-width: 768px) {
        .info-grid {
            grid-template-columns: 1fr;
            gap: 20px;
        }
        
        .directors-grid {
            grid-template-columns: 1fr;
        }
    }
</style>