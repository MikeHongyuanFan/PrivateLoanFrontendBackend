<template>
    <div class="broker">
        <div class="title">
            <h1>{{ brokers?.name || '' }}</h1>
            <h2>{{ brokers?.created_at || '' }}</h2>
            <p style="color: #2984DE">Broker ID: {{ brokerId }}</p>
        </div>
        <el-tabs v-model="activeName" class="tabs">
            <el-tab-pane name="1">
                <template #label>
                    <div class="label">Overview</div>
                </template>
                <div class="tab">
                    <div class="info">
                        <p style="color: #7A858E">Contact Name</p>
                        <p class="text">{{ brokers.name }}</p>
                    </div>
                    <div class="info">
                        <p style="color: #7A858E">Broker ID</p>
                        <p class="text">{{ brokers.id }}</p>
                    </div>
                    <div class="info">
                        <p style="color: #7A858E">Company</p>
                        <p class="text">{{ brokers.company }}</p>
                    </div>
                    <div class="info">
                        <p style="color: #7A858E">Email</p>
                        <p class="text">{{ brokers.email }}</p>
                    </div>
                    <div class="info">
                        <p style="color: #7A858E">Branch</p>
                        <p class="text">
                            <router-link 
                                v-if="brokers.branch?.id" 
                                :to="`/branch/${brokers.branch.id}`" 
                                class="branch-link"
                            >
                                {{ brokers.branch.name }}
                            </router-link>
                            <span v-else>{{ brokers.branch?.name || '-' }}</span>
                        </p>
                    </div>
                    <div class="info" v-if="brokers.branch?.address">
                        <p style="color: #7A858E">Branch Address</p>
                        <p class="text">{{ brokers.branch.address }}</p>
                    </div>
                    <div class="info">
                        <p style="color: #7A858E">Phone</p>
                        <p class="text">{{ brokers.phone || '-' }}</p>
                    </div>
                    <div class="info">
                        <p style="color: #7A858E">Address</p>
                        <p class="text">{{ brokers.address || '-' }}</p>
                    </div>
                    <div class="info">
                        <p style="color: #7A858E">BD</p>
                        <div class="text">
                            <template v-if="brokers.bdms && brokers.bdms.length > 0">
                                <router-link 
                                    v-for="(bdm, index) in brokers.bdms" 
                                    :key="bdm.id"
                                    :to="`/bdm/${bdm.id}`" 
                                    class="bdm-link"
                                >
                                    {{ bdm.display_name || bdm.name }}
                                    <span v-if="index < brokers.bdms.length - 1">, </span>
                                </router-link>
                            </template>
                            <span v-else>-</span>
                        </div>
                    </div>
                </div>
            </el-tab-pane>
            <el-tab-pane name="2">
                <template #label>
                    <div class="label">Commission Account</div>
                </template>
                <div class="tab">
                    <div class="info">
                        <p style="color: #7A858E">Bank Name</p>
                        <p class="text">{{ brokers.commission_bank_name || '-' }}</p>
                    </div>
                    <div class="info">
                        <p style="color: #7A858E">Bank Account Name</p>
                        <p class="text">{{ brokers.commission_account_name || '-' }}</p>
                    </div>
                    <div class="info">
                        <p style="color: #7A858E">BSB</p>
                        <p class="text">{{ brokers.commission_bsb || '-' }}</p>
                    </div>
                    <div class="info">
                        <p style="color: #7A858E">Account No.</p>
                        <p class="text">{{ brokers.commission_account_number || '-' }}</p>
                    </div>
                    <div class="info">
                        <p style="color: #7A858E">Contact Name for Commission</p>
                        <p class="text">{{ brokers.name }}</p>
                    </div>
                    <div class="info">
                        <p style="color: #7A858E">Email for Commission</p>
                        <p class="text">{{ brokers.email }}</p>
                    </div>
                    <div v-if="brokers.commission_account_locked" class="info commission-lock-info">
                        <p style="color: #7A858E">Commission Account Status</p>
                        <div class="text">
                            <el-tag type="warning" size="small">Locked</el-tag>
                            <p style="color: #909399; font-size: 0.7rem; margin-top: 5px;">
                                Locked by: {{ brokers.commission_account_locked_by?.email || 'Unknown' }}<br>
                                Locked at: {{ formatDate(brokers.commission_account_locked_at) }}
                            </p>
                        </div>
                    </div>
                </div>
            </el-tab-pane>
            <el-tab-pane name="3">
                <template #label>
                    <div class="label">Applications</div>
                </template>
                <div class="applications-section">
                    <div v-if="loadingApplications" class="loading">Loading applications...</div>
                    <div v-else-if="!applications || applications.length === 0" class="no-data">No applications found for this broker</div>
                    <div v-else>
                        <div class="applications-header">
                            <h3>Applications ({{ applications.length }})</h3>
                        </div>
                        <el-table 
                            :data="applications" 
                            style="width: 100%" 
                            class="applications-table"
                            :key="`broker-applications-${brokerId}`"
                            v-loading="loadingApplications"
                        >
                            <el-table-column prop="reference_number" label="Reference Number" width="150">
                                <template #default="scope">
                                    <router-link :to="`/application/${scope.row.id}`" class="app-link">
                                        {{ scope.row.reference_number }}
                                    </router-link>
                                </template>
                            </el-table-column>
                            <el-table-column prop="stage" label="Stage" width="120">
                                <template #default="scope">
                                    <el-tag :type="getStageTagType(scope.row.stage)" size="small">
                                        {{ scope.row.stage_display || scope.row.stage }}
                                    </el-tag>
                                </template>
                            </el-table-column>
                            <el-table-column prop="loan_amount" label="Loan Amount" width="120">
                                <template #default="scope">
                                    {{ formatCurrency(scope.row.loan_amount) }}
                                </template>
                            </el-table-column>
                            <el-table-column prop="application_type" label="Type" width="120">
                                <template #default="scope">
                                    {{ scope.row.application_type || '-' }}
                                </template>
                            </el-table-column>
                            <el-table-column prop="created_at" label="Created" width="120">
                                <template #default="scope">
                                    {{ formatDate(scope.row.created_at) }}
                                </template>
                            </el-table-column>
                            <el-table-column label="Primary Borrower" min-width="150">
                                <template #default="scope">
                                    {{ getPrimaryBorrowerName(scope.row.borrowers) }}
                                </template>
                            </el-table-column>
                        </el-table>
                    </div>
                </div>
            </el-tab-pane>
            <el-tab-pane name="4">
                <template #label>
                    <div class="label">Borrowers</div>
                </template>
                Borrowers
            </el-tab-pane>
        </el-tabs>
    </div>
