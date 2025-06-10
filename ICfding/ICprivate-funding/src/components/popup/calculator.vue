<template>
    <div class="popup">
        <div class="popup_title">
            <h1>Funding Calculator</h1>
            <div class="close">
                <!-- <el-icon :size="20" style="cursor: pointer; color: #7A858E;" @click="handleMinimize"><Minus /></el-icon> -->
                <el-icon :size="20" style="cursor: pointer; color: #7A858E;" @click="handleClose"><Close /></el-icon>                    
            </div>
        </div>
        <div class="popup_content">
            <div class="form">
                <div class="long_item">
                    <h2>Funding Calculation Inputs <span class="required">*</span></h2>
                    <span class="hint">Parameters used to calculate funding details</span>
                </div>
                <div class="long_item">
                    <h2>Total Loan Amount <span class="required">*</span></h2>
                    <el-input v-model="detail.loan_amount" type="number" step="0.01" placeholder="e.g. 2.5" />
                </div>
                <div class="item">
                    <p>Establishment Fee Rate (%) <span class="required">*</span></p>
                    <el-input v-model="detail.establishment_fee_rate" type="number" step="0.01" placeholder="e.g. 2.5" />
                    <span class="hint">Percentage rate for establishment fee (max 3 digits before decimal)</span>
                </div>
                <div class="item">
                    <p>Interest Rate (%) <span class="required">*</span></p>
                    <el-input v-model="detail.interest_rate" type="number" step="0.01" placeholder="e.g. 2.5" />
                    <span class="hint">Percentage rate for interest (max 3 digits before decimal)</span>
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
                    <p>Security Value ($) <span class="required">*</span></p>
                    <el-input v-model="detail.security_value" type="number" placeholder="e.g. 500" />
                    <span class="hint">Fixed security value amount (max 8 digits)</span>
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
                
                <div class="long_item">
                    <el-button type="primary" @click="calculate" :loading="loading">Calculate Funding</el-button>
                </div>
                
                <!-- Results section -->
                <div v-if="calculationResults" class="long_item results-container">
                    <el-card class="calculation-results">
                        <template #header>
                            <div class="card-header">
                                <h3>Calculation Results</h3>
                            </div>
                        </template>
                        <div class="results-content">
                            <div class="result-item">
                                <span class="result-label">Total Upfront Fees:</span>
                                <span class="result-value">${{ formatCurrency(calculationResults.total_upfront_fees) }}</span>
                            </div>
                            <div class="result-item">
                                <span class="result-label">Monthly Fees:</span>
                                <span class="result-value">${{ formatCurrency(calculationResults.monthly_fees) }}</span>
                            </div>
                            <div class="result-item">
                                <span class="result-label">Estimated Cost Over 12 Months:</span>
                                <span class="result-value">${{ formatCurrency(calculationResults.estimated_annual_cost) }}</span>
                            </div>
                            <div class="result-item" v-if="calculationResults.interest_capped_at">
                                <span class="result-label">Interest Capped At:</span>
                                <span class="result-value">${{ formatCurrency(calculationResults.interest_capped_at) }}</span>
                            </div>
                            <div class="result-item" v-if="calculationResults.total_fees_with_gst">
                                <span class="result-label">Total Fees (with GST):</span>
                                <span class="result-value">${{ formatCurrency(calculationResults.total_fees_with_gst) }}</span>
                            </div>
                        </div>
                    </el-card>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
    import { ref, computed, onMounted } from 'vue';
    import { ElMessage } from 'element-plus';
    import { api } from '@/api';

    const emit = defineEmits(['close', 'minimize']);

    const handleClose = () => {
        emit('close');
    };
    
    const handleMinimize = () => {
        emit('minimize');
    };

    // Initialize the detail object with default values
    const detail = ref({
        establishment_fee_rate: 1.2,
        capped_interest_months: 9,
        monthly_line_fee_rate: 0.8,
        brokerage_fee_rate: 2.5,
        application_fee: 500,
        due_diligence_fee: 300,
        legal_fee_before_gst: 400,
        valuation_fee: 700,
        monthly_account_fee: 50,
        working_fee: 0,
        loan_amount: 10000,
        interest_rate: 2.5,
        security_value: 1000
    });

    const loading = ref(false);
    const calculationResults = ref(null);

    // Create computed property for capped interest months to handle type conversion
    const cappedInterestMonths = computed({
        get: () => Number(detail.value.capped_interest_months) || 9,
        set: (val) => { detail.value.capped_interest_months = val }
    });

    // Function to format currency values
    const formatCurrency = (value) => {
        return parseFloat(value).toLocaleString('en-US', {
            minimumFractionDigits: 2,
            maximumFractionDigits: 2
        });
    };

    // Function to calculate funding details
    const calculate = async () => {
        // Validate that all required fields are filled
        const requiredFields = [
            'establishment_fee_rate',
            'capped_interest_months',
            'monthly_line_fee_rate',
            'brokerage_fee_rate',
            'application_fee',
            'due_diligence_fee',
            'legal_fee_before_gst',
            'valuation_fee',
            'monthly_account_fee',
            'loan_amount',
            'security_value',
            'interest_rate'
        ];

        const missingFields = requiredFields.filter(field => {
            const value = detail.value[field];
            return value === undefined || value === null || value === '';
        });

        if (missingFields.length > 0) {
            ElMessage.error('Please fill in all required fields before calculating');
            return;
        }

        // Prepare payload with only the funding calculation input fields
        const payload = {
            application_fee: Number(detail.value.application_fee),
            brokerage_fee_rate: Number(detail.value.brokerage_fee_rate),
            capped_interest_months: Number(detail.value.capped_interest_months),
            due_diligence_fee: Number(detail.value.due_diligence_fee),
            establishment_fee_rate: Number(detail.value.establishment_fee_rate),
            legal_fee_before_gst: Number(detail.value.legal_fee_before_gst),
            monthly_account_fee: Number(detail.value.monthly_account_fee),
            monthly_line_fee_rate: Number(detail.value.monthly_line_fee_rate),
            valuation_fee: Number(detail.value.valuation_fee),
            working_fee: Number(detail.value.working_fee) || 0,
            loan_amount: Number(detail.value.loan_amount) || 0,
            security_value: Number(detail.value.security_value),
            interest_rate: Number(detail.value.interest_rate),
        };

        loading.value = true;
        try {
            const [error, response] = await api.calculator(payload);

            if (error) {
                console.error("Calculation error:", error);
                ElMessage.error(error.detail || 'Failed to calculate funding details');
                return;
            }

            // Handle successful response
            calculationResults.value = response;
            ElMessage.success('Funding calculation completed successfully');
        } catch (err) {
            console.error("Unexpected error during calculation:", err);
            ElMessage.error('An unexpected error occurred during calculation');
        } finally {
            loading.value = false;
        }
    };

    // Initialize calculation with default values on mount
    onMounted(() => {

    });
