<template>
    <div class="form">
        <div class="long_item">
            <h1>Loan Details</h1>
        </div>
        <div class="item">
            <p>Application Type <span class="required">*</span></p>
            <el-select v-model="detail.application_type" placeholder="Select application type">
                <el-option value="residential" label="Residential" />
                <el-option value="commercial" label="Commercial" />
                <el-option value="construction" label="Construction" />
                <el-option value="refinance" label="Refinance" />
                <el-option value="investment" label="Investment" />
                <el-option value="smsf" label="SMSF" />
            </el-select>
            <span class="hint">Select the type of loan application</span>
        </div>
        <div class="item">
            <p>Estimated Settlement Date <span class="required">*</span></p>
            <el-date-picker 
                v-model="detail.estimated_settlement_date" 
                type="date" 
                placeholder="YYYY-MM-DD" 
                format="YYYY-MM-DD"
                value-format="YYYY-MM-DD" />
            <span class="hint">Date must be in YYYY-MM-DD format</span>
        </div>
        <div class="item">
            <p>Net Loan Required ($) <span class="required">*</span></p>
            <el-input v-model="detail.loan_amount" type="number" placeholder="e.g. 500000" />
            <span class="hint">Enter the loan amount (max 10 digits before decimal)</span>
        </div>
        <div class="item">
            <p>Term Required (months)</p>
            <el-input v-model="detail.loan_term" type="number" placeholder="e.g. 12" />
            <span class="hint">Enter the loan term in months</span>
        </div>
        <div class="item">
            <p>Expected Repayment Frequency <span class="required">*</span></p>
            <el-select v-model="detail.repayment_frequency" placeholder="Select frequency">
                <el-option value="weekly" label="Weekly" />
                <el-option value="fortnightly" label="Fortnightly" />
                <el-option value="monthly" label="Monthly" />
                <el-option value="quarterly" label="Quarterly" />
                <el-option value="annually" label="Annually" />
            </el-select>
            <span class="hint">How often repayments will be made</span>
        </div>
        <div class="item">
            <p>Reference Number <span class="required">*</span></p>
            <el-input v-model="detail.reference_number" placeholder="e.g. REF12345" />
            <span class="hint">Unique reference for this application (max 20 characters)</span>
        </div>
        <div class="item">
            <p>Product ID <span class="required">*</span></p>
            <el-input v-model="detail.product_id" placeholder="e.g. PROD-123" />
            <span class="hint">Product identifier (max 50 characters)</span>
        </div>
        <div class="item">
            <p>Expected Interest Rate (p.a) (%)</p>
            <el-input v-model="detail.interest_rate" type="number" step="0.01" placeholder="e.g. 5.5" />
            <span class="hint">Enter rate as percentage (max 3 digits before decimal)</span>
        </div>
        <div class="prior">
            <el-checkbox v-model="detail.prior_application">Prior Application</el-checkbox>
            <el-input v-model="detail.prior_application_details" placeholder="Details of prior application" :disabled="!detail.prior_application"/>
            <span class="hint">Check if this is related to a previous application</span>
        </div>
        <div class="long_item">
            <h1>Valuer</h1>
        </div>
        <div class="item">
            <p>Company Name</p>
            <el-input v-model="detail.valuer_company_name" placeholder="Valuation company name" />
            <span class="hint">Name of the valuation company</span>
        </div>
        <div class="item">
            <p>Contact Name</p>
            <el-input v-model="detail.valuer_contact_name" placeholder="Contact person name" />
            <span class="hint">Name of the contact person at the valuation company</span>
        </div>
        <div class="item">
            <p>Phone Number</p>
            <el-input v-model="detail.valuer_phone" placeholder="e.g. +61 2 1234 5678" />
            <span class="hint">Contact phone number (max 20 characters)</span>
        </div>
        <div class="item">
            <p>Email Address</p>
            <el-input v-model="detail.valuer_email" type="email" placeholder="example@domain.com" />
            <span class="hint">Must be a valid email address</span>
        </div>
        <div class="long_item">
            <h1>QS</h1>
        </div>
        <div class="item">
            <p>Company Name</p>
            <el-input v-model="detail.qs_company_name" placeholder="QS company name" />
            <span class="hint">Name of the quantity surveyor company</span>
        </div>
        <div class="item">
            <p>Contact Name</p>
            <el-input v-model="detail.qs_contact_name" placeholder="Contact person name" />
            <span class="hint">Name of the contact person at the QS company</span>
        </div>
        <div class="item">
            <p>Phone Number</p>
            <el-input v-model="detail.qs_phone" placeholder="e.g. +61 2 1234 5678" />
            <span class="hint">Contact phone number (max 20 characters)</span>
        </div>
        <div class="item">
            <p>Email Address</p>
            <el-input v-model="detail.qs_email" type="email" placeholder="example@domain.com" />
            <span class="hint">Must be a valid email address</span>
        </div>
        <div class="long_item">
            <h1>Loan Purpose</h1>
        </div>
        <div class="item">
            <p>Purpose <span class="required">*</span></p>
            <el-select v-model="detail.loan_purpose" placeholder="Select loan purpose">
                <el-option value="purchase" label="Purchase" />
                <el-option value="refinance" label="Refinance" />
                <el-option value="construction" label="Construction" />
                <el-option value="equity_release" label="Equity Release" />
                <el-option value="debt_consolidation" label="Debt Consolidation" />
                <el-option value="business_expansion" label="Business Expansion" />
                <el-option value="working_capital" label="Working Capital" />
                <el-option value="other" label="Other" />
            </el-select>
            <span class="hint">Primary purpose of the loan</span>
        </div>
        <div class="item" v-if="detail.loan_purpose === 'other'">
            <p>Other Purpose <span class="required">*</span></p>
            <el-input v-model="otherPurpose" placeholder="Specify other purpose" @input="updateOtherPurpose" />
            <span class="hint">Required if 'Other' is selected</span>
        </div>
        <div class="long_item">
            <h1>Additional Comments</h1>
        </div>
        <div class="long_item">
            <p>Please provide any additional relevant information / comments regarding this application</p>
            <el-input v-model="detail.additional_comments" type="textarea" :rows="3" placeholder="Enter any additional information here" />
            <span class="hint">Optional additional information about the application</span>
        </div>
    </div>
