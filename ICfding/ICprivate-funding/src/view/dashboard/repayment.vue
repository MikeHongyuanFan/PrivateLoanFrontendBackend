<script setup>
import { ref, onMounted, computed } from 'vue';
import { api } from '@/api';
import Calendar from '@/components/icons/calendar.vue';
import Search from '@/components/buttons/search.vue';
import Clear from '@/components/buttons/clear.vue';
import Create from '@/components/buttons/create.vue'
import AddRepayment from '@/components/popup/addrepayment.vue';
import { Pagination } from '@/components'
import { RepaymentTable } from './components'
import { ElMessage } from 'element-plus';

const action = ref("Add Repayment")
const popup = ref(false)
const repayments = ref([])
const repayment = ref({})
const loading = ref(false)
const totalInfo = computed(() =>[
    {
        title: "Total Repayment",
        money: repayment.value.total_amount_due,
        num: repayment.value.total_repayments
    },
    {
        title: "Paid on Time",
        money: repayment.value.total_amount_paid,
        num: repayment.value.paid_on_time
    },
    {
        title: "Paid Late",
        money: "-",
        num: repayment.value.paid_late
    },
    {
        title: "Overdue",
        money: repayment.value.total_amount_due - repayment.value.total_amount_paid,
        num: repayment.value.missed
    }
])
const searchedRepayment = ref("")
// const statuses = ref([
//     { value: "scheduled", label: "Scheduled" },
//     { value: "dueSoon", label: "Due Soon" },
//     { value: "paid", label: "Paid" },
//     { value: "overdue", label: "Overdue" }
// ])
const paginationInfo = ref({
    total: 10,
})
const popupAction = ref("")
const selectedStatus = ref("")
const dateRange = ref("")
const itemClass = (index) => {
    switch (index) {
        case 0: return 'item1'
        case 1: return 'item2'
        case 2: return 'item3'
        case 3: return 'item4'
        default: return ''
    }
}
const selected = ref({
    search: "",
    due_after: "",
    due_before: "",
    page: 1
})

onMounted(() => {
    getRepayments()
    getRepaymentCompliance()
})

const getRepayments = async () => {
    loading.value = true
    selected.value.due_after = dateRange.value[0]
    selected.value.due_before = dateRange.value[1]
    const [err, res] = await api.repayments(selected.value)
    if (!err) {
        console.log(res);
        repayments.value = res?.results || []
        paginationInfo.value.total = res?.count || 0
    } else {
        console.log(err)
    }
    loading.value = false
}

async function getRepaymentCompliance() {
    let params = {}
    const [err, res] = await api.repaymentCompliance(params)
    console.log('🚀 ~ getData3 ~ repaymentCompliance:', res)
    repayment.value = res
}

const handleChange = (currantPage) => {
    selected.value.page = currantPage
    getRepayments()
    console.log(currantPage);
}

const addRepayment = () => {
    popup.value = true
    popupAction.value = "Add Payment"
}

const handleEdit = (id) => {
    popup.value = true
    popupAction.value = `Edit Payment ${id}`
}

const close = () => {
    popup.value = false
    // Refresh the repayments list after adding a new one
    getRepayments()
}

const handleSearch = () => {
    console.log(dateRange.value)
    getRepayments()
}

const handleClear = () => {
    searchedRepayment.value = ""
    selectedStatus.value = ""
    dateRange.value = ""
    getRepayments()
}
</script>

<template>
    <div class="repayment">
        <div class="totals">
            <div v-for="(info, index) in totalInfo" :key="index" class="total" :class="itemClass(index)">
                <h1>{{ info.title }}</h1>
                <h2>{{ info.money }}</h2>
                <p>{{ info.num }} repayments</p>
            </div>
        </div>
        <div class="filters">
            <div class="filters_left">
                <el-input v-model="searchedRepayment" style="width: 200px" placeholder="Search..." />
                <!-- <el-select v-model="selectedStatus" placeholder="Select Status" style="width: 200px">
                    <el-option v-for="item in statuses" :key="item.value" :label="item.label" :value="item.value" />
                </el-select> -->
                <div class="date_picker">
                    <el-date-picker v-model="dateRange" type="daterange" start-placeholder="start" end-placeholder="end"
                        format="DD MMM" value-format="YYYY-MM-DD" :prefix-icon="Calendar" clearable style="width: 180px;" />
                </div>
                <Search @click="handleSearch"></Search>
                <Clear @click="handleClear"></Clear>
            </div>
            <Create :action="action" @click="addRepayment"></Create>
        </div>
        <div class="container">
            <div class="list">
                <RepaymentTable :repayments="repayments" @refresh="getRepayments"></RepaymentTable>
                <div class="flex">
                    <div></div>
                    <Pagination :="paginationInfo" @change="handleChange"></Pagination>
                </div>
            </div>
        </div>
        <transition name="slide-right-popup">
            <AddRepayment v-if="popup" :action="popupAction" @close="close">
            </AddRepayment>
        </transition>
    </div>
</template>

<style lang="scss" scoped>
.repayment {
    display: flex;
    flex-direction: column;
    gap: 20px;
}

.totals {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 20px;
}

.total {
    padding: 20px;
    display: flex;
    flex-direction: column;
    align-items: start;
    gap: 10px;
}

h1 {
    font-feature-settings: 'liga' off, 'clig' off;
    font-size: 1.1rem;
    font-style: normal;
    font-weight: 500;
    line-height: normal;
}

h2 {
    color: #384144;
    font-feature-settings: 'liga' off, 'clig' off;
    font-size: 1.5rem;
    font-style: normal;
    font-weight: 600;
    line-height: normal;
    margin: 0;
}

p {
    color: #384144;
    font-feature-settings: 'liga' off, 'clig' off;
    font-size: 1rem;
    font-style: normal;
    font-weight: 400;
    line-height: normal;
    margin: 0;
}

.item1 {
    border-radius: 5px;
    border: 1px solid #E8EBEE;
    background: #384144;
}

.item1 h1,
.item1 h2,
.item1 p {
    color: #FFF;
}

.item2,
.item3,
.item4 {
    border-radius: 5px;
    border: 1px solid #E8EBEE;
    background: #F5F7FB;
}

.item2 h1 {
    color: #1AAD0A;
}

.item3 h1 {
    color: #FAAD14;
}

.item4 h1 {
    color: #F21515;
}

.filters {
    padding: 20px;
    display: flex;
    flex-direction: row;
    justify-content: space-between;
    align-items: center;
    gap: 20px;
    border-radius: 6px;
    background: #FFF;
}

.filters_left {
    display: flex;
    flex-direction: row;
    justify-content: start;
    align-items: center;
    gap: 20px;
}

.date_picker {
    width: 200px;
}

:deep(.el-date-editor .el-range-input) {
    width: 50px !important;
}

:deep(.el-date-editor .el-range__icon) {
    font-size: 20px;
}

:deep(.el-date-editor .el-range-separator) {
    flex: 0;
}

.container {
    flex: 1;
    border-radius: 3px;
    background: #FFF;
    overflow: hidden;

    .list {
        height: 100%;
        padding: 10px;
    }

    .flex {
        display: flex;
        align-items: center;
        justify-content: space-between;
    }

    .pagination {
        margin-top: 20px;
    }
}
.slide-right-popup-enter-active,
.slide-right-popup-leave-active {
    transition: all 0.3s ease;
}

.slide-right-popup-enter-from,
.slide-right-popup-leave-to {
    opacity: 0;
    transform: translateX(100%);
}

.slide-right-popup-enter-to,
.slide-right-popup-leave-from {
    opacity: 1;
    transform: translateX(0);
}
</style>