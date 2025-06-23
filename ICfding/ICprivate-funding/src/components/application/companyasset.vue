<template>
    <div class="content">
        <!-- Enhanced Asset Summary from Cascade Data -->
        <div v-if="summary && summary.length > 0" class="asset_summary">
            <div class="summary_header">
                <h2>💰 Assets & Liabilities Overview</h2>
            </div>
            <div class="borrower_assets">
                <div v-for="(borrower, index) in summary" :key="index" class="borrower_section">
                    <div class="borrower_header">
                        <h3>{{ borrower.is_company ? borrower.company_name : `${borrower.first_name} ${borrower.last_name}` }}</h3>
                        <p class="borrower_type">{{ borrower.is_company ? 'Company Borrower' : 'Individual Borrower/Guarantor' }}</p>
                    </div>
                    
                    <!-- Assets Table -->
                    <div v-if="borrower.assets && borrower.assets.length > 0" class="assets_section">
                        <h4>Assets ({{ borrower.assets.length }})</h4>
                        <el-table :data="borrower.assets" style="width: 100%" class="assets_table">
                            <el-table-column prop="asset_type" label="Asset Type" min-width="120">
                                <template #default="{ row }">{{ row.asset_type || '-' }}</template>
                            </el-table-column>
                            <el-table-column prop="description" label="Description" min-width="200">
                                <template #default="{ row }">{{ row.description || '-' }}</template>
                            </el-table-column>
                            <el-table-column prop="value" label="Value" min-width="120">
                                <template #default="{ row }">{{ formatCurrency(row.value) }}</template>
                            </el-table-column>
                            <el-table-column prop="amount_owing" label="Amount Owing" min-width="120">
                                <template #default="{ row }">{{ formatCurrency(row.amount_owing) }}</template>
                            </el-table-column>
                            <el-table-column prop="to_be_refinanced" label="To Be Refinanced" min-width="120">
                                <template #default="{ row }">{{ row.to_be_refinanced ? 'Yes' : 'No' }}</template>
                            </el-table-column>
                            <el-table-column prop="address" label="Address" min-width="200">
                                <template #default="{ row }">{{ row.address || '-' }}</template>
                            </el-table-column>
                        </el-table>
                    </div>
                    
                    <!-- Liabilities Table -->
                    <div v-if="borrower.liabilities && borrower.liabilities.length > 0" class="liabilities_section">
                        <h4>Liabilities ({{ borrower.liabilities.length }})</h4>
                        <el-table :data="borrower.liabilities" style="width: 100%" class="liabilities_table">
                            <el-table-column prop="liability_type" label="Liability Type" min-width="120">
                                <template #default="{ row }">{{ row.liability_type || '-' }}</template>
                            </el-table-column>
                            <el-table-column prop="description" label="Description" min-width="200">
                                <template #default="{ row }">{{ row.description || '-' }}</template>
                            </el-table-column>
                            <el-table-column prop="amount" label="Amount" min-width="120">
                                <template #default="{ row }">{{ formatCurrency(row.amount) }}</template>
                            </el-table-column>
                            <el-table-column prop="monthly_payment" label="Monthly Payment" min-width="120">
                                <template #default="{ row }">{{ formatCurrency(row.monthly_payment) }}</template>
                            </el-table-column>
                            <el-table-column prop="to_be_refinanced" label="To Be Refinanced" min-width="120">
                                <template #default="{ row }">{{ row.to_be_refinanced ? 'Yes' : 'No' }}</template>
                            </el-table-column>
                        </el-table>
                    </div>
                    
                    <!-- No Data Messages -->
                    <div v-if="(!borrower.assets || borrower.assets.length === 0) && (!borrower.liabilities || borrower.liabilities.length === 0)" class="no_data">
                        <p>No assets or liabilities found for this {{ borrower.is_company ? 'company' : 'borrower/guarantor' }}</p>
                    </div>
                </div>
            </div>
        </div>

        <!-- Legacy Single Borrower View (if needed) -->
        <div v-else-if="borrowerId" class="legacy_view">
            <el-table v-loading="loading" :data="assets" style="width: 100%">
                <el-table-column prop="asset_type" label="Asset Type" min-width="120">
                    <template #default="{ row }">{{ row.asset_type || '-' }}</template>
                </el-table-column>
                <el-table-column prop="description" label="Description" min-width="200">
                    <template #default="{ row }">{{ row.description || '-' }}</template>
                </el-table-column>
                <el-table-column prop="value" label="Value" min-width="120">
                    <template #default="{ row }">{{ formatCurrency(row.value) }}</template>
                </el-table-column>
                <el-table-column prop="amount_owing" label="Amount Owing" min-width="120">
                    <template #default="{ row }">{{ formatCurrency(row.amount_owing) }}</template>
                </el-table-column>
                <el-table-column prop="to_be_refinanced" label="To Be Refinanced" min-width="120">
                    <template #default="{ row }">{{ row.to_be_refinanced ? 'Yes' : 'No' }}</template>
                </el-table-column>
                <el-table-column prop="address" label="Address" min-width="200">
                    <template #default="{ row }">{{ row.address || '-' }}</template>
                </el-table-column>
            </el-table>
            <div v-if="error" class="error-message">{{ error }}</div>
            <div v-if="!loading && (!assets || assets.length === 0)" class="empty-state">No assets found</div>
        </div>

        <!-- No Data Message -->
        <div v-else class="no_data">
            <p>No borrower asset information available</p>
        </div>
    </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { ElMessage } from 'element-plus'