</template>

<script setup>
    import { ref, watch, onMounted } from 'vue';

    const props = defineProps({
        detail: Object
    });

    // Create local ref for other purpose
    const otherPurpose = ref("");

    // Initialize values from props
    onMounted(() => {
        // Check if loan_purpose is already set and is a valid enum value
        const validPurposes = ["purchase", "refinance", "construction", "equity_release", 
                              "debt_consolidation", "business_expansion", "working_capital", "other"];
        
        if (props.detail.loan_purpose && validPurposes.includes(props.detail.loan_purpose)) {
            // If it's a valid enum value, keep it as is
        } else if (props.detail.loan_purpose) {
            // If it's set but not a valid enum, assume it's a custom value
            otherPurpose.value = props.detail.loan_purpose;
            props.detail.loan_purpose = "other";
        } else {
            // Set default loan purpose if not set
            props.detail.loan_purpose = "refinance";
        }
        
        // Set default repayment frequency if not set
        if (!props.detail.repayment_frequency) {
            props.detail.repayment_frequency = "monthly";
        }
    });

    // Function to update the loan purpose when "other" is selected
    const updateOtherPurpose = () => {
        if (props.detail.loan_purpose === 'other' && otherPurpose.value) {
            // Store the custom value in the loan_purpose field
            props.detail.custom_loan_purpose = otherPurpose.value;
        }
    };

    // Watch for changes in the loan purpose
    watch(() => props.detail.loan_purpose, (newVal) => {
        if (newVal !== 'other') {
            // Reset the other purpose input when a predefined purpose is selected
            otherPurpose.value = "";
        }
    });
</script>

<style scoped>
    .form {
        display: grid;
        grid-template-columns: repeat(2, 1fr);
        gap: 15px 20px;
    }
    .item {
        display: flex;
        flex-direction: column;
        align-items: start;
        gap: 10px;
    }
    p {
        color: #384144;
        font-feature-settings: 'liga' off, 'clig' off;
        font-size: 0.75rem;
        font-style: normal;
        font-weight: 500;
        line-height: 12px;
        margin: 0;
    }
    .long_item {
        grid-column: 1 / 3;
        display: flex;
        flex-direction: column;
        align-items: start;
        gap: 10px;
    }
    .group {
        grid-column: 1 / 3;
        display: flex;
        flex-direction: column;
        gap: 10px;
    }
    .line {
        width: 100%;
        display: flex;
        flex-direction: row;
        justify-content: space-between;
        align-items: center;
    }
    .prior {
        grid-column: 1 / 3;
        display: flex;
        flex-direction: column;
        align-items: start;
        gap: 10px;
    }
    h1 {
        color: #384144;
        font-feature-settings: 'liga' off, 'clig' off;
        font-size: 0.9rem;
        font-style: normal;
        font-weight: 500;
        line-height: 12px;
    }
    :deep(.el-date-editor) {
        --el-date-editor-width: 100%;
    }
    :deep(.el-select) {
        width: 100%;
    }
    .hint {
        color: #8c8c8c;
        font-size: 0.7rem;
        font-style: italic;
    }
    .required {
        color: #f56c6c;
        margin-left: 2px;
    }
</style>
