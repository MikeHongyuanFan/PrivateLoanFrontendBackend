<template>
    <div class="form">
        <div class="long_item">
            <h1>Funding Calculation Inputs <span class="required">*</span></h1>
            <span class="hint">Parameters used to calculate funding details</span>
        </div>
        <div class="item">
            <p>Establishment Fee Rate (%) <span class="required">*</span></p>
            <el-input v-model="detail.establishment_fee_rate" type="number" step="0.01" placeholder="e.g. 2.5" />
            <span class="hint">Percentage rate for establishment fee (max 3 digits before decimal)</span>
        </div>
        <div class="item">
            <p>Capped Interest Months <span class="required">*</span></p>
            <el-input-number v-model="cappedInterestMonths" :min="1" :max="36" placeholder="e.g. 9" />
            <span class="hint">Number of months for capped interest (min: 1)</span>
        </div>
        <div class="item">
            <p>Monthly Line Fee Rate (%) <span class="required">*</span></p>
            <el-input v-model="detail.monthly_line_fee_rate" type="number" step="0.01" placeholder="e.g. 0.25" />
            <span class="hint">Monthly line fee as percentage (max 3 digits before decimal)</span>
        </div>
        <div class="item">
            <p>Brokerage Fee Rate (%) <span class="required">*</span></p>
            <el-input v-model="detail.brokerage_fee_rate" type="number" step="0.01" placeholder="e.g. 1.0" />
            <span class="hint">Brokerage fee as percentage (max 3 digits before decimal)</span>
        </div>
        <div class="item">
            <p>Application Fee ($) <span class="required">*</span></p>
            <el-input v-model="detail.application_fee" type="number" placeholder="e.g. 500" />
            <span class="hint">Fixed application fee amount (max 8 digits)</span>
        </div>
        <div class="item">
            <p>Due Diligence Fee ($) <span class="required">*</span></p>
            <el-input v-model="detail.due_diligence_fee" type="number" placeholder="e.g. 1000" />
            <span class="hint">Due diligence fee amount (max 8 digits)</span>
        </div>
        <div class="item">
            <p>Legal Fee Before GST ($) <span class="required">*</span></p>
            <el-input v-model="detail.legal_fee_before_gst" type="number" placeholder="e.g. 2000" />
            <span class="hint">Legal fee amount before GST (max 8 digits)</span>
        </div>
        <div class="item">
            <p>Valuation Fee ($) <span class="required">*</span></p>
            <el-input v-model="detail.valuation_fee" type="number" placeholder="e.g. 800" />
            <span class="hint">Property valuation fee amount (max 8 digits)</span>
        </div>
        <div class="item">
            <p>Monthly Account Fee ($) <span class="required">*</span></p>
            <el-input v-model="detail.monthly_account_fee" type="number" placeholder="e.g. 50" />
            <span class="hint">Monthly account maintenance fee (max 8 digits)</span>
        </div>
        <div class="item">
            <p>Working Fee ($)</p>
            <el-input v-model="detail.working_fee" type="number" placeholder="e.g. 0" />
            <span class="hint">Additional working fee if applicable (max 8 digits)</span>
        </div>
    </div>
</template>

<script setup>
    import { ref, computed, onMounted, watch } from 'vue';

    const props = defineProps({
        detail: Object
    });

    // Create computed property for capped interest months to handle type conversion
    const cappedInterestMonths = computed({
        get: () => Number(props.detail.capped_interest_months) || 9,
        set: (val) => { props.detail.capped_interest_months = val }
    });

    // Initialize values
    onMounted(() => {
        // Set default values if not provided
        if (!props.detail.capped_interest_months) {
            props.detail.capped_interest_months = 9;
        }
        if (!props.detail.working_fee) {
            props.detail.working_fee = "0.00";
        }
        
        // Ensure numeric fields are properly formatted
        props.detail.establishment_fee_rate = Number(props.detail.establishment_fee_rate) || 0;
        props.detail.monthly_line_fee_rate = Number(props.detail.monthly_line_fee_rate) || 0;
        props.detail.brokerage_fee_rate = Number(props.detail.brokerage_fee_rate) || 0;
        props.detail.application_fee = Number(props.detail.application_fee) || 0;
        props.detail.due_diligence_fee = Number(props.detail.due_diligence_fee) || 0;
        props.detail.legal_fee_before_gst = Number(props.detail.legal_fee_before_gst) || 0;
        props.detail.valuation_fee = Number(props.detail.valuation_fee) || 0;
        props.detail.monthly_account_fee = Number(props.detail.monthly_account_fee) || 0;
        props.detail.working_fee = Number(props.detail.working_fee) || 0;
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
    .long_item {
        grid-column: 1 / 3;
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
    h1 {
        color: #384144;
        font-feature-settings: 'liga' off, 'clig' off;
        font-size: 0.9rem;
        font-style: normal;
        font-weight: 500;
        line-height: 12px;
    }
    :deep(.el-input-number) {
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
