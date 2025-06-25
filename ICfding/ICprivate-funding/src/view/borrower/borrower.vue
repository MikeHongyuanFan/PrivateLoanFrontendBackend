<template>
    <div class="borrower">
        <div class="title">
            <h1>{{ borrowers.first_name }} {{ borrowers.last_name }}</h1>
            <h2>Date Created: {{ borrowers.created_at?.split('T')[0] }}</h2>
            <p style="color: #2984DE">Borrower ID: {{ borrowerId }}</p>
        </div>
        <el-tabs v-model="activeName" class="tabs" >
            <el-tab-pane name="1">
                <template #label>
                    <div class="label">Personal Information</div>
                </template>
                <div class="tab">
                    <div class="info">
                        <p style="color: #7A858E">Title</p>
                        <p class="text">{{ formatTitle(borrowers.title) }}</p>
                    </div>
                    <div class="info">
                        <p style="color: #7A858E">Contact Name</p>
                        <p class="text">{{ borrowers.first_name }} {{ borrowers.last_name }}</p>
                    </div>
                    <div class="info">
                        <p style="color: #7A858E">Borrower Type</p>
                        <p class="text">{{ type }}</p>
                    </div>
                    <div class="info">
                        <p style="color: #7A858E">Email</p>
                        <p class="text">{{ borrowers.email || '-' }}</p>
                    </div>
                    <div class="info">
                        <p style="color: #7A858E">Home Phone</p>
                        <p class="text">{{ borrowers.home_phone || '-' }}</p>
                    </div>
                    <div class="info">
                        <p style="color: #7A858E">Mobile Phone</p>
                        <p class="text">{{ borrowers.mobile || '-' }}</p>
                    </div>
                    <div class="info">
                        <p style="color: #7A858E">Date of Birth</p>
                        <p class="text">{{ borrowers.date_of_birth || '-' }}</p>
                    </div>
                    <div class="info">
                        <p style="color: #7A858E">Driver's License Number</p>
                        <p class="text">{{ borrowers.drivers_licence_no || '-' }}</p>
                    </div>
                    <div class="info">
                        <p style="color: #7A858E">Tax ID (TFN)</p>
                        <p class="text">{{ borrowers.tax_id || '-' }}</p>
                    </div>
                    <div class="info">
                        <p style="color: #7A858E">Marital Status</p>
                        <p class="text">{{ formatMaritalStatus(borrowers.marital_status) }}</p>
                    </div>
                    <div class="info">
                        <p style="color: #7A858E">Residency Status</p>
                        <p class="text">{{ formatResidencyStatus(borrowers.residency_status) }}</p>
                    </div>
                    <div class="info">
                        <p style="color: #7A858E">Referral Source</p>
                        <p class="text">{{ borrowers.referral_source || '-' }}</p>
                    </div>
                    <div class="info">
                        <p style="color: #7A858E">Tags</p>
                        <p class="text">{{ borrowers.tags || '-' }}</p>
                    </div>
                </div>
            </el-tab-pane>
            <el-tab-pane name="2">
                <template #label>
                    <div class="label">Residential Address</div>
                </template>
                <div class="tab">
                    <div class="info">
                        <p style="color: #7A858E">Unit Number</p>
                        <p class="text">{{ borrowers.address_unit || '-' }}</p>
                    </div>
                    <div class="info">
                        <p style="color: #7A858E">Street Number</p>
                        <p class="text">{{ borrowers.address_street_no || '-' }}</p>
                    </div>
                    <div class="info">
                        <p style="color: #7A858E">Street Name</p>
                        <p class="text">{{ borrowers.address_street_name || '-' }}</p>
                    </div>
                    <div class="info">
                        <p style="color: #7A858E">Suburb</p>
                        <p class="text">{{ borrowers.address_suburb || '-' }}</p>
                    </div>
                    <div class="info">
                        <p style="color: #7A858E">State</p>
                        <p class="text">{{ borrowers.address_state || '-' }}</p>
                    </div>
                    <div class="info">
                        <p style="color: #7A858E">Postcode</p>
                        <p class="text">{{ borrowers.address_postcode || '-' }}</p>
                    </div>
                    <div class="info">
                        <p style="color: #7A858E">Full Address</p>
                        <p class="text">{{ formatFullAddress(borrowers) }}</p>
                    </div>
                </div>
            </el-tab-pane>
            <el-tab-pane name="3">
                <template #label>
                    <div class="label">Employment Information</div>
                </template>
                <div class="tab">
                    <div class="info">
                        <p style="color: #7A858E">Occupation</p>
                        <p class="text">{{ borrowers.occupation || '-' }}</p>
                    </div>
                    <div class="info">
                        <p style="color: #7A858E">Employment Type</p>
                        <p class="text">{{ formatEmploymentType(borrowers.employment_type) }}</p>
                    </div>
                    <div class="info">
                        <p style="color: #7A858E">Employer Name</p>
                        <p class="text">{{ borrowers.employer_name || '-' }}</p>
                    </div>
                    <div class="info">
                        <p style="color: #7A858E">Annual Income</p>
                        <p class="text">{{ formatCurrency(borrowers.annual_income) }}</p>
                    </div>
                </div>
            </el-tab-pane>
            <el-tab-pane name="4">
                <template #label>
                    <div class="label">Legacy Information</div>
                </template>
                <div class="tab">
                    <div class="info">
                        <p style="color: #7A858E">Legacy Phone</p>
                        <p class="text">{{ borrowers.phone || '-' }}</p>
                    </div>
                    <div class="info">
                        <p style="color: #7A858E">Legacy Residential Address</p>
                        <p class="text">{{ borrowers.residential_address || '-' }}</p>
                    </div>
                    <div class="info">
                        <p style="color: #7A858E">Legacy Mailing Address</p>
                        <p class="text">{{ borrowers.mailing_address || '-' }}</p>
                    </div>
                    <div class="info">
                        <p style="color: #7A858E">Legacy Job Title</p>
                        <p class="text">{{ borrowers.job_title || '-' }}</p>
                    </div>
                    <div class="info">
                        <p style="color: #7A858E">Legacy Employment Duration</p>
                        <p class="text">{{ borrowers.employment_duration ? `${borrowers.employment_duration} months` : '-' }}</p>
                    </div>
                    <div class="info">
                        <p style="color: #7A858E">Legacy Employer Address</p>
                        <p class="text">{{ borrowers.employer_address || '-' }}</p>
                    </div>
                    <div class="info">
                        <p style="color: #7A858E">Legacy Other Income</p>
                        <p class="text">{{ formatCurrency(borrowers.other_income) }}</p>
                    </div>
                    <div class="info">
                        <p style="color: #7A858E">Legacy Monthly Expenses</p>
                        <p class="text">{{ formatCurrency(borrowers.monthly_expenses) }}</p>
                    </div>
                    <div class="info">
                        <p style="color: #7A858E">Legacy Credit Score</p>
                        <p class="text">{{ borrowers.credit_score || '-' }}</p>
                    </div>
                </div>
            </el-tab-pane>
        </el-tabs>
    </div>
