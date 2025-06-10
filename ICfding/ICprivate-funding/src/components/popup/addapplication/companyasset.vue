<template>
    <div class="form">
        <div class="long_item">
            <h1>Company Assets</h1>
        </div>
        <div v-for="(company, index) in company" :key="index" class="company">
            <div class="long_item">
                <h1>Assets</h1>
            </div>
            <div v-for="(asset, idx) in company.assets" :key="idx" class="asset">
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
                        <el-option value="To be refinanced" label="To be refinanced" />
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
                    <el-button type="danger" @click="$emit('removeAsset')" :disabled="company.assets.length <= 1">Remove</el-button>
                </div>
            </div>
            <div class="add">
                <el-button type="primary" @click="$emit('addAsset')">Add Asset</el-button>
            </div>
            <div class="long_item">
                <h1>Liabilities</h1>
            </div>
            <div v-for="(liability, idx) in company.liabilities" :key="idx" class="liability">
                <div class="item">
                    <p>Liability Type <span class="required">*</span></p>
                    <el-select v-model="liability.liability_type" placeholder="Select liability type">
                        <el-option value="mortgage" label="Mortgage" />
                        <el-option value="personal_loan" label="Personal Loan" />
                        <el-option value="car_loan" label="Car Loan" />
                        <el-option value="credit_card" label="Credit Card" />
                        <el-option value="tax_debt" label="Tax Debt" />
                        <el-option value="other_creditor" label="Other Creditor" />
                        <el-option value="other" label="Other" />
                    </el-select>
                    <span class="hint">Type of liability</span>
                </div>
                <div class="item">
                    <p>Description <span class="required">*</span></p>
                    <el-input v-model="liability.description" placeholder="Brief description of the liability" />
                    <span class="hint">Brief description of the liability</span>
                </div>
                <div class="item">
                    <p>Amount ($) <span class="required">*</span></p>
                    <el-input v-model="liability.amount" type="number" placeholder="e.g. 150000" />
                    <span class="hint">Total amount of the liability (max 10 digits)</span>
                </div>
                <div class="item">
                    <p>Lender</p>
                    <el-input v-model="liability.lender" placeholder="Name of the lender" />
                    <span class="hint">Name of the bank or financial institution</span>
                </div>
                <div class="item">
                    <p>Monthly Payment ($)</p>
                    <el-input v-model="liability.monthly_payment" type="number" placeholder="e.g. 1500" />
                    <span class="hint">Monthly repayment amount (max 8 digits)</span>
                </div>
                <div class="item">
                    <p>To Be Refinanced</p>
                    <el-checkbox v-model="liability.to_be_refinanced">Yes</el-checkbox>
                    <span class="hint">Check if this liability will be refinanced</span>
                </div>
                <div class="item">
                    <p>BG Type <span class="required">*</span></p>
                    <el-radio-group v-model="liability.bg_type">
                        <el-radio value="bg1">BG1</el-radio>
                        <el-radio value="bg2">BG2</el-radio>
                    </el-radio-group>
                    <span class="hint">Borrower/Guarantor classification</span>
                </div>
                <div class="buttons">
                    <el-button type="danger" @click="$emit('removeLiability')" :disabled="company.liabilities.length <= 1">Remove</el-button>
                </div>
            </div>
            <div class="add">
                <el-button type="primary" @click="$emit('addLiability')">Add Liability</el-button>
            </div>
            <div class="long_item">
                <h1>Financial Summary</h1>
            </div>
            <div class="item">
                <p>Annual Revenue ($) <span class="required">*</span></p>
                <el-input v-model="company.financial_info.annual_revenue" type="number" placeholder="e.g. 1000000" />
                <span class="hint">Annual revenue in dollars (max 10 digits)</span>
            </div>
            <div class="item">
                <p>Net Profit ($) <span class="required">*</span></p>
                <el-input v-model="company.financial_info.net_profit" type="number" placeholder="e.g. 250000" />
                <span class="hint">Annual net profit in dollars (max 10 digits)</span>
            </div>
            <div class="item">
                <p>Total Assets ($)</p>
                <el-input v-model="company.financial_info.assets" type="number" disabled />
                <span class="hint">Sum of all assets (calculated automatically)</span>
            </div>
            <div class="item">
                <p>Total Liabilities ($)</p>
                <el-input v-model="company.financial_info.liabilities" type="number" disabled />
                <span class="hint">Sum of all liabilities (calculated automatically)</span>
            </div>
        </div>
    </div>
</template>

<script setup>
    const props = defineProps({
        company: Array
    });

    defineEmits(['addAsset', 'removeAsset', 'addLiability', 'removeLiability']);
</script>

<style scoped>
    .form {
        display: flex;
        flex-direction: column;
        gap: 20px;
    }
    .company {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 15px;
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
    .asset, .liability {
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
