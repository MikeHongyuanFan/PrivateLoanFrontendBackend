<template>
    <div class="content">
        <div class="form">
            <div class="item">
                <p class="title">Net Loan Required ($)</p>
                <p>{{ detail.loan_amount || '-' }}</p>
            </div>
            <div class="item">
                <p class="title">Term Required (Month)</p>
                <p>{{ detail.loan_term || '-' }}</p>
            </div>
            <div class="item">
                <p class="title">Proposed Settlement Date</p>
                <p>{{ detail.estimated_settlement_date || '-' }}</p>
            </div>
            <div class="item">
                <p class="title">Expected Rate (p.a) (%)</p>
                <p>{{ detail.interest_rate || '-' }}</p>
            </div>
            <div class="item">
                <p class="title">Loan Purpose</p>
                <p>{{ detail.loan_purpose || '-' }}</p>
            </div>
            <div class="item">
                <p class="title">Additional Comments</p>
                <p>{{ detail.additional_comments || '-' }}</p>
            </div>
        </div>
    </div>
</template>

<script setup>
    import { ref } from 'vue';

    const { detail } = defineProps({
        detail: Object
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
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 20px;
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
    }
</style>