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
                        <p class="text">{{ brokers.branch?.name || '-' }}</p>
                    </div>
                    <div class="info">
                        <p style="color: #7A858E">BD</p>
                        <p class="text">{{ brokers.bdms }}</p>
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
                        <p class="text">{{ brokers.commission_bank_name }}</p>
                    </div>
                    <div class="info">
                        <p style="color: #7A858E">Bank Account Name</p>
                        <p class="text">{{ brokers.commission_account_name }}</p>
                    </div>
                    <div class="info">
                        <p style="color: #7A858E">BSB</p>
                        <p class="text">{{ brokers.commission_bsb }}</p>
                    </div>
                    <div class="info">
                        <p style="color: #7A858E">Account No.</p>
                        <p class="text">{{ brokers.commission_account_number }}</p>
                    </div>
                    <div class="info">
                        <p style="color: #7A858E">Contact Name for Commission</p>
                        <p class="text">{{ brokers.name }}</p>
                    </div>
                    <div class="info">
                        <p style="color: #7A858E">Email for Commission</p>
                        <p class="text">{{ brokers.email }}</p>
                    </div>
                </div>
            </el-tab-pane>
            <el-tab-pane name="3">
                <template #label>
                    <div class="label">Applications</div>
                </template>
                Application
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

onMounted(() => {
    getBroker()
})

const getBroker = async () => {
    const [err, res] = await api.broker(brokerId)
    if (!err) {
        console.log(res);
        brokers.value = res
    } else {
        console.log(err)
    }
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
</style>