<template>
    <!-- 
    UNIFIED DATA DISPLAY:
    This component displays guarantor assets and liabilities from the unified Asset and Liability tables
    in a single combined table to reflect the unified data structure approach.
    -->
    <div class="content">
        <div v-if="!guarantorsWithFinancialItems.length">
            <p>No guarantor financial information in this application</p>
        </div>
        <div class="form" v-for="(guarantor, gIndex) in guarantorsWithFinancialItems" :key="gIndex">
            <div class="index">
                <h1>{{ guarantor.first_name }} {{ guarantor.last_name }} - Financial Items</h1>
                <p class="subtitle">Assets and Liabilities (Unified Table)</p>
            </div>
            
            <div v-if="!guarantor.financialItems || guarantor.financialItems.length === 0" class="no-financial-items">
                <p>No financial items (assets or liabilities) for this guarantor</p>
            </div>
            
            <template v-else>
                <div class="item header">
                    <p class="title">Type</p>
                    <p class="title">Category</p>
                    <p class="title">Description</p>
                    <p class="title">Description (if applicable)</p>
                    <p class="title">Value/Amount</p>
                    <p class="title">Amount Owing/Monthly Payment</p>
                    <p class="title">BG Type</p>
                </div>
                
                <div class="item" v-for="(item, index) in guarantor.financialItems" :key="index">
                    <p>{{ item.itemType }}</p>
                    <p>{{ item.category || '-' }}</p>
                    <p>{{ item.description || '-' }}</p>
                    <p>{{ item.descriptionIfApplicable || '-' }}</p>
                    <p>${{ formatNumber(item.primaryAmount) || '0' }}</p>
                    <p>${{ formatNumber(item.secondaryAmount) || '0' }}</p>
                    <p>{{ item.bg_type || 'BG1' }}</p>
                </div>
                
                <!-- Summary Row -->
                <div class="item summary" v-if="guarantor.financialItems.length > 0">
                    <p><strong>Total</strong></p>
                    <p>-</p>
                    <p>-</p>
                    <p>-</p>
                    <p><strong>${{ formatNumber(guarantor.totalAssetValue) }}</strong></p>
                    <p><strong>${{ formatNumber(guarantor.totalLiabilityAmount) }}</strong></p>
                    <p><strong>Net: ${{ formatNumber(guarantor.netWorth) }}</strong></p>
                </div>
            </template>
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
</script>

<style scoped>
    .content {
        display: flex;
        flex-direction: column;
        gap: 20px;        
    }
    .form {
        padding: 20px;
        border-radius: 6px;
        background: #FFF;
        display: flex;
        flex-direction: column;
        gap: 10px;
    }
    .item {
        display: grid;
        grid-template-columns: 1fr 1.5fr 2fr 2fr 1.2fr 1.5fr 1fr;
        gap: 10px;
        padding: 10px 0;
        border-bottom: 1px solid #E8EBEE;
    }
    .header {
        border-bottom: 2px solid #E8EBEE;
        font-weight: bold;
        background-color: #f8f9fa;
    }
    .summary {
        border-bottom: 2px solid #2196F3;
        background-color: #f0f8ff;
        font-weight: bold;
    }
    .no-financial-items {
        padding: 20px;
        text-align: center;
        color: #7A858E;
        font-style: italic;
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
    .index {
        margin: 20px 0 10px 0;
    }
    h1 {
        color: #384144;
        font-feature-settings: 'liga' off, 'clig' off;
        font-size: 0.9rem;
        font-style: normal;
        font-weight: 600;
        line-height: normal;
        margin: 0 0 5px 0;
    }
    .subtitle {
        color: #7A858E;
        font-size: 0.7rem;
        margin: 0;
        font-style: italic;
    }
</style>
