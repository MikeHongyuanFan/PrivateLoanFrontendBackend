<template>
    <div class="form">
        <div class="long_item">
            <h1>Funding Calculation Inputs <span class="required">*</span></h1>
            <span class="hint">Parameters used to calculate funding details</span>
        </div>
        
        <!-- NEW: Display calculated loan amount from loan requirements -->
        <div class="item loan-amount-display">
            <p>Total Loan Amount (from Requirements) <span class="required">*</span></p>
            <el-input v-model="calculatedLoanAmount" readonly placeholder="Calculated from loan requirements" />
            <span class="hint">This amount is automatically calculated from the sum of all loan requirements</span>
        </div>
        
        <!-- NEW: Warning message when no loan amount is available -->
        <div class="item warning-message" v-if="!hasLoanAmount">
            <div class="warning-content">
                <el-icon color="#E6A23C"><Warning /></el-icon>
                <span>Please complete the Loan Requirements step first to calculate the total loan amount.</span>
            </div>
        </div>
        
        <div class="item">
            <p>Establishment Fee Rate (%) <span class="required">*</span></p>
            <el-input v-model="localDetail.establishment_fee_rate" type="number" step="0.01" placeholder="e.g. 2.5" />
            <span class="hint">Percentage rate for establishment fee (max 3 digits before decimal)</span>
        </div>
        <div class="item">
            <p>Capped Interest Months <span class="required">*</span></p>
            <el-input-number v-model="cappedInterestMonths" :min="1" :max="36" placeholder="e.g. 9" />
            <span class="hint">Number of months for capped interest (min: 1)</span>
        </div>
        <div class="item">
            <p>Monthly Line Fee Rate (%) <span class="required">*</span></p>
            <el-input v-model="localDetail.monthly_line_fee_rate" type="number" step="0.01" placeholder="e.g. 0.25" />
            <span class="hint">Monthly line fee as percentage (max 3 digits before decimal)</span>
        </div>
        <div class="item">
            <p>Brokerage Fee Rate (%) <span class="required">*</span></p>
            <el-input v-model="localDetail.brokerage_fee_rate" type="number" step="0.01" placeholder="e.g. 1.0" />
            <span class="hint">Brokerage fee as percentage (max 3 digits before decimal)</span>
        </div>
        <div class="item">
            <p>Application Fee ($) <span class="required">*</span></p>
            <el-input v-model="localDetail.application_fee" type="number" placeholder="e.g. 500" />
            <span class="hint">Fixed application fee amount (max 8 digits)</span>
        </div>
        <div class="item">
            <p>Due Diligence Fee ($) <span class="required">*</span></p>
            <el-input v-model="localDetail.due_diligence_fee" type="number" placeholder="e.g. 1000" />
            <span class="hint">Due diligence fee amount (max 8 digits)</span>
        </div>
        <div class="item">
            <p>Legal Fee Before GST ($) <span class="required">*</span></p>
            <el-input v-model="localDetail.legal_fee_before_gst" type="number" placeholder="e.g. 2000" />
            <span class="hint">Legal fee amount before GST (max 8 digits)</span>
        </div>
        <div class="item">
            <p>Valuation Fee ($) <span class="required">*</span></p>
            <el-input v-model="localDetail.valuation_fee" type="number" placeholder="e.g. 800" />
            <span class="hint">Property valuation fee amount (max 8 digits)</span>
        </div>
        <div class="item">
            <p>Monthly Account Fee ($) <span class="required">*</span></p>
            <el-input v-model="localDetail.monthly_account_fee" type="number" placeholder="e.g. 50" />
            <span class="hint">Monthly account maintenance fee (max 8 digits)</span>
        </div>
        <div class="item">
            <p>Working Fee ($)</p>
            <el-input v-model="localDetail.working_fee" type="number" placeholder="e.g. 0" />
            <span class="hint">Additional working fee if applicable (max 8 digits)</span>
        </div>
    </div>
</template>

