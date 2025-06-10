<template>
    <div class="content">
        <div class="form">
            <div class="item">
                <p class="title">Company Name</p>
                <p>{{ detail.company_name || '-' }}</p>
            </div>
            <div class="item">
                <p class="title">ABN</p>
                <p>{{ detail.company_abn || '-' }}</p>
            </div>
            <div class="item">
                <p class="title">ACN</p>
                <p>{{ detail.company_acn || '-' }}</p>
            </div>
            <div class="item">
                <p class="title">Industry Type</p>
                <p>{{ detail.industry_type || '-' }}</p>
            </div>
            <div class="item">
                <p class="title">Contact Number</p>
                <p>{{ detail.contact_number || '-' }}</p>
            </div>
            <div class="item">
                <p class="title">Annual Company Income</p>
                <p>{{ formatCurrency(detail.annual_company_income) }}</p>
            </div>
            <div class="item">
                <p class="title">Is the company a Trustee?</p>
                <p>{{ status(detail.is_trustee) }}</p>
            </div>
            <div class="item">
                <p class="title">Is the company a Trustee for an SMSF?</p>
                <p>{{ status(detail.is_smsf_trustee) }}</p>
            </div>
            <div class="item">
                <p class="title">Trustee Name</p>
                <p>{{ detail.trustee_name || '-' }}</p>
            </div>
        </div>
        <div class="part"><h1>Position Held</h1></div>
        <div class="form">
            <div class="item">
                <p class="title">Name</p>
                <p>{{ detail.name1 || '-' }}</p>
            </div>
            <div class="item">
                <p class="title">Position</p>
                <p>{{ detail.position1 || '-' }}</p>
            </div>
            <div class="item">
                <p class="title">Director ID</p>
                <p>{{ detail.id1 || '-' }}</p>
            </div>
            <div class="item">
                <p class="title">Name</p>
                <p>{{ detail.name2 || '-' }}</p>
            </div>
            <div class="item">
                <p class="title">Position</p>
                <p>{{ detail.position2 || '-' }}</p>
            </div>
            <div class="item">
                <p class="title">Director ID</p>
                <p>{{ detail.id2 || '-' }}</p>
            </div>
        </div>
        <div class="part"><h1>Registered Address</h1></div>
        <div class="item">
            <p class="title">Full Address</p>
            <p>{{ formatAddress(detail) || '-' }}</p>
        </div>
    </div>
</template>

<script setup>
    const { detail } = defineProps({
        detail: {
            type: Object,
            required: true,
            default: () => ({})
        }
    })

    const status = (st) => {
        if (st === true) {
            return "Yes"
        } else {
            return "No"
        }
    }

    const formatCurrency = (value) => {
        if (!value) return '-'
        return new Intl.NumberFormat('en-AU', {
            style: 'currency',
            currency: 'AUD'
        }).format(value)
    }

    const formatAddress = (detail) => {
        if (!detail) return '-'
        const parts = [
            detail.registered_address_unit,
            detail.registered_address_street_no,
            detail.registered_address_street_name,
            detail.registered_address_suburb
        ]
        return parts.filter(Boolean).join(' ')
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
    .part {
        padding: 20px 0;
        border-top: 1.5px solid #E8EBEE;
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