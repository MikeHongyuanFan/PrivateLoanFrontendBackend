<template>
    <div class="form">
        <div v-for="(item, index) in borrowers" :key="index" class="borrower">
            <div class="item">
                <p>First Name <span class="required">*</span></p>
                <el-input v-model="item.first_name" placeholder="Enter first name" />
                <span class="hint">Legal first name</span>
            </div>
            <div class="item">
                <p>Last Name <span class="required">*</span></p>
                <el-input v-model="item.last_name" placeholder="Enter last name" />
                <span class="hint">Legal last name</span>
            </div>
            <div class="item">
                <p>Email <span class="required">*</span></p>
                <el-input v-model="item.email" type="email" placeholder="example@domain.com" />
                <span class="hint">Valid email address</span>
            </div>
            <div class="item">
                <p>Phone <span class="required">*</span></p>
                <el-input v-model="item.phone" placeholder="e.g. +61 4XX XXX XXX" />
                <span class="hint">Contact phone number</span>
            </div>
            <div class="item">
                <p>Date of Birth <span class="required">*</span></p>
                <el-date-picker 
                    v-model="item.date_of_birth" 
                    type="date" 
                    placeholder="YYYY-MM-DD" 
                    format="YYYY-MM-DD"
                    value-format="YYYY-MM-DD" />
                <span class="hint">Date must be in YYYY-MM-DD format</span>
            </div>
            <div class="item">
                <p>Tax ID (TFN)</p>
                <el-input v-model="item.tax_id" placeholder="e.g. 123 456 789" maxlength="11" />
                <span class="hint">Tax File Number (optional)</span>
            </div>
            <div class="item">
                <p>Marital Status</p>
                <el-select v-model="item.marital_status" placeholder="Select status">
                    <el-option value="single" label="Single" />
                    <el-option value="married" label="Married" />
                    <el-option value="de_facto" label="De Facto" />
                    <el-option value="divorced" label="Divorced" />
                    <el-option value="widowed" label="Widowed" />
                </el-select>
                <span class="hint">Current marital status</span>
            </div>
            <div class="item">
                <p>Residency Status</p>
                <el-select v-model="item.residency_status" placeholder="Select status">
                    <el-option value="citizen" label="Citizen" />
                    <el-option value="permanent_resident" label="Permanent Resident" />
                    <el-option value="temporary_resident" label="Temporary Resident" />
                    <el-option value="foreign_investor" label="Foreign Investor" />
                </el-select>
                <span class="hint">Current Australian residency status</span>
            </div>
            <div class="item">
                <p>Referral Source</p>
                <el-input v-model="item.referral_source" placeholder="How did you hear about us?" />
                <span class="hint">How the borrower was referred</span>
            </div>
            <div class="item">
                <p>Tags</p>
                <el-input v-model="item.tags" placeholder="e.g. VIP, Repeat Customer" />
                <span class="hint">Comma-separated tags for categorization</span>
            </div>
            <div class="buttons">
                <el-button type="danger" @click="$emit('remove', index)" :disabled="borrowers.length <= 1">Remove</el-button>
            </div>
        </div>
        <div class="add">
            <el-button type="primary" @click="$emit('add')">Add Borrower</el-button>
        </div>
    </div>
</template>

<script setup>
    const props = defineProps({
        borrowers: Array
    });

    defineEmits(['add', 'remove']);
</script>

<style scoped>
    .form {
        display: flex;
        flex-direction: column;
        gap: 20px;
    }
    .borrower {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 15px;
        padding: 15px;
        border: 1px solid #e1e1e1;
        border-radius: 5px;
    }
    .item {
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
    .buttons {
        grid-column: 1 / 4;
        display: flex;
        justify-content: flex-end;
        margin-top: 10px;
    }
    .add {
        display: flex;
        justify-content: center;
        margin-top: 10px;
    }
    :deep(.el-date-editor) {
        --el-date-editor-width: 100%;
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
