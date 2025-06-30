<template>
    <div class="content">
        <div class="form">
            <!-- Current Funding Calculation Result -->
            <div class="section" v-if="detail.funding_result">
                <h3>Current Funding Calculation</h3>
                <div class="calculation-grid">
                    <div class="calculation-item">
                        <p class="title">Loan Amount</p>
                        <p class="value">${{ formatCurrency(detail.funding_result.loan_amount || detail.loan_amount) }}</p>
                    </div>
                    <div class="calculation-item">
                        <p class="title">Total Fees</p>
                        <p class="value">${{ formatCurrency(detail.funding_result.total_fees) }}</p>
                    </div>
                    <div class="calculation-item">
                        <p class="title">Funds Available</p>
                        <p class="value highlight">${{ formatCurrency(detail.funding_result.funds_available) }}</p>
                    </div>
                </div>
                
                <!-- Detailed Fee Breakdown -->
                <div class="fee-breakdown">
                    <h4>Fee Breakdown</h4>
                    <div class="fee-grid">
                        <div class="fee-item" v-if="detail.funding_result.establishment_fee">
                            <span class="fee-label">Establishment Fee:</span>
                            <span class="fee-value">${{ formatCurrency(detail.funding_result.establishment_fee) }}</span>
                        </div>
                        <div class="fee-item" v-if="detail.funding_result.capped_interest">
                            <span class="fee-label">Capped Interest:</span>
                            <span class="fee-value">${{ formatCurrency(detail.funding_result.capped_interest) }}</span>
                        </div>
                        <div class="fee-item" v-if="detail.funding_result.line_fee">
                            <span class="fee-label">Line Fee:</span>
                            <span class="fee-value">${{ formatCurrency(detail.funding_result.line_fee) }}</span>
                        </div>
                        <div class="fee-item" v-if="detail.funding_result.brokerage_fee">
                            <span class="fee-label">Brokerage Fee:</span>
                            <span class="fee-value">${{ formatCurrency(detail.funding_result.brokerage_fee) }}</span>
                        </div>
                        <div class="fee-item" v-if="detail.funding_result.legal_fee">
                            <span class="fee-label">Legal Fee:</span>
                            <span class="fee-value">${{ formatCurrency(detail.funding_result.legal_fee) }}</span>
                        </div>
                        <div class="fee-item" v-if="detail.funding_result.application_fee">
                            <span class="fee-label">Application Fee:</span>
                            <span class="fee-value">${{ formatCurrency(detail.funding_result.application_fee) }}</span>
                        </div>
                        <div class="fee-item" v-if="detail.funding_result.due_diligence_fee">
                            <span class="fee-label">Due Diligence Fee:</span>
                            <span class="fee-value">${{ formatCurrency(detail.funding_result.due_diligence_fee) }}</span>
                        </div>
                        <div class="fee-item" v-if="detail.funding_result.valuation_fee">
                            <span class="fee-label">Valuation Fee:</span>
                            <span class="fee-value">${{ formatCurrency(detail.funding_result.valuation_fee) }}</span>
                        </div>
                        <div class="fee-item" v-if="detail.funding_result.monthly_account_fee">
                            <span class="fee-label">Monthly Account Fee:</span>
                            <span class="fee-value">${{ formatCurrency(detail.funding_result.monthly_account_fee) }}</span>
                        </div>
                        <div class="fee-item" v-if="detail.funding_result.working_fee">
                            <span class="fee-label">Working Fee:</span>
                            <span class="fee-value">${{ formatCurrency(detail.funding_result.working_fee) }}</span>
                        </div>
                    </div>
                </div>
            </div>
            
            <!-- No Funding Calculation Message -->
            <div class="section no-calculation" v-else>
                <div class="no-calculation-content">
                    <el-icon size="48" color="#909399"><InfoFilled /></el-icon>
                    <h3>No Funding Calculation Available</h3>
                    <p>This application doesn't have a funding calculation yet. Use the calculator to perform a funding calculation.</p>
                    <el-button type="primary" @click="openCalculator">
                        <el-icon><Money /></el-icon>
                        Open Calculator
                    </el-button>
                </div>
            </div>
            
            <!-- Funding Calculation History -->
            <div class="section" v-if="detail.funding_calculation_history && detail.funding_calculation_history.length > 0">
                <h3>Calculation History</h3>
                <el-timeline>
                    <el-timeline-item
                        v-for="(calculation, index) in detail.funding_calculation_history"
                        :key="index"
                        :timestamp="formatDate(calculation.created_at)"
                        :type="index === 0 ? 'primary' : 'info'"
                    >
                        <div class="history-item">
                            <div class="history-header">
                                <span class="calculation-date">{{ formatDate(calculation.created_at) }}</span>
                                <span class="calculation-user" v-if="calculation.created_by_details">
                                    by {{ calculation.created_by_details.first_name }} {{ calculation.created_by_details.last_name }}
                                </span>
                            </div>
                            <div class="history-results">
                                <div class="result-item">
                                    <span class="result-label">Total Fees:</span>
                                    <span class="result-value">${{ formatCurrency(calculation.calculation_result.total_fees) }}</span>
                                </div>
                                <div class="result-item">
                                    <span class="result-label">Funds Available:</span>
                                    <span class="result-value highlight">${{ formatCurrency(calculation.calculation_result.funds_available) }}</span>
                                </div>
                            </div>
                        </div>
                    </el-timeline-item>
                </el-timeline>
            </div>
        </div>
    </div>
