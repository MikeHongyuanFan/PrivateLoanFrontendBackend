<template>
    <div class="form">
        <div class="long_item">
            <h1>General Solvency Enquiries <span class="required">*</span></h1>
            <span class="hint">Information about the financial standing of borrowers and guarantors</span>
        </div>
        <div class="enquiry">
            <p>Do the Borrower(s) and the Guarantor(s) have any pending or past litigation matters (within the last 2 years)? <span class="required">*</span></p>
            <el-radio-group v-model="enquiry.has_pending_litigation">
                <el-radio :value="true">Yes</el-radio>
                <el-radio :value="false">No</el-radio>
            </el-radio-group>
            <span class="hint">Select Yes if there are any pending or past litigation matters</span>
        </div>
        <div class="enquiry">
            <p>Are there any unsatisfied judgements against the Borrower(s) and the Guarantor(s)? <span class="required">*</span></p>
            <el-radio-group v-model="enquiry.has_unsatisfied_judgements">
                <el-radio :value="true">Yes</el-radio>
                <el-radio :value="false">No</el-radio>
            </el-radio-group>
            <span class="hint">Select Yes if there are any unsatisfied judgements</span>
        </div>
        <div class="enquiry">
            <p>Have the Borrower(s) and the Guarantor(s) been bankrupt or insolvent in the past 5 years? <span class="required">*</span></p>
            <el-radio-group v-model="enquiry.has_been_bankrupt">
                <el-radio :value="true">Yes</el-radio>
                <el-radio :value="false">No</el-radio>
            </el-radio-group>
            <span class="hint">Select Yes if there has been bankruptcy or insolvency</span>
        </div>
        <div class="enquiry">
            <p>Has the Borrower(s) and the Guarantor(s) been refused credit by a credit provider in the last 1 year? <span class="required">*</span></p>
            <el-radio-group v-model="enquiry.has_been_refused_credit">
                <el-radio :value="true">Yes</el-radio>
                <el-radio :value="false">No</el-radio>
            </el-radio-group>
            <span class="hint">Select Yes if credit has been refused in the last year</span>
        </div>
        <div class="enquiry">
            <p>Are there any outstanding debts current or otherwise due to the ATO by the Borrower(s) and the Guarantor(s)? <span class="required">*</span></p>
            <el-radio-group v-model="enquiry.has_outstanding_ato_debt">
                <el-radio :value="true">Yes</el-radio>
                <el-radio :value="false">No</el-radio>
            </el-radio-group>
            <span class="hint">Select Yes if there are outstanding ATO debts</span>
        </div>
        <div class="enquiry">
            <p>Does the Borrower(s) and the Guarantor(s) have outstanding Tax or BAS returns due to be lodged with the ATO? <span class="required">*</span></p>
            <el-radio-group v-model="enquiry.has_outstanding_tax_returns">
                <el-radio :value="true">Yes</el-radio>
                <el-radio :value="false">No</el-radio>
            </el-radio-group>
            <span class="hint">Select Yes if there are outstanding tax returns</span>
        </div>
        <div class="enquiry">
            <p>Has the Borrower(s) and the Guarantor(s) made payment arrangements with a creditor to payout debt that is still current? <span class="required">*</span></p>
            <el-radio-group v-model="enquiry.has_payment_arrangements">
                <el-radio :value="true">Yes</el-radio>
                <el-radio :value="false">No</el-radio>
            </el-radio-group>
            <span class="hint">Select Yes if there are current payment arrangements</span>
        </div>
        <div class="long_item">
            <p>Additional Details</p>
            <el-input 
                v-model="enquiry.solvency_enquiries_details" 
                type="textarea" 
                :rows="4" 
                placeholder="Please provide details for any 'Yes' answers above"
                :disabled="!hasAnyYesAnswers" />
            <span class="hint">Required if any question above is answered 'Yes'</span>
        </div>
    </div>
</template>

<script setup>
    import { computed, onMounted } from 'vue';

    const props = defineProps({
        enquiry: Object
    });

    // Initialize default values
    onMounted(() => {
        // Set default values to false if null
        if (props.enquiry.has_pending_litigation === null) props.enquiry.has_pending_litigation = false;
        if (props.enquiry.has_unsatisfied_judgements === null) props.enquiry.has_unsatisfied_judgements = false;
        if (props.enquiry.has_been_bankrupt === null) props.enquiry.has_been_bankrupt = false;
        if (props.enquiry.has_been_refused_credit === null) props.enquiry.has_been_refused_credit = false;
        if (props.enquiry.has_outstanding_ato_debt === null) props.enquiry.has_outstanding_ato_debt = false;
        if (props.enquiry.has_outstanding_tax_returns === null) props.enquiry.has_outstanding_tax_returns = false;
        if (props.enquiry.has_payment_arrangements === null) props.enquiry.has_payment_arrangements = false;
    });

    // Check if any question has a "Yes" answer
    const hasAnyYesAnswers = computed(() => {
        return props.enquiry.has_pending_litigation === true ||
               props.enquiry.has_unsatisfied_judgements === true ||
               props.enquiry.has_been_bankrupt === true ||
               props.enquiry.has_been_refused_credit === true ||
               props.enquiry.has_outstanding_ato_debt === true ||
               props.enquiry.has_outstanding_tax_returns === true ||
               props.enquiry.has_payment_arrangements === true;
    });
</script>

<style scoped>
    .form {
        display: flex;
        flex-direction: column;
        gap: 20px;
    }
    .long_item {
        display: flex;
        flex-direction: column;
        align-items: start;
        gap: 10px;
    }
    .enquiry {
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
        line-height: 16px;
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
