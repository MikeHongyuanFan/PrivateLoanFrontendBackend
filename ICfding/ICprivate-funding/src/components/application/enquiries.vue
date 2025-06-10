<template>
    <div class="content">
        <div class="line">
            <p>Do/es the Borrower(s) and the Guarantor(s) have any pending or past litigation matters (within the last 2 years)?</p>
            <p class="status">{{ status(detail.has_pending_litigation) }}</p>
        </div>
        <div class="line">
            <p>Are there any unsatisfied judgements against the Borrower(s) and the Guarantor(s)?</p>
            <p class="status">{{ status(detail.has_unsatisfied_judgements) }}</p>
        </div>
        <div class="line">
            <p>Have the Borrower(s) and the Guarantor(s) been bankrupt or insolvent in the past 5 years?</p>
            <p class="status">{{ status(detail.has_been_bankrupt) }}</p>
        </div>
        <div class="line">
            <p>Has the Borrower(s) and the Guarantor(s) been refused credit by a credit provider in the last 1 year?</p>
            <p class="status">{{ status(detail.has_been_refused_credit) }}</p>
        </div>
        <div class="line">
            <p>Are there any outstanding debts current or otherwise due to the ATO by the Borrower(s) and the Guarantor(s)?</p>
            <p class="status">{{ status(detail.has_outstanding_ato_debt) }}</p>
        </div>
        <div class="line">
            <p>Does the Borrower(s) and the Guarantor(s) have outstanding Tax or BAS returns due to be lodged with the ATO?</p>
            <p class="status">{{ status(detail.has_outstanding_tax_returns) }}</p>
        </div>
        <div class="line">
            <p>Has the Borrower(s) and the Guarantor(s) made payment arrangements with a creditor to payout debt that is still current?</p>
            <p class="status">{{ status(detail.has_payment_arrangements) }}</p>
        </div>
        <div class="line">
            <p>Solvency Enquiries Details</p>
            <p class="status">{{ detail.solvency_enquiries_details || '-' }}</p>
        </div>
    </div>
</template>

<script setup>
    import { ref } from 'vue';

    const { detail } = defineProps({
        detail: Object
    })

    const status = (st) => {
        if (st === false) {
            return "No"
        } else {
            return "Yes"
        }
    }
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
    .line {
        display: flex;
        flex-direction: column;
        gap: 10px;
    }
    p {
        color: #7A858E;
        font-feature-settings: 'liga' off, 'clig' off;
        font-size: 0.75rem;
        font-style: normal;
        font-weight: 500;
        line-height: 140%;
        margin: 0;
    }
    .status {
        color: #384144;
        font-weight: 600;
    }
</style>