</template>

<script setup>
    import { InfoFilled, Money } from '@element-plus/icons-vue';

    const props = defineProps({
        detail: Object
    });

    const emit = defineEmits(['open-calculator']);

    const formatCurrency = (value) => {
        if (!value && value !== 0) return '0.00';
        return parseFloat(value).toLocaleString('en-US', {
            minimumFractionDigits: 2,
            maximumFractionDigits: 2
        });
    };

    const formatDate = (dateString) => {
        if (!dateString) return '';
        return new Date(dateString).toLocaleString('en-US', {
            year: 'numeric',
            month: 'short',
            day: 'numeric',
            hour: '2-digit',
            minute: '2-digit'
        });
    };

    const openCalculator = () => {
        emit('open-calculator');
    };
</script>

<style scoped>
    .content {
        padding: 20px;
    }

    .form {
        display: flex;
        flex-direction: column;
        gap: 20px;
    }

    .section {
        background: #ffffff;
        border: 1px solid #e4e7ed;
        border-radius: 8px;
        padding: 20px;
    }

    .section h3 {
        margin: 0 0 20px 0;
        color: #303133;
        font-size: 1.2rem;
        font-weight: 600;
    }

    .section h4 {
        margin: 0 0 15px 0;
        color: #606266;
        font-size: 1rem;
        font-weight: 500;
    }

    .calculation-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 20px;
        margin-bottom: 20px;
    }

    .calculation-item {
        background: #f8f9fa;
        border: 1px solid #e9ecef;
        border-radius: 6px;
        padding: 15px;
        text-align: center;
    }

    .calculation-item .title {
        margin: 0 0 8px 0;
        color: #606266;
        font-size: 0.9rem;
        font-weight: 500;
    }

    .calculation-item .value {
        margin: 0;
        color: #303133;
        font-size: 1.3rem;
        font-weight: 600;
    }

    .calculation-item .value.highlight {
        color: #67c23a;
    }

    .fee-breakdown {
        margin-top: 20px;
    }

    .fee-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
        gap: 12px;
    }

    .fee-item {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 8px 12px;
        background: #f8f9fa;
        border-radius: 4px;
    }

    .fee-label {
        color: #606266;
        font-size: 0.9rem;
    }

    .fee-value {
        color: #303133;
        font-weight: 500;
    }

    .no-calculation {
        text-align: center;
        padding: 40px 20px;
    }

    .no-calculation-content {
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 16px;
    }

    .no-calculation-content h3 {
        margin: 0;
        color: #909399;
    }

    .no-calculation-content p {
        margin: 0;
        color: #909399;
        max-width: 400px;
    }

    .history-item {
        padding: 10px 0;
    }

    .history-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 10px;
    }

    .calculation-date {
        font-weight: 500;
        color: #303133;
    }

    .calculation-user {
        color: #909399;
        font-size: 0.9rem;
    }

    .history-results {
        display: flex;
        gap: 20px;
    }

    .result-item {
        display: flex;
        align-items: center;
        gap: 8px;
    }

    .result-label {
        color: #606266;
        font-size: 0.9rem;
    }

    .result-value {
        font-weight: 500;
        color: #303133;
    }

    .result-value.highlight {
        color: #67c23a;
    }

    @media (max-width: 768px) {
        .calculation-grid {
            grid-template-columns: 1fr;
        }

        .fee-grid {
            grid-template-columns: 1fr;
        }

        .history-results {
            flex-direction: column;
            gap: 8px;
        }
    }
</style> 