<script setup>
    import { ref, computed, onMounted, watch } from 'vue';
    import { Warning } from '@element-plus/icons-vue';

    const props = defineProps({
        detail: Object
    });

    const emit = defineEmits(['update:detail']);

    // Create reactive local variables that sync with props
    const localDetail = ref({
        establishment_fee_rate: 0,
        capped_interest_months: 9,
        monthly_line_fee_rate: 0,
        brokerage_fee_rate: 0,
        application_fee: 0,
        due_diligence_fee: 0,
        legal_fee_before_gst: 0,
        valuation_fee: 0,
        monthly_account_fee: 0,
        working_fee: 0,
        calculated_loan_amount: '0.00'
    });

    // NEW: Computed property to calculate total loan amount from requirements
    const calculatedLoanAmount = computed({
        get: () => {
            return localDetail.value.calculated_loan_amount || '0.00';
        },
        set: (val) => {
            localDetail.value.calculated_loan_amount = val;
        }
    });

    // NEW: Check if loan amount is available
    const hasLoanAmount = computed(() => {
        const amount = parseFloat(localDetail.value.calculated_loan_amount?.replace(/,/g, '') || '0');
        return amount > 0;
    });

    // Watch for changes in props and update local state
    watch(() => props.detail, (newDetail) => {
        if (newDetail) {
            console.log('Calculation component detail changed:', newDetail);
            // Sync props to local state
            Object.keys(localDetail.value).forEach(key => {
                if (newDetail[key] !== undefined && newDetail[key] !== null) {
                    localDetail.value[key] = newDetail[key];
                }
            });
        }
    }, { deep: true, immediate: true });

    // Watch for changes in local state and emit updates
    watch(localDetail, (newLocalDetail) => {
        console.log('Local detail changed, emitting update:', newLocalDetail);
        emit('update:detail', newLocalDetail);
    }, { deep: true });

    // Create computed property for capped interest months to handle type conversion
    const cappedInterestMonths = computed({
        get: () => Number(localDetail.value.capped_interest_months) || 9,
        set: (val) => { 
            localDetail.value.capped_interest_months = val;
        }
    });

    // Initialize values
    onMounted(() => {
        // Ensure the detail object exists and has all required fields
        if (!props.detail) {
            console.warn('Detail object is not provided to Calculation component');
            return;
        }

        console.log('Calculation component detail object:', props.detail);
        console.log('Detail object keys:', Object.keys(props.detail));

        // Initialize local state with props data
        if (props.detail) {
            Object.keys(localDetail.value).forEach(key => {
                if (props.detail[key] !== undefined && props.detail[key] !== null) {
                    localDetail.value[key] = props.detail[key];
                }
            });
        }
        
        console.log('Calculation component initialized with local detail:', localDetail.value);
        console.log('All fields after initialization:', {
            establishment_fee_rate: localDetail.value.establishment_fee_rate,
            capped_interest_months: localDetail.value.capped_interest_months,
            monthly_line_fee_rate: localDetail.value.monthly_line_fee_rate,
            brokerage_fee_rate: localDetail.value.brokerage_fee_rate,
            application_fee: localDetail.value.application_fee,
            due_diligence_fee: localDetail.value.due_diligence_fee,
            legal_fee_before_gst: localDetail.value.legal_fee_before_gst,
            valuation_fee: localDetail.value.valuation_fee,
            monthly_account_fee: localDetail.value.monthly_account_fee,
            working_fee: localDetail.value.working_fee,
            calculated_loan_amount: localDetail.value.calculated_loan_amount
        });
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
    
    /* NEW: Styling for loan amount display */
    .loan-amount-display {
        background-color: #f8f9fa;
        border: 1px solid #e9ecef;
        border-radius: 4px;
        padding: 10px;
    }
    
    .loan-amount-display :deep(.el-input__inner) {
        background-color: #ffffff;
        font-weight: 600;
        color: #2984DE;
    }
    
    /* NEW: Styling for warning message */
    .warning-message {
        grid-column: 1 / 3;
    }
    
    .warning-content {
        display: flex;
        align-items: center;
        gap: 8px;
        padding: 12px;
        background-color: #fdf6ec;
        border: 1px solid #f5dab1;
        border-radius: 4px;
        color: #e6a23c;
        font-size: 0.8rem;
    }
</style>