</script>

<style scoped>
    .popup {
        position: fixed;
        top: 0;
        right: 0;
        bottom: 0;
        display: flex;
        flex-direction: column;
        background: white;
        border: none;
        box-shadow: -8px -1px 9.3px 0px rgba(202, 202, 202, 0.16);
        width: 40%;
        height: 100vh;
        overflow: hidden;
        z-index: 1000;
    }
    .popup_title {
        width: 100%;
        padding: 20px 10px;
        display: flex;
        flex-direction: row;
        justify-content: space-between;
        align-items: center;
        border-bottom: 1.5px solid var(--Line, #E1E1E1);
    }
    .popup_content {
        flex: 1;
        padding: 20px;
        overflow-y: auto;
    }
    h1 {
        color: #384144;
        font-feature-settings: 'liga' off, 'clig' off;
        font-size: 1.1rem;
        font-style: normal;
        font-weight: 500;
        line-height: 12px;
    }
    h2 {
        color: #384144;
        font-feature-settings: 'liga' off, 'clig' off;
        font-size: 0.9rem;
        font-style: normal;
        font-weight: 500;
        line-height: 12px;
        margin: 0;
    }
    .close {
        display: flex;
        flex-direction: row;
        align-items: center;
        gap: 20px;
    }
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
    .results-container {
        margin-top: 20px;
        width: 100%;
    }
    .calculation-results {
        width: 100%;
    }
    .card-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    .card-header h3 {
        margin: 0;
        font-size: 1rem;
    }
    .results-content {
        display: flex;
        flex-direction: column;
        gap: 12px;
    }
    .result-item {
        display: flex;
        justify-content: space-between;
        padding: 8px 0;
        border-bottom: 1px solid #f0f0f0;
    }
    .result-item:last-child {
        border-bottom: none;
    }
    .result-label {
        font-weight: 500;
        color: #606266;
    }
    .result-value {
        font-weight: 600;
        color: #303133;
    }
</style>