</template>

<script setup>
    import { onMounted, ref, computed } from 'vue';
    import { api } from '@/api';
    import { useRoute } from 'vue-router';

    const route = useRoute()

    const borrowers = ref({})
    const activeName = ref('1')
    const borrowerId = route.params.borrowerId

    onMounted(() => {
        getBorrower()
    })

    const getBorrower = async () => {
        const [err, res] = await api.borrower(borrowerId)
        if (!err) {
            console.log(res);
            borrowers.value = res
        } else {
            console.log(err)
        }
    }
    
    const type = computed(() => {
        if (borrowers.value.is_company === true) {
            return 'Company'
        } else {
            return 'Individual'
        }
    })

    // Formatting functions
    const formatTitle = (title) => {
        if (!title) return '-';
        const titleMap = {
            'mr': 'Mr',
            'mrs': 'Mrs',
            'ms': 'Ms',
            'miss': 'Miss',
            'dr': 'Dr',
            'other': 'Other'
        };
        return titleMap[title] || title;
    }

    const formatMaritalStatus = (status) => {
        if (!status) return '-';
        const statusMap = {
            'single': 'Single',
            'married': 'Married',
            'de_facto': 'De Facto',
            'divorced': 'Divorced',
            'widowed': 'Widowed'
        };
        return statusMap[status] || status;
    }

    const formatResidencyStatus = (status) => {
        if (!status) return '-';
        const statusMap = {
            'citizen': 'Citizen',
            'permanent_resident': 'Permanent Resident',
            'temporary_resident': 'Temporary Resident',
            'foreign_investor': 'Foreign Investor'
        };
        return statusMap[status] || status;
    }

    const formatEmploymentType = (type) => {
        if (!type) return '-';
        const typeMap = {
            'full_time': 'Full Time',
            'part_time': 'Part Time',
            'casual': 'Casual',
            'self_employed': 'Self Employed',
            'contractor': 'Contractor',
            'unemployed': 'Unemployed',
            'retired': 'Retired'
        };
        return typeMap[type] || type;
    }

    const formatCurrency = (amount) => {
        if (!amount || isNaN(amount)) return '-';
        return new Intl.NumberFormat('en-AU', {
            style: 'currency',
            currency: 'AUD'
        }).format(amount);
    }

    const formatFullAddress = (borrower) => {
        const parts = [];
        if (borrower.address_unit) parts.push(borrower.address_unit);
        if (borrower.address_street_no) parts.push(borrower.address_street_no);
        if (borrower.address_street_name) parts.push(borrower.address_street_name);
        if (borrower.address_suburb) parts.push(borrower.address_suburb);
        if (borrower.address_state) parts.push(borrower.address_state);
        if (borrower.address_postcode) parts.push(borrower.address_postcode);
        
        return parts.length > 0 ? parts.join(' ') : '-';
    }
