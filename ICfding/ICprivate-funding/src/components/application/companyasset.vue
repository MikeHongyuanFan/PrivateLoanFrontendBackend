<template>
    <div class="content">
        <!-- Enhanced Asset Summary from Cascade Data -->
        <div v-if="summary && summary.length > 0" class="form">
            <div v-for="(borrower, index) in summary" :key="index" class="borrower-section">
                <div class="section-header">
                    <h3>{{ borrower.is_company ? borrower.company_name : `${borrower.first_name} ${borrower.last_name}` }}</h3>
                    <p class="borrower-type">{{ borrower.is_company ? 'Company Borrower' : 'Individual Borrower/Guarantor' }}</p>
                </div>
                
                <!-- Financial Summary -->
                <div class="summary-grid">
                    <div class="item">
                        <p class="title">Total Assets</p>
                        <p>{{ formatCurrency(borrower.total_assets) }}</p>
                    </div>
                    <div class="item">
                        <p class="title">Total Liabilities</p>
                        <p>{{ formatCurrency(borrower.total_liabilities) }}</p>
                    </div>
                    <div class="item">
                        <p class="title">Net Worth</p>
                        <p>{{ formatCurrency(borrower.net_worth) }}</p>
                    </div>
                </div>
                
                <!-- Assets Section -->
                <div v-if="borrower.assets && borrower.assets.length > 0" class="assets-section">
                    <h4>Assets & Liabilities</h4>
                    <div class="assets-grid">
                        <div v-for="(asset, assetIndex) in borrower.assets" :key="assetIndex" class="asset-item">
                            <div class="item">
                                <p class="title">Assets & Liabilities Type</p>
                                <p>{{ asset.asset_type || '-' }}</p>
                            </div>
                            <div class="item">
                                <p class="title">Description</p>
                                <p>{{ asset.description || '-' }}</p>
                            </div>
                            <div class="item">
                                <p class="title">Value</p>
                                <p>{{ formatCurrency(asset.value) }}</p>
                            </div>
                            <div class="item">
                                <p class="title">Amount Owing</p>
                                <p>{{ formatCurrency(asset.amount_owing) }}</p>
                            </div>
                            <div class="item">
                                <p class="title">To Be Refinanced</p>
                                <p>{{ asset.to_be_refinanced ? 'Yes' : 'No' }}</p>
                            </div>
                            <div class="item">
                                <p class="title">Address</p>
                                <p>{{ asset.address || '-' }}</p>
                            </div>
                        </div>
                    </div>
                </div>
                
                <!-- Liabilities Section -->
                <div v-if="borrower.liabilities && borrower.liabilities.length > 0" class="liabilities-section">
                    <h4>Liabilities</h4>
                    <div class="liabilities-grid">
                        <div v-for="(liability, liabilityIndex) in borrower.liabilities" :key="liabilityIndex" class="liability-item">
                            <div class="item">
                                <p class="title">Liability Type</p>
                                <p>{{ liability.liability_type || '-' }}</p>
                            </div>
                            <div class="item">
                                <p class="title">Description</p>
                                <p>{{ liability.description || '-' }}</p>
                            </div>
                            <div class="item">
                                <p class="title">Amount</p>
                                <p>{{ formatCurrency(liability.amount) }}</p>
                            </div>
                            <div class="item">
                                <p class="title">Monthly Payment</p>
                                <p>{{ formatCurrency(liability.monthly_payment) }}</p>
                            </div>
                            <div class="item">
                                <p class="title">To Be Refinanced</p>
                                <p>{{ liability.to_be_refinanced ? 'Yes' : 'No' }}</p>
                            </div>
                            <div class="item">
                                <p class="title">Address</p>
                                <p>{{ liability.address || '-' }}</p>
                            </div>
                        </div>
                    </div>
                </div>
                
                <!-- No Data Messages -->
                <div v-if="(!borrower.assets || borrower.assets.length === 0) && (!borrower.liabilities || borrower.liabilities.length === 0)" class="no-data">
                    <p>No assets or liabilities found for this {{ borrower.is_company ? 'company' : 'borrower/guarantor' }}</p>
                </div>
            </div>
        </div>

        <!-- Legacy Single Borrower View (if needed) -->
        <div v-else-if="borrowerId" class="form">
            <div v-loading="loading" class="assets-section">
                <h4>Assets & Liabilities</h4>
                <div class="assets-grid">
                    <div v-for="(asset, index) in assets" :key="index" class="asset-item">
                        <div class="item">
                            <p class="title">Assets & Liabilities Type</p>
                            <p>{{ asset.asset_type || '-' }}</p>
                        </div>
                        <div class="item">
                            <p class="title">Description</p>
                            <p>{{ asset.description || '-' }}</p>
                        </div>
                        <div class="item">
                            <p class="title">Value</p>
                            <p>{{ formatCurrency(asset.value) }}</p>
                        </div>
                        <div class="item">
                            <p class="title">Amount Owing</p>
                            <p>{{ formatCurrency(asset.amount_owing) }}</p>
                        </div>
                        <div class="item">
                            <p class="title">To Be Refinanced</p>
                            <p>{{ asset.to_be_refinanced ? 'Yes' : 'No' }}</p>
                        </div>
                        <div class="item">
                            <p class="title">Address</p>
                            <p>{{ asset.address || '-' }}</p>
                        </div>
                    </div>
                </div>
            </div>
            <div v-if="error" class="error-message">{{ error }}</div>
            <div v-if="!loading && (!assets || assets.length === 0)" class="no-data">No assets found</div>
        </div>

        <!-- No Data Message -->
        <div v-else class="no-data">
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
    min-height: 250px;      
}

.form {
    display: flex;
    flex-direction: column;
    gap: 30px;
}

.borrower-section {
    margin-bottom: 30px;
}

.section-header {
    margin-bottom: 20px;
}

.section-header h3 {
    margin: 0 0 5px 0;
    color: #384144;
    font-feature-settings: 'liga' off, 'clig' off;
    font-size: 0.9rem;
    font-style: normal;
    font-weight: 500;
    line-height: 12px;
}

.borrower-type {
    margin: 0;
    color: #7A858E;
    font-feature-settings: 'liga' off, 'clig' off;
    font-size: 0.75rem;
    font-style: normal;
    font-weight: 500;
    line-height: 12px;
}

.summary-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 20px;
    margin-bottom: 20px;
}

.assets-section, .liabilities-section {
    margin-bottom: 20px;
}

.assets-section h4, .liabilities-section h4 {
    margin: 0 0 15px 0;
    color: #384144;
    font-feature-settings: 'liga' off, 'clig' off;
    font-size: 0.9rem;
    font-style: normal;
    font-weight: 500;
    line-height: 12px;
}

.assets-grid, .liabilities-grid {
    display: flex;
    flex-direction: column;
    gap: 20px;
}

.asset-item, .liability-item {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 20px;
    padding: 15px;
    background: #FAFAFA;
    border-radius: 6px;
    border: 1px solid #E8EBEE;
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
    font-feature-settings: 'liga' off, 'clig' off;
    font-size: 0.75rem;
    font-style: normal;
    font-weight: 500;
    line-height: 12px;
}

.error-message {
    color: #f56c6c;
    font-size: 0.75rem;
    margin-top: 10px;
    text-align: center;
}

.no-data {
    text-align: center;
    padding: 40px;
    color: #666;
    font-style: italic;
}

.no-data p {
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
    .summary-grid {
        grid-template-columns: 1fr;
    }
    
    .asset-item, .liability-item {
        grid-template-columns: 1fr;
    }
}
</style>