<template>
    <div class="form">
        <div class="long_item">
            <h1>Asset & Liabilities</h1>
        </div>
        <div v-if="companyList.length === 0" class="no-company">
            <p>No company borrowers found. Please add a company borrower first to manage assets.</p>
            <div class="add-company">
                <el-button type="primary" @click="$emit('addCompany')">Add Company Borrower</el-button>
            </div>
        </div>
        <div v-for="(company, index) in companyList" :key="`company-asset-${index}-${company.company_name || 'unnamed'}`" class="company">
            <div class="company-header">
                <h2>{{ company.company_name || `Company ${index + 1}` }}</h2>
                <p v-if="company.company_abn">ABN: {{ company.company_abn }}</p>
            </div>
            <div class="long_item">
                <h1>Assets</h1>
            </div>
            <div v-for="(asset, idx) in ensureAssets(company)" :key="idx" class="asset">
                <div class="item">
                    <p>Asset Type <span class="required">*</span></p>
                    <el-select v-model="asset.asset_type" placeholder="Select asset type">
                        <el-option value="Property" label="Property" />
                        <el-option value="Vehicle" label="Vehicle" />
                        <el-option value="Savings" label="Savings" />
                        <el-option value="Investment Shares" label="Investment Shares" />
                        <el-option value="Credit Card" label="Credit Card" />
                        <el-option value="Other Creditor" label="Other Creditor" />
                        <el-option value="Other" label="Other" />
                    </el-select>
                    <span class="hint">Type of asset</span>
                </div>
                <div class="item">
                    <p>Description</p>
                    <el-input v-model="asset.description" placeholder="Brief description of the asset" />
                    <span class="hint">Brief description of the asset</span>
                </div>
                <div class="item">
                    <p>Value ($)</p>
                    <el-input v-model="asset.value" type="number" placeholder="e.g. 250000" />
                    <span class="hint">Current market value (max 10 digits)</span>
                </div>
                <div class="item">
                    <p>Amount Owing ($)</p>
                    <el-input v-model="asset.amount_owing" type="number" placeholder="e.g. 150000" />
                    <span class="hint">Amount still owed on this asset</span>
                </div>
                <div class="item">
                    <p>To Be Refinanced</p>
                    <el-checkbox v-model="asset.to_be_refinanced">Yes</el-checkbox>
                    <span class="hint">Check if this asset will be refinanced</span>
                </div>
                <div class="item">
                    <p>Address (if property)</p>
                    <el-input v-model="asset.address" placeholder="Full property address" />
                    <span class="hint">Complete address if asset is a property</span>
                </div>
                <div class="buttons">
                    <el-button type="danger" @click="$emit('removeAsset', index)" :disabled="ensureAssets(company).length <= 1">Remove</el-button>
                </div>
            </div>
            <div class="add">
                <el-button type="primary" @click="$emit('addAsset', index)">Add Asset</el-button>
            </div>
            <div class="long_item">
                <h1>Financial Summary</h1>
            </div>
            <div class="item">
                <p>Annual Company Income ($) <span class="required">*</span></p>
                <el-input v-model="company.annual_company_income" type="number" placeholder="e.g. 1000000" />
                <span class="hint">Annual company income in dollars (max 10 digits)</span>
            </div>
            <div class="item">
                <p>Total Assets ($)</p>
                <el-input :value="calculateTotalAssets(company)" type="number" disabled />
                <span class="hint">Sum of all assets (calculated automatically)</span>
            </div>
        </div>
    </div>
</template>

<script setup>
    import { computed, watch } from 'vue';

    const props = defineProps({
        company: {
            type: Array,
            default: () => []
        }
    });

    const emit = defineEmits(['addAsset', 'removeAsset', 'addCompany']);

    // Computed property to ensure reactivity and filter out empty companies
    const companyList = computed(() => {
        const companies = props.company || [];
        console.log("CompanyAssets: Raw company data:", companies);
        
        // Simply return all companies - don't filter out empty ones as they may be in the process of being filled
        console.log("CompanyAssets: Using companies:", companies);
        return companies;
    });

    // Watch for changes in the company array
    watch(() => props.company, (newCompany) => {
        console.log("CompanyAssets: Company data changed:", newCompany);
        console.log("CompanyAssets: Company array length:", newCompany?.length || 0);
    }, { deep: true, immediate: true });

    // Watch for changes in company array length
    watch(() => props.company?.length, (newLength, oldLength) => {
        console.log(`CompanyAssets: Company array length changed from ${oldLength} to ${newLength}`);
    });

    // Helper functions to calculate totals
    const calculateTotalAssets = (company) => {
        if (!company?.assets || !Array.isArray(company.assets)) return 0;
        return company.assets.reduce((total, asset) => {
            const value = parseFloat(asset.value) || 0;
            return total + value;
        }, 0);
    };

    // New function to ensure assets are properly initialized
    const ensureAssets = (company) => {
        if (!company?.assets || !Array.isArray(company.assets)) {
            return [];
        }
        return company.assets;
    };
</script>

<style scoped>
    .form {
        display: flex;
        flex-direction: column;
        gap: 20px;
    }
    .no-company {
        text-align: center;
        padding: 40px 20px;
        border: 2px dashed #e1e1e1;
        border-radius: 8px;
        background-color: #fafafa;
    }
    .no-company p {
        color: #666;
        font-size: 0.9rem;
        margin-bottom: 20px;
    }
    .add-company {
        display: flex;
        justify-content: center;
        margin-top: 20px;
    }
    .company {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 15px;
    }
    .company-header {
        grid-column: 1 / 4;
        padding: 15px;
        background-color: #f8f9fa;
        border-radius: 8px;
        margin-bottom: 15px;
        border-left: 4px solid #2984DE;
    }
    .company-header h2 {
        margin: 0;
        color: #2984DE;
        font-size: 1.1rem;
        font-weight: 600;
    }
    .company-header p {
        margin: 5px 0 0 0;
        color: #666;
        font-size: 0.8rem;
    }
    .item {
        display: flex;
        flex-direction: column;
        align-items: start;
        gap: 10px;
    }
    .long_item {
        grid-column: 1 / 4;
        display: flex;
        flex-direction: column;
        align-items: start;
        gap: 10px;
    }
    .asset {
        grid-column: 1 / 4;
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 15px;
        padding: 15px;
        border: 1px solid #e1e1e1;
        border-radius: 5px;
        margin-bottom: 10px;
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
    .buttons {
        display: flex;
        justify-content: flex-end;
        align-items: flex-end;
    }
    .add {
        grid-column: 1 / 4;
        display: flex;
        justify-content: center;
        margin-top: 10px;
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
