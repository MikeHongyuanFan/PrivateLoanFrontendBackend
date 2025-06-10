<template>
    <div class="popup">
        <div class="popup_title">
            <h1>{{ action }}</h1>
            <div class="close">
                <!-- <el-icon :size="20" style="cursor: pointer; color: #7A858E;" @click="handleMinimize"><Minus /></el-icon> -->
                <el-icon :size="20" style="cursor: pointer; color: #7A858E;" @click="handleClose">
                    <Close />
                </el-icon>
            </div>
        </div>
        <div class="popup_content">
            <el-collapse v-model="activeNames" accordion style="--el-collapse-border-color: none;">
                <el-collapse-item name="1">
                    <template #title>
                        <div class="title">
                            <el-icon style="font-size: 20px" :color="isOverviewValid ? '#2984DE' : '#E1E1E1'">
                                <SuccessFilled />
                            </el-icon>
                            <p :style="{ color: isOverviewValid ? '#2984DE' : '#272727' }">Overview</p>
                        </div>
                    </template>
                    <div class="form">
                        <div class="item">
                            <p>Given Names</p>
                            <el-input v-model="overview.first_name" />
                        </div>
                        <div class="item">
                            <p>Surname</p>
                            <el-input v-model="overview.last_name" />
                        </div>
                        <div class="item">
                            <p>Phone Number</p>
                            <el-input v-model="overview.phone" />
                        </div>
                        <div class="item">
                            <p>Email Address</p>
                            <el-input v-model="overview.email" />
                        </div>
                        <div class="item">
                            <p>Date of Birth</p>
                            <el-input v-model="overview.date_of_birth" />
                        </div>
                        <div class="item">
                            <p>tax Id</p>
                            <el-input v-model="overview.tax_id" />
                        </div>
                        <div class="item">
                            <p>Marital Status</p>
                            <el-input v-model="overview.marital_status" />
                        </div>
                        <div class="long_item">
                            <p>Current Employment Type</p>
                            <el-radio-group v-model="overview.employment_type" class="group">
                                <el-radio value="full_time">
                                    <h1>Full Time</h1>
                                </el-radio>
                                <el-radio value="part_ime">
                                    <h1>Part Time</h1>
                                </el-radio>
                                <el-radio value="Casual/Temp">
                                    <h1>Casual/Temp</h1>
                                </el-radio>
                                <el-radio value="contract">
                                    <h1>Contract</h1>
                                </el-radio>
                            </el-radio-group>
                        </div>
                    </div>
                </el-collapse-item>
                <!-- <el-collapse-item name="2">
                    <template #title>
                        <div class="title">
                            <el-icon style="font-size: 20px" :color="isSummaryValid ? '#2984DE' : '#E1E1E1'">
                                <SuccessFilled />
                            </el-icon>
                            <p :style="{ color: isSummaryValid ? '#2984DE' : '#272727' }">Financial Summary</p>
                        </div>
                    </template>
                    <div class="form">
                        <div class="item">
                            <p>Total Loan</p>
                            <el-input v-model="summary.total" />
                        </div>
                        <div class="item">
                            <p>Active Loans</p>
                            <el-input v-model="summary.active" />
                        </div>
                        <div class="item">
                            <p>Total Loan Amount</p>
                            <el-input v-model="summary.totalAmount" />
                        </div>
                        <div class="item">
                            <p>Outstanding Amount</p>
                            <el-input v-model="summary.outstanding" />
                        </div>
                    </div>
                </el-collapse-item> -->
            </el-collapse>
        </div>
        <div class="buttons">
            <Cancel @click="handleClose"></Cancel>
            <Save @click="handleAddOrEdit"></Save>
        </div>
    </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue';
import Cancel from '../buttons/cancel.vue';
import Save from '../buttons/save.vue';
import { api } from '@/api';
import useSystem from '@/hooks/useSystem'
import { ElMessage } from 'element-plus'

const { userInfo } = useSystem()

const props = defineProps({
    action: String,
    editId: [String, Number]
})

const activeNames = ref("1")
//todo something
const overview = ref({
    first_name: "",
    last_name: "",
    email: "",
    phone: "",
    date_of_birth: "",
    tax_id: "",
    marital_status: "",
    residency_status: "",
    referral_source: "",
    tags: "",
    employment_type: "",
    // user: userInfo.value?.user_id || "",
})
//todo something
const summary = ref({
    total: "",
    active: "",
    totalAmount: "",
    outstanding: ""
})
watch(() => props.editId, (newVal) => {
    if (newVal) {
        console.log("watch", newVal);
        getBorrower()
    }
}, { deep: true, immediate: true })