</script>

<style scoped>
    .borrower {
        min-height: 70vh;
        padding: 20px;
        border-radius: 6px;
        background: #FFF;
        display: flex;
        flex-direction: column;
        align-items: start;
        gap: 20px;
    }
    .title {
        display: flex;
        flex-direction: column;
        gap: 15px;
    }
    h1 {
        color: #000;
        font-feature-settings: 'liga' off, 'clig' off;
        font-size: 1.5rem;
        font-style: normal;
        font-weight: 700;
        line-height: 12px;
    }
    h2 {
        color: #939393;
        font-feature-settings: 'liga' off, 'clig' off;
        font-size: 0.9rem;
        font-style: normal;
        font-weight: 400;
        line-height: 12px;
        margin: 0;
    }
    p {
        font-feature-settings: 'liga' off, 'clig' off;
        font-size: 0.75rem;
        font-style: normal;
        font-weight: 600;
        line-height: 140%;
        margin: 0;
    }
    .tabs {
        width: 100%;
        --el-color-primary: #384144;
    }
    .label {
        padding: 0 20px;
        color: #949494;
        font-feature-settings: 'liga' off, 'clig' off;
        font-size: 0.9rem;
        font-style: normal;
        font-weight: 400;
        line-height: 12px;
    }
    .tabs :deep(.el-tabs__item) {
        padding: 0;
    }
    .tabs :deep(.el-tabs__item.is-active .label) {
        color: #384144;
    }
    .tab {
        padding: 20px;
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 20px;
    }
    .info {
        display: flex;
        flex-direction: column;
        align-items: start;
        gap: 10px;
    }
    .text {
        font-family: Inter;
        font-weight: 600;
        font-size: 12px;
        line-height: 100%;
        letter-spacing: 0px;
        color: #000000;
    }
</style>