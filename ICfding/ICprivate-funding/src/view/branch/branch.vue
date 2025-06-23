<template>
    <div class="branch">
        <div class="title">
            <h1>{{ overview.name }}</h1>
            <!-- <h2>{{ overview.date }}</h2> -->
            <p style="color: #2984DE">Branch/Subsidiary ID: {{ branchId }}</p>
        </div>
        <el-tabs v-model="activeName" class="tabs">
            <el-tab-pane name="1">
                <template #label>
                    <div class="label">Overview</div>
                </template>
                <div class="tab">
                    <div class="info">
                        <p style="color: #7A858E">Branch/Subsidiary Name</p>
                        <p class="text">{{ overview.name }}</p>
                    </div>
                    <div class="info">
                        <p style="color: #7A858E">Created At</p>
                        <p class="text">{{ formatDate(overview.created_at) }}</p>
                    </div>
                </div>
            </el-tab-pane>
            <el-tab-pane name="2">
                <template #label>
                    <div class="label">Brokers</div>
                </template>
                <div class="brokers-section">
                    <div v-if="loadingBrokers" class="loading">Loading brokers...</div>
                    <div v-else-if="!brokers || brokers.length === 0" class="no-data">No brokers found for this branch</div>
                    <div v-else>
                        <div class="brokers-header">
                            <h3>Brokers ({{ brokers.length }})</h3>
                        </div>
                        <el-table 
                            :data="brokers" 
                            style="width: 100%" 
                            class="brokers-table"
                            :key="`branch-brokers-${branchId}`"
                            v-loading="loadingBrokers"
                        >
                            <el-table-column prop="name" label="Broker Name" min-width="150">
                                <template #default="scope">
                                    <router-link :to="`/broker/${scope.row.id}`" class="broker-link">
                                        {{ scope.row.name }}
                                    </router-link>
                                </template>
                            </el-table-column>
                            <el-table-column prop="company" label="Company" min-width="150">
                                <template #default="scope">
                                    {{ scope.row.company || '-' }}
                                </template>
                            </el-table-column>
                            <el-table-column prop="email" label="Email" min-width="180">
                                <template #default="scope">
                                    {{ scope.row.email || '-' }}
                                </template>
                            </el-table-column>
                            <el-table-column prop="phone" label="Phone" width="120">
                                <template #default="scope">
                                    {{ scope.row.phone || '-' }}
                                </template>
                            </el-table-column>
                            <el-table-column prop="created_at" label="Created" width="120">
                                <template #default="scope">
                                    {{ formatDate(scope.row.created_at) }}
                                </template>
                            </el-table-column>
                        </el-table>
                    </div>
                </div>
            </el-tab-pane>
            <el-tab-pane name="3">
                <template #label>
                    <div class="label">Applications</div>
                </template>
                <div class="applications-section">
                    <div v-if="loadingApplications" class="loading">Loading applications...</div>
                    <div v-else-if="!applications || applications.length === 0" class="no-data">No applications found for this branch</div>
                    <div v-else>
                        <div class="applications-header">
                            <h3>Applications ({{ applications.length }})</h3>
                        </div>
                        <el-table 
                            :data="applications" 
                            style="width: 100%" 
                            class="applications-table"
                            :key="`branch-applications-${branchId}`"
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
                            <el-table-column label="Broker" min-width="150">
                                <template #default="scope">
                                    {{ scope.row.broker?.name || '-' }}
                                </template>
                            </el-table-column>
                        </el-table>
                    </div>
                </div>
            </el-tab-pane>
        </el-tabs>
    </div>
</template>

<script setup>
import { onMounted, ref } from 'vue';
import { api } from '@/api';
import { useRoute } from 'vue-router';

const route = useRoute()

const branch = ref({
    name: "Branch Name",
    date: "Date Create: 2025-12-23 10:13:42"
})
const activeName = ref('1')
const branchId = route.params.branchId
const overview = ref({
    name: "",
    created_at: ""
})
const applications = ref([])
const loadingApplications = ref(false)
const brokers = ref([])
const loadingBrokers = ref(false)

// Helper function to format dates
const formatDate = (dateString) => {
    if (!dateString) return '-';
    const date = new Date(dateString);
    return date.toLocaleDateString();
}

onMounted(async () => {
    try {
        await getBranch()
    } catch (error) {
        console.error('Error loading branch data:', error)
    }
})

const getBranch = async () => {
    try {
        const [err, res] = await api.branch(branchId)
        if (!err) {
            console.log(res);
            // borrowers.value = res.results
            overview.value = res || {}
            await getBrokers()
            await getApplications()
        } else {
            console.log(err)
        }
    } catch (error) {
        console.error('Error in getBranch:', error)
    }
}

const getBrokers = async () => {
    try {
        loadingBrokers.value = true
        const [err, res] = await api.branchBrokers(branchId)
        if (!err) {
            console.log(res);
            brokers.value = res || []
        } else {
            console.log(err)
            brokers.value = []
        }
    } catch (error) {
        console.error('Error in getBrokers:', error)
        brokers.value = []
    } finally {
        loadingBrokers.value = false
    }
}

const getApplications = async () => {
    try {
        loadingApplications.value = true
        const [err, res] = await api.branchApplications(branchId)
        if (!err) {
            console.log(res);
            // Ensure res is always an array
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
    if (!amount) return '-'
    return new Intl.NumberFormat('en-AU', {
        style: 'currency',
        currency: 'AUD'
    }).format(amount)
}
</script>

<style scoped>
.branch {
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

.brokers-section {
    padding: 20px;
}

.brokers-header {
    margin-bottom: 20px;
}

.brokers-header h3 {
    font-size: 1.25rem;
    font-weight: 700;
    color: #000;
    margin: 0;
}

.brokers-table {
    width: 100%;
}

.broker-link {
    color: #409EFF;
    text-decoration: none;
}

.broker-link:hover {
    text-decoration: underline;
}
</style>