const emit = defineEmits(['close', 'minimize'])

const handleClose = () => {
    emit('close')
}
const handleMinimize = () => {
    emit('minimize')
}
const isOverviewValid = computed(() => {
    return Object.values(overview.value).every(value => value !== '')
})
const isSummaryValid = computed(() => {
    return Object.values(summary.value).every(value => value !== '')
})

async function getBorrower() {
    const [err, res] = await api.borrower(props.editId)
    if (!err) {
        console.log(res);
        overview.value.first_name = res?.first_name || ""
        overview.value.last_name = res?.last_name || ""
        overview.value.email = res?.email || ""
        overview.value.phone = res?.phone || ""
        overview.value.date_of_birth = res?.date_of_birth || ""
        overview.value.tax_id = res?.tax_id || ""
        overview.value.marital_status = res?.marital_status || ""
        overview.value.residency_status = res?.residency_status || ""
        overview.value.referral_source = res?.referral_source || ""
        overview.value.tags = res?.tags || ""
        overview.value.employment_type = res?.employment_type || ""
    } else {
        console.log(err)
    }
}

const addBorrower = async () => {
    const data = {
        //todo something
        ...overview.value,
        // ...commission.value
    }
    console.log(data)
    const [err, res] = await api.addBorrowers(data)
    if (!err) {
        console.log(res);
        emit('close')
    } else {
        ElMessage.error(JSON.stringify(err))
    }
}

const editBorrower = async () => {
    const data = {
        ...overview.value
    }
    console.log(data)
    const [err, res] = await api.putBorrower(props.editId, data)
    if (!err) {
        console.log(res);
        emit('close')
    } else {
        console.log(err)
        ElMessage.error(JSON.stringify(err))
    }
}

const handleAddOrEdit = async () => {
    if (props.editId) {
        editBorrower()
    } else {
        addBorrower()
    }
}
</script>

<style lang="scss" scoped>
.popup {
    position: fixed;
    top: 0;
    right: 0;
    bottom: 0;
    padding: 10px;
    display: flex;
    flex-direction: column;
    background: white;
    border: none;
    box-shadow: -8px -1px 9.3px 0px rgba(202, 202, 202, 0.16);
    width: 40%;
    height: 100vh;
    overflow: hidden;
    z-index: 1000;
}

.popup_title {
    width: 100%;
    padding: 10px;
    display: flex;
    flex-direction: row;
    justify-content: space-between;
    align-items: center;
    border-bottom: 1.5px solid var(--Line, #E1E1E1);
}

h1 {
    color: #384144;
    font-feature-settings: 'liga' off, 'clig' off;
    font-size: 1.1rem;
    font-style: normal;
    font-weight: 500;
    line-height: 12px;
}

.close {
    display: flex;
    flex-direction: row;
    align-items: center;
    gap: 20px;
}

.popup_content {
    width: 100%;
    padding: 10px;
}

.title {
    display: flex;
    flex-direction: row;
    align-items: center;
    gap: 10px;
    padding-left: 5px;
}

.title p {
    font-feature-settings: 'liga' off, 'clig' off;
    font-size: 0.9rem;
    font-style: normal;
    font-weight: 400;
    line-height: 12px;
}

.form {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 15px 20px;
}

.item {
    display: flex;
    flex-direction: column;
    align-items: start;
    gap: 10px;
}

.item p {
    color: #384144;
    font-feature-settings: 'liga' off, 'clig' off;
    font-size: 0.75rem;
    font-style: normal;
    font-weight: 500;
    line-height: 12px;
    margin: 0;
}

.buttons {
    width: 100%;
    padding: 10px;
    margin-top: auto;
    display: flex;
    flex-direction: row;
    justify-content: end;
    align-items: center;
    border-top: 1.5px solid #E1E1E1;
    gap: 10px;
}

.long_item {
    grid-column: 1 / 3;
    display: flex;
    flex-direction: column;
    align-items: start;
    gap: 10px;
}

.group {
    width: 100%;
    display: flex;
    flex-direction: row;
    justify-content: space-between;
    align-items: center;

    h1 {
        color: #384144;
        font-feature-settings: 'liga' off, 'clig' off;
        font-size: 0.9rem;
        font-style: normal;
        font-weight: 500;
        line-height: 12px;
    }
}
</style>