import { api } from '@/api'

const props = defineProps({
    borrowerId: { 
        type: Number, 
        required: false,
        default: null
    },
    detail: {
        type: Object,
        required: false,
        default: () => ({})
    },
    summary: {
        type: Array,
        required: false,
        default: () => []
    }
})

const assets = ref([])
const loading = ref(false)
const error = ref(null)

const formatCurrency = (value) => {
    if (!value) return '-'
    return new Intl.NumberFormat('en-AU', { style: 'currency', currency: 'AUD' }).format(value)
}

const fetchAssets = async () => {
    if (!props.borrowerId) return
    
    loading.value = true
    error.value = null
    try {
        const [err, data] = await api.getBorrowerAssets(props.borrowerId)
        if (err) {
            throw new Error('Failed to fetch assets')
        }
        assets.value = data.results || []
    } catch (err) {
        error.value = 'Error loading assets. Please try again.'
        ElMessage.error('Failed to load company assets')
        console.error('Error fetching assets:', err)
    } finally {
        loading.value = false
    }
}

onMounted(() => {
    if (props.borrowerId && (!props.summary || props.summary.length === 0)) {
        fetchAssets()
    }
})
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

/* Asset Summary Styles */
.asset_summary {
    display: flex;
    flex-direction: column;
    gap: 20px;
}
.summary_header h2 {
    color: #384144;
    font-size: 1.2rem;
    font-weight: 600;
    margin: 0;
}
.borrower_assets {
    display: flex;
    flex-direction: column;
    gap: 30px;
}
.borrower_section {
    border: 1px solid #E8EBEE;
    border-radius: 8px;
    padding: 20px;
    background: #FAFAFA;
}
.borrower_header {
    display: flex;
    flex-direction: column;
    gap: 10px;
    margin-bottom: 20px;
    padding-bottom: 15px;
    border-bottom: 1px solid #E8EBEE;
}
.borrower_header h3 {
    color: #2984DE;
    font-size: 1rem;
    font-weight: 600;
    margin: 0;
}
.borrower_type {
    color: #909399;
    font-size: 0.8rem;
    font-weight: 400;
}

/* Section Styles */
.assets_section, .liabilities_section {
    margin-bottom: 20px;
}
.assets_section h4, .liabilities_section h4 {
    color: #384144;
    font-size: 0.9rem;
    font-weight: 600;
    margin: 0 0 10px 0;
}

/* Table Styles */
.assets_table, .liabilities_table {
    background: #FFF;
    border-radius: 6px;
}

/* Legacy and Error Styles */
.legacy_view {
    display: flex;
    flex-direction: column;
    gap: 10px;
}
.error-message {
    color: #f56c6c;
    font-size: 14px;
    margin-top: 10px;
    text-align: center;
}
.empty-state, .no_data {
    color: #909399;
    font-size: 14px;
    text-align: center;
    padding: 40px;
    font-style: italic;
}
.no_data p {
    margin: 0;
}

/* Element Plus Table Overrides */
:deep(.el-table) {
    --el-table-border-color: #E8EBEE;
    --el-table-header-bg-color: #F8F9FA;
    --el-table-row-hover-bg-color: #F8F9FA;
}
:deep(.el-table th) {
    background-color: #F8F9FA;
    color: #7A858E;
    font-weight: 600;
    font-size: 12px;
}
:deep(.el-table td) {
    color: #384144;
    font-size: 12px;
}

/* Responsive adjustments */
@media (max-width: 768px) {
    .borrower_header {
        align-items: flex-start;
    }
}
</style>