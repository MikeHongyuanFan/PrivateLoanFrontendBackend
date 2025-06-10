<template>
    <div class="content">
        <div v-if="!guarantorsWithAssets.length">
            <p>No guarantor assets in this application</p>
        </div>
        <div class="form" v-for="(guarantor, gIndex) in guarantorsWithAssets" :key="gIndex">
            <div class="index"><h1>{{ guarantor.first_name }} {{ guarantor.last_name }} - Assets</h1></div>
            
            <div v-if="!guarantor.assets || guarantor.assets.length === 0" class="no-assets">
                <p>No assets for this guarantor</p>
            </div>
            
            <template v-else>
                <div class="item header" v-if="guarantor.assets && guarantor.assets.length > 0">
                    <p class="title">Asset Type</p>
                    <p class="title">Description</p>
                    <p class="title">Value</p>
                    <p class="title">Amount Owing</p>
                    <p class="title">To Be Refinanced</p>
                </div>
                
                <div class="item" v-for="(asset, index) in guarantor.assets" :key="index">
                    <p>{{ asset.asset_type || '-' }}</p>
                    <p>{{ asset.description || '-' }}</p>
                    <p>${{ formatNumber(asset.value) || '0' }}</p>
                    <p>${{ formatNumber(asset.amount_owing) || '0' }}</p>
                    <p>{{ asset.to_be_refinanced ? 'Yes' : 'No' }}</p>
                </div>
            </template>
            
            <div class="index"><h1>{{ guarantor.first_name }} {{ guarantor.last_name }} - Liabilities</h1></div>
            
            <div v-if="!guarantor.liabilities || guarantor.liabilities.length === 0" class="no-liabilities">
                <p>No liabilities for this guarantor</p>
            </div>
            
            <template v-else>
                <div class="item header" v-if="guarantor.liabilities && guarantor.liabilities.length > 0">
                    <p class="title">Liability Type</p>
                    <p class="title">Description</p>
                    <p class="title">Amount</p>
                    <p class="title">Monthly Payment</p>
                    <p class="title">To Be Refinanced</p>
                </div>
                
                <div class="item" v-for="(liability, index) in guarantor.liabilities" :key="index">
                    <p>{{ liability.liability_type || '-' }}</p>
                    <p>{{ liability.description || '-' }}</p>
                    <p>${{ formatNumber(liability.amount) || '0' }}</p>
                    <p>${{ formatNumber(liability.monthly_payment) || '0' }}</p>
                    <p>{{ liability.to_be_refinanced ? 'Yes' : 'No' }}</p>
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
    
    const guarantorsWithAssets = computed(() => {
        if (!props.detail || !props.detail.guarantors) return [];
        return props.detail.guarantors.map(guarantor => {
            return {
                ...guarantor,
                assets: guarantor.assets || [],
                liabilities: guarantor.liabilities || []
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
        grid-template-columns: 1fr 1fr 1fr 1fr 1fr;
        gap: 10px;
        padding: 10px 0;
        border-bottom: 1px solid #E8EBEE;
    }
    .header {
        border-bottom: 2px solid #E8EBEE;
        font-weight: bold;
    }
    .no-assets, .no-liabilities {
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
    }
</style>
