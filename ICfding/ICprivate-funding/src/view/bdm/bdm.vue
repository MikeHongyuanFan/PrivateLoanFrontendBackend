<template>
    <div class="bdm">
        <div class="title">
            <h1>{{ overview.name }}</h1>
            <!-- <h2>{{ bdm.date }}</h2> -->
            <p style="color: #2984DE">BDM ID: {{ bdmId }}</p>
        </div>
        <el-tabs v-model="activeName" class="tabs">
            <el-tab-pane name="1">
                <template #label>
                    <div class="label">Overview</div>
                </template>
                <div class="tab">
                    <div class="info">
                        <p style="color: #7A858E">BDM Name</p>
                        <p class="text">{{ overview.name }}</p>
                    </div>
                    <div class="info">
                        <p style="color: #7A858E">Branch</p>
                        <p class="text">
                            <router-link 
                                v-if="overview.branch?.id" 
                                :to="`/branch/${overview.branch.id}`" 
                                class="branch-link"
                            >
                                {{ overview.branch.name }}
                            </router-link>
                            <span v-else>{{ overview.branch?.name || '-' }}</span>
                        </p>
                    </div>
                    <div class="info" v-if="overview.branch?.address">
                        <p style="color: #7A858E">Branch Address</p>
                        <p class="text">{{ overview.branch.address }}</p>
                    </div>
                    <div class="info">
                        <p style="color: #7A858E">Phone Number</p>
                        <p class="text">{{ overview.phone }}</p>
                    </div>
                    <div class="info">
                        <p style="color: #7A858E">Email Address</p>
                        <p class="text">{{ overview.email }}</p>
                    </div>
                </div>
            </el-tab-pane>
            <el-tab-pane name="2">
                <template #label>
                    <div class="label">Applications</div>
                </template>
                <div class="applications-section">
                    <div v-if="loadingApplications" class="loading">Loading applications...</div>
                    <div v-else-if="!applications || applications.length === 0" class="no-data">No applications found for this BDM</div>
                    <div v-else>
                        <div class="applications-header">
                            <h3>Applications ({{ applications.length }})</h3>
                        </div>
                        <el-table 
                            :data="applications" 
                            style="width: 100%" 
                            class="applications-table" 
                            :key="`bdm-applications-${bdmId}`"
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

const bdm = ref({
    name: "BDM Name",
    date: "Date Create: 2025-12-23 10:13:42"
})
const activeName = ref('1')
const bdmId = route.params.bdmId
const overview = ref({})
const applications = ref([])
const loadingApplications = ref(false)

onMounted(async () => {
    try {
        await getBdm()
    } catch (error) {
        console.error('Error loading BDM data:', error)
    }
})

const getBdm = async () => {
    try {
        const [err, res] = await api.bdm(bdmId)
        if (!err) {
            overview.value = res
            console.log(overview.value);
            await getApplications()
        } else {
            console.log(err)
        }
    } catch (error) {
        console.error('Error in getBdm:', error)
    }
}

const getApplications = async () => {
    try {
        loadingApplications.value = true
        const [err, res] = await api.bdmApplications(bdmId)
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
    if (!amount) return '-'
    return new Intl.NumberFormat('en-AU', {
        style: 'currency',
        currency: 'AUD'
    }).format(amount)
}

const formatDate = (dateString) => {
    if (!dateString) return '-'
    return new Date(dateString).toLocaleDateString('en-AU')
}
</script>

<style scoped>
.bdm {
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
    margin-bottom: 20px;
}

.no-data {
    text-align: center;
    color: #909399;
    margin-bottom: 20px;
}

.applications-header {
    margin-bottom: 20px;
}

.applications-table {
    width: 100%;
}

.app-link {
    color: #409EFF;
    text-decoration: none;
}

.branch-link {
    color: #409EFF;
    text-decoration: none;
}

.branch-link:hover {
    text-decoration: underline;
}
</style>