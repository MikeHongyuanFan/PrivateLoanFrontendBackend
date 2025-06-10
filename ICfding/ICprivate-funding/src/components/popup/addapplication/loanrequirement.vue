<template>
    <div class="form">
        <div class="long_item">
            <h1>Loan Requirements <span class="required">*</span></h1>
            <span class="hint">Specify the requirements and breakdown of the loan amount</span>
        </div>
        <div v-for="(item, index) in requirement" :key="index" class="requirement">
            <div class="item">
                <p>Description <span class="required">*</span></p>
                <el-input v-model="item.description" placeholder="e.g. Property Purchase, Renovation, Debt Consolidation" />
                <span class="hint">Purpose or description of this portion of the loan</span>
            </div>
            <div class="item">
                <p>Amount ($) <span class="required">*</span></p>
                <el-input v-model="item.amount" type="number" placeholder="e.g. 250000" />
                <span class="hint">Amount in dollars (max 10 digits)</span>
            </div>
            <div class="buttons">
                <el-button type="danger" @click="$emit('remove')" :disabled="requirement.length <= 1">Remove</el-button>
            </div>
        </div>
        <div class="add">
            <el-button type="primary" @click="$emit('add')">Add Requirement</el-button>
        </div>
        <div class="total">
            <p>Total Amount: ${{ totalAmount }}</p>
            <span class="hint">Sum of all loan requirements</span>
        </div>
    </div>
</template>

<script setup>
    import { computed } from 'vue';

    const props = defineProps({
        requirement: Array
    });

    defineEmits(['add', 'remove']);

    const totalAmount = computed(() => {
        return props.requirement
            .map(item => parseFloat(item.amount) || 0)
            .reduce((sum, val) => sum + val, 0)
            .toLocaleString();
    });
</script>

<style scoped>
    .form {
        display: flex;
        flex-direction: column;
        gap: 20px;
    }
    .requirement {
        display: grid;
        grid-template-columns: 2fr 1fr auto;
        gap: 15px;
        padding: 15px;
        border: 1px solid #e1e1e1;
        border-radius: 5px;
        align-items: end;
    }
    .item {
        display: flex;
        flex-direction: column;
        align-items: start;
        gap: 10px;
    }
    .long_item {
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
    }
    .add {
        display: flex;
        justify-content: center;
        margin-top: 10px;
    }
    .total {
        display: flex;
        flex-direction: column;
        align-items: end;
        margin-top: 10px;
        font-weight: bold;
    }
    .total p {
        font-size: 1rem;
        font-weight: 600;
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
