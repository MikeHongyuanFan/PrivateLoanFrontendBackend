<template>
    <div class="content">
        <div class="form">
            <div class="item">
                <p class="title">Net Loan Required ($)</p>
                <p>{{ detail.loan_amount || '-' }}</p>
            </div>
            <div class="item">
                <p class="title">Term Required (Month)</p>
                <p>{{ detail.loan_term || '-' }}</p>
            </div>
            <div class="item">
                <p class="title">Capitalised Interest Term (Months)</p>
                <p>{{ detail.capitalised_interest_term || '-' }}</p>
            </div>
            <div class="item">
                <p class="title">Proposed Settlement Date</p>
                <p>{{ detail.estimated_settlement_date || '-' }}</p>
            </div>
            <div class="item">
                <p class="title">Expected Rate (p.a) (%)</p>
                <p>{{ detail.interest_rate || '-' }}</p>
            </div>
            <div class="item">
                <p class="title">Application Type</p>
                <p>{{ formatApplicationType(detail.application_type, detail.application_type_other) }}</p>
            </div>
            <div class="item">
                <p class="title">Product ID</p>
                <p v-if="detail.product_name">{{ detail.product_name }} (ID: {{ detail.product_id }})</p>
                <p v-else-if="detail.product_id">Product ID: {{ detail.product_id }}</p>
                <p v-else>-</p>
            </div>
            <div class="item">
                <p class="title">Loan Purpose</p>
                <p>{{ detail.loan_purpose || '-' }}</p>
            </div>
            <div class="item">
                <p class="title">Additional Comments</p>
                <p>{{ detail.additional_comments || '-' }}</p>
            </div>
            <!-- Valuer Information -->
            <div class="item">
                <p class="title">Valuer</p>
                <div v-if="detail.valuer" class="entity-info">
                    <p class="entity-name">{{ detail.valuer.company_name }}</p>
                    <p class="entity-details">{{ detail.valuer.contact_name }} - {{ detail.valuer.phone }}</p>
                    <p class="entity-email">{{ detail.valuer.email }}</p>
                </div>
                <p v-else>Not assigned</p>
            </div>
            <!-- Quantity Surveyor Information -->
            <div class="item">
                <p class="title">Quantity Surveyor</p>
                <div v-if="detail.quantity_surveyor" class="entity-info">
                    <p class="entity-name">{{ detail.quantity_surveyor.company_name }}</p>
                    <p class="entity-details">{{ detail.quantity_surveyor.contact_name }} - {{ detail.quantity_surveyor.phone }}</p>
                    <p class="entity-email">{{ detail.quantity_surveyor.email }}</p>
                </div>
                <p v-else>Not assigned</p>
            </div>
            <!-- Prior Application Info -->
            <div class="item" v-if="detail.prior_application">
                <p class="title">Prior Application</p>
                <p>{{ detail.prior_application_details || 'Yes' }}</p>
            </div>
            <div class="item" v-if="detail.has_other_credit_providers">
                <p class="title">Has Application to Other Credit Providers?</p>
                <p>Yes</p>
            </div>
            <div class="item" v-if="detail.has_other_credit_providers">
                <p class="title">Other Credit Providers Details</p>
                <p>{{ detail.other_credit_providers_details || '-' }}</p>
            </div>
        </div>
    </div>
</template>

<script setup>
    import { ref } from 'vue';

    const { detail } = defineProps({
        detail: Object
    })

    const formatApplicationType = (applicationType, applicationTypeOther) => {
        if (!applicationType) return '-';
        
        // Map the values to display labels
        const typeLabels = {
            'acquisition': 'Acquisition',
            'refinance': 'Refinance',
            'equity_release': 'Equity Release',
            'refinance_equity_release': 'Refinance & Equity Release',
            'second_mortgage': '2nd Mortgage',
            'caveat': 'Caveat',
            'other': 'Other'
        };
        
        if (applicationType === 'other' && applicationTypeOther) {
            return `Other: ${applicationTypeOther}`;
        }
        
        return typeLabels[applicationType] || applicationType;
    };
</script>

<style scoped>
    .content {
        padding: 20px;
        border-radius: 6px;
        background: #FFF;  
        min-height: 250px;      
    }
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
    .entity-info {
        display: flex;
        flex-direction: column;
        gap: 2px;
    }
    .entity-name {
        font-weight: 700;
        color: #2984DE;
    }
    .entity-details {
        font-size: 0.7rem;
        color: #666;
        font-weight: 500;
    }
    .entity-email {
        font-size: 0.7rem;
        color: #666;
        font-weight: 500;
    }
</style>