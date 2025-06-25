<template>
    <!-- 
    UNIFIED DATA DISPLAY:
    This component displays guarantor assets and liabilities from the unified Asset and Liability tables
    in a single combined table to reflect the unified data structure approach.
    -->
    <div class="content">
        <div v-if="!guarantorsWithFinancialItems.length" class="no-data">
            <p>No guarantor financial information in this application</p>
        </div>
        <div v-else class="form">
            <div v-for="(guarantor, gIndex) in guarantorsWithFinancialItems" :key="gIndex" class="guarantor-section">
                <div class="section-header">
                    <h3>{{ guarantor.first_name }} {{ guarantor.last_name }}</h3>
                    <p class="guarantor-type">Guarantor</p>
                </div>
                
                <!-- Financial Summary -->
                <div class="summary-grid">
                    <div class="item">
                        <p class="title">Total Assets</p>
                        <p>{{ formatCurrency(guarantor.totalAssetValue) }}</p>
                    </div>
                    <div class="item">
                        <p class="title">Total Liabilities</p>
                        <p>{{ formatCurrency(guarantor.totalLiabilityAmount) }}</p>
                    </div>
                    <div class="item">
                        <p class="title">Net Worth</p>
                        <p>{{ formatCurrency(guarantor.netWorth) }}</p>
                    </div>
                </div>
                
                <div v-if="!guarantor.financialItems || guarantor.financialItems.length === 0" class="no-data">
                    <p>No financial items (assets or liabilities) for this guarantor</p>
                </div>
                
                <template v-else>
                    <!-- Assets Section -->
                    <div v-if="guarantor.financialItems.filter(item => item.itemType === 'Asset').length > 0" class="assets-section">
                        <h4>Assets & Liabilities</h4>
                        <div class="assets-grid">
                            <div v-for="(item, index) in guarantor.financialItems.filter(item => item.itemType === 'Asset')" :key="index" class="asset-item">
                                <div class="item">
                                    <p class="title">Assets & Liabilities Type</p>
                                    <p>{{ item.category || '-' }}</p>
                                </div>
                                <div class="item">
                                    <p class="title">Description</p>
                                    <p>{{ item.description || '-' }}</p>
                                </div>
                                <div class="item">
                                    <p class="title">Value</p>
                                    <p>{{ formatCurrency(item.primaryAmount) }}</p>
                                </div>
                                <div class="item">
                                    <p class="title">Amount Owing</p>
                                    <p>{{ formatCurrency(item.secondaryAmount) }}</p>
                                </div>
                                <div class="item">
                                    <p class="title">BG Type</p>
                                    <p>{{ item.bg_type || 'BG1' }}</p>
                                </div>
                            </div>
                        </div>
                    </div>
                    
                    <!-- Liabilities Section -->
                    <div v-if="guarantor.financialItems.filter(item => item.itemType === 'Liability').length > 0" class="liabilities-section">
                        <h4>Assets & Liabilities</h4>
                        <div class="liabilities-grid">
                            <div v-for="(item, index) in guarantor.financialItems.filter(item => item.itemType === 'Liability')" :key="index" class="liability-item">
                                <div class="item">
                                    <p class="title">Assets & Liabilities Type</p>
                                    <p>{{ item.category || '-' }}</p>
                                </div>
                                <div class="item">
                                    <p class="title">Description</p>
                                    <p>{{ item.description || '-' }}</p>
                                </div>
                                <div class="item">
                                    <p class="title">Amount</p>
                                    <p>{{ formatCurrency(item.primaryAmount) }}</p>
                                </div>
                                <div class="item">
                                    <p class="title">Monthly Payment</p>
                                    <p>{{ formatCurrency(item.secondaryAmount) }}</p>
                                </div>
                                <div class="item">
                                    <p class="title">BG Type</p>
                                    <p>{{ item.bg_type || 'BG1' }}</p>
                                </div>
                            </div>
                        </div>
                    </div>
                </template>
            </div>
        </div>
    </div>
</template>

<script setup>
    import { ref, computed } from 'vue';

    const props = defineProps({
        detail: Object
    });
    
    // Unified financial items from both Asset and Liability tables
    // Combines assets and liabilities into a single display structure
    const guarantorsWithFinancialItems = computed(() => {
        if (!props.detail || !props.detail.guarantors) return [];
        
        return props.detail.guarantors.map(guarantor => {
            const assets = guarantor.assets || [];      // From unified Asset table
            const liabilities = guarantor.liabilities || [];  // From unified Liability table
            
            // Combine assets and liabilities into unified financial items
            const financialItems = [];
            
            // Add assets to the unified list
            assets.forEach(asset => {
                financialItems.push({
                    itemType: 'Asset',
                    category: asset.asset_type,
                    description: asset.description,
                    descriptionIfApplicable: asset.description_if_applicable,
                    primaryAmount: asset.value,
                    secondaryAmount: asset.amount_owing,
                    bg_type: asset.bg_type,
                    originalData: asset
                });
            });
            
            // Add liabilities to the unified list
            liabilities.forEach(liability => {
                financialItems.push({
                    itemType: 'Liability',
                    category: liability.liability_type,
                    description: liability.description,
                    descriptionIfApplicable: liability.description_if_applicable,
                    primaryAmount: liability.amount,
                    secondaryAmount: liability.monthly_payment,
                    bg_type: liability.bg_type,
                    originalData: liability
                });
            });
            
            // Sort by type (Assets first, then Liabilities) and then by BG type
            financialItems.sort((a, b) => {
                if (a.itemType !== b.itemType) {
                    return a.itemType === 'Asset' ? -1 : 1;
                }
                return (a.bg_type || 'BG1').localeCompare(b.bg_type || 'BG1');
            });
            
            // Calculate totals
            const totalAssetValue = assets.reduce((sum, asset) => sum + (parseFloat(asset.value) || 0), 0);
            const totalLiabilityAmount = liabilities.reduce((sum, liability) => sum + (parseFloat(liability.amount) || 0), 0);
            const netWorth = totalAssetValue - totalLiabilityAmount;
            
            return {
                ...guarantor,
                financialItems,
                totalAssetValue,
                totalLiabilityAmount,
                netWorth
            };
        });
    });
    
    const formatNumber = (value) => {
        if (!value) return '0';
        return parseFloat(value).toLocaleString('en-US', {
            minimumFractionDigits: 2,
            maximumFractionDigits: 2
        });
    };

    const formatCurrency = (value) => {
        if (!value) return '$0';
        return '$' + parseFloat(value).toLocaleString('en-US', {
            minimumFractionDigits: 2,
            maximumFractionDigits: 2
        });
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
        display: flex;
        flex-direction: column;
        gap: 30px;
    }

    .guarantor-section {
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

    .guarantor-type {
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