</template>

<script setup>
import { onMounted, ref } from 'vue';
import { api } from '@/api';
import { useRoute } from 'vue-router';

const route = useRoute()

const broker = ref({
    name: "Broker Name",
    date: "Date Create: 2025-12-23 10:13:42"
})
const activeName = ref('1')
const brokerId = route.params.brokerId
const overview = ref({
    name: "Broker One",
    id: "16786541",
    company: "Company Name",
    email: "broker@gmail.com",
    branch: "Branch Name",
    bd: "BD Name"
})
const account = ref({
    bank: "Commonwealth Bank",
    accountName: "Broker Name",
    bsb: "062124",
    account: "15254523",
    contact: "Name",
    email: "broker@gmail.com"
})

const brokers = ref({})
const applications = ref([])
const loadingApplications = ref(false)

onMounted(async () => {
    try {
        await getBroker()
    } catch (error) {
        console.error('Error loading broker data:', error)
    }
})

const getBroker = async () => {
    try {
        const [err, res] = await api.broker(brokerId)
        if (!err) {
            console.log(res);
            brokers.value = res
            await getApplications()
        } else {
            console.log(err)
        }
    } catch (error) {
        console.error('Error in getBroker:', error)
    }
}

const getApplications = async () => {
    try {
        loadingApplications.value = true
        const [err, res] = await api.brokerApplications(brokerId)
        if (!err) {
            console.log(res);
            applications.value = Array.isArray(res) ? res : []
        } else {
            console.log(err)
            applications.value = []
        }
    } catch (error) {
        console.error('Error in getApplications:', error)
        applications.value = []
    } finally {
        loadingApplications.value = false
    }
}

const getStageTagType = (stage) => {
    // Define tag types based on stage
    const stageTypes = {
        'inquiry': 'info',
        'sent_to_lender': 'primary',
        'funding_table_issued': 'primary',
        'iloo_issued': 'warning',
        'iloo_signed': 'warning',
        'formal_approval': 'success',
        'settled': 'success',
        'declined': 'danger',
        'withdrawn': 'danger'
    }
    return stageTypes[stage] || 'info'
}

const formatCurrency = (amount) => {
    if (!amount || isNaN(amount)) return '-'
    return new Intl.NumberFormat('en-AU', {
        style: 'currency',
        currency: 'AUD'
    }).format(amount)
}

const formatDate = (dateString) => {
    if (!dateString) return '-'
    try {
        return new Date(dateString).toLocaleDateString('en-AU')
    } catch (error) {
        return '-'
    }
}

const getPrimaryBorrowerName = (borrowers) => {
    if (!borrowers || !Array.isArray(borrowers) || borrowers.length === 0) {
        return '-'
    }
    const primaryBorrower = borrowers.find(b => b.is_primary) || borrowers[0]
    return primaryBorrower?.first_name && primaryBorrower?.last_name 
        ? `${primaryBorrower.first_name} ${primaryBorrower.last_name}`
        : primaryBorrower?.name || '-'
}
</script>

<style scoped>
.broker {
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

.applications-section {
    padding: 20px;
}

.loading {
    text-align: center;
    color: #909399;
    font-size: 0.875rem;
    margin-bottom: 20px;
}

.no-data {
    text-align: center;
    color: #909399;
    font-size: 0.875rem;
    margin-bottom: 20px;
}

.applications-header {
    margin-bottom: 20px;
}

.applications-header h3 {
    font-size: 1.25rem;
    font-weight: 700;
    color: #000;
    margin: 0;
}

.applications-table {
    width: 100%;
}

.app-link {
    color: #409EFF;
    text-decoration: none;
}

.app-link:hover {
    text-decoration: underline;
}

.branch-link {
    color: #409EFF;
    text-decoration: none;
}

.branch-link:hover {
    text-decoration: underline;
}

.bdm-link {
    color: #409EFF;
    text-decoration: none;
}

.bdm-link:hover {
    text-decoration: underline;
}

.commission-lock-info {
    padding: 10px;
    background-color: #FFF;
    border-radius: 4px;
    border: 1px solid #E4E7ED;
}
</style>