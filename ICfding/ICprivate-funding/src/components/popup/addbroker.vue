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
                            <p>Contact Name</p>
                            <el-input v-model="overview.name" />
                        </div>
                        <div class="item">
                            <p>Company Name</p>
                            <el-input v-model="overview.company" />
                        </div>
                        <div class="item">
                            <p>Address</p>
                            <el-input v-model="overview.address" />
                        </div>
                        <div class="item">
                            <p>Phone</p>
                            <el-input v-model="overview.phone" />
                        </div>
                        <div class="item">
                            <p>Email</p>
                            <el-input v-model="overview.email" />
                        </div>
                        <div class="item">
                            <p>Branch</p>
                            <el-select v-model="overview.branch" placeholder="Please Select...">
                                <el-option v-for="item in branchesList" :key="item.id" :label="item.name"
                                    :value="item.id" />
                            </el-select>
                        </div>
                        <!-- <div class="item">
                            <p>Lisence Number</p>
                            <el-input v-model="overview.license" />
                        </div> -->
                    </div>
                </el-collapse-item>
                <el-collapse-item name="2">
                    <template #title>
                        <div class="title">
                            <el-icon style="font-size: 20px" :color="isCommissionValid ? '#2984DE' : '#E1E1E1'">
                                <SuccessFilled />
                            </el-icon>
                            <p :style="{ color: isCommissionValid ? '#2984DE' : '#272727' }">Commission Account</p>
                        </div>
                    </template>
                    <div class="form">
                        <div class="item">
                            <p>Bank Name</p>
                            <el-input v-model="commission.commission_bank_name" />
                        </div>
                        <div class="item">
                            <p>Account Name</p>
                            <el-input v-model="commission.commission_account_name" />
                        </div>
                        <div class="item">
                            <p>Account No.</p>
                            <el-input v-model="commission.commission_account_number" />
                        </div>
                        <div class="item">
                            <p>BSB</p>
                            <el-input v-model="commission.commission_bsb" />
                        </div>
                    </div>
                </el-collapse-item>
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
import { api } from '@/api';
import Cancel from '../buttons/cancel.vue';
import Save from '../buttons/save.vue';
import useSystem from '@/hooks/useSystem';
import useBranches from '@/hooks/useBranches'
import { ElMessage } from 'element-plus'

const { branchesList } = useBranches()

const { userInfo } = useSystem()

const props = defineProps({
    action: String,
    editId: [String, Number]
})

const activeNames = ref("1")
//todo something
const overview = ref({
    name: "",
    company: "",
    address: "",
    phone: "",
    email: "",
    branch: "",
    // license: "",
    user: userInfo.value?.user_id || "",
    // bdms: []
})
//todo something
const commission = ref({
    commission_bank_name: "",
    commission_account_name: "",
    commission_account_number: "",
    commission_bsb: ""
})

watch(() => props.editId, (newVal) => {
    if (newVal) {
        console.log("watch", newVal);
        getBroker()
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
const isCommissionValid = computed(() => {
    return Object.values(commission.value).every(value => value !== '')
})

async function getBroker() {
    const [err, res] = await api.broker(props.editId)
    if (!err) {
        console.log(res);
        // brokers.value = res
        overview.value.address = res.address
        overview.value.company = res.company
        overview.value.email = res.email
        overview.value.name = res.name
        overview.value.phone = res.phone
        overview.value.branch = res.branch
        //编辑时传入user会报错，先置为空
        overview.value.user = ""
        // overview.value.bdms = res.bdms
        commission.value.commission_account_name = res.commission_account_name
        commission.value.commission_account_number = res.commission_account_number
        commission.value.commission_bank_name = res.commission_bank_name
        commission.value.commission_bsb = res.commission_bsb
    } else {
        console.log(err)
    }
}
const addBroker = async () => {
    const data = {
        //todo something
        ...overview.value,
        ...commission.value
    }
    console.log(data)
    const [err, res] = await api.addBrokers(data)
    if (!err) {
        console.log(res);
        emit('close')
    } else {
        console.log(JSON.stringify(err))
    }
}

const editBroker = async () => {
    const data = {
        ...overview.value,
        ...commission.value
    }
    const [err, res] = await api.putBrokers(props.editId, data)
    if (!err) {
        emit('close')
    } else {
        console.log(err)
        ElMessage.error(JSON.stringify(err))
    }
}

const handleAddOrEdit = async () => {
    if (props.editId) {
        editBroker()
    } else {
        addBroker()
    }
}
</script>

<style scoped>
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
    z-index: 1999;
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
</style>