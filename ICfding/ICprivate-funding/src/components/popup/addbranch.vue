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
                    <el-form ref="ruleFormRef" class="form" :model="overview" label-position="top" :rules="rules"
                        label-width="auto">
                        <el-form-item class="item" label="Branch Name" prop="name">
                            <el-input v-model="overview.name" />
                        </el-form-item>
                        <el-form-item class="item" label="Branch Address" prop="address">
                            <el-input v-model="overview.address" />
                        </el-form-item>
                        <el-form-item class="item" label="Phone Number" prop="phone">
                            <el-input v-model="overview.phone" />
                        </el-form-item>
                        <el-form-item class="item" label="Email Address" prop="email">
                            <el-input v-model="overview.email" />
                        </el-form-item>
                    </el-form>
                </el-collapse-item>
            </el-collapse>
        </div>
        <div class="buttons">
            <Cancel @click="handleClose"></Cancel>
            <Save @click="handleAddOrEdit(ruleFormRef)"></Save>
        </div>
    </div>
</template>

<script setup>
import { ref, computed, watch, reactive } from 'vue';
import { api } from '@/api';
import Cancel from '../buttons/cancel.vue';
import Save from '../buttons/save.vue';
import { ElMessage } from 'element-plus'

const props = defineProps({
    action: {
        type: String,
        default: ""
    },
    data: {
        type: Object,
        default: () => ({})
    }
})

// console.log(props.data);

const editId = ref("")
const activeNames = ref("1")
const overview = ref({
    name: "",
    address: "",
    phone: "",
    email: "",
    // manager: ""
})
const managers = ref([
    { value: "1", label: "1" },
    { value: "2", label: "2" }
])

const ruleFormRef = ref(null)
//select trigger触发使用'change'
const rules = reactive({
    name: [
        { required: true, message: 'Please input Branch Name', trigger: 'blur' },
    ],
    address: [
        { required: true, message: 'Please input Activity name', trigger: 'blur' },
    ],
    phone: [
        { required: true, message: 'Please input Activity name', trigger: 'blur' },
    ],
    email: [
        { required: true, message: 'Please input Activity name', trigger: 'blur' },
        { validator: validateEmail, trigger: 'blur' }
    ],
})

//校验邮箱格式
function validateEmail(rule, value, callback) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(value)) {
        callback(new Error('Please enter a valid email address'));
    }
    callback();
}

watch(() => props.data, (newVal) => {
    if (newVal) {
        editId.value = newVal?.id || ""
        overview.value = {
            name: newVal?.name || "",
            address: newVal?.address || "",
            phone: newVal?.phone || "",
            email: newVal?.email || "",
            // manager: newVal.manager
        }
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
const addBranch = async () => {
    const data = {
        ...overview.value
    }
    console.log(data)
    const [err, res] = await api.addBranches(data)
    if (!err) {
        console.log(res);
        emit('close')
    } else {
        console.log(err)
        ElMessage.error(err?.email[0] || err?.phone[0])
    }
}

const editBranch = async () => {
    const data = {
        ...overview.value
    }
    const [err, res] = await api.putBranch(editId.value, data)
    if (!err) {
        emit('close')
    } else {
        console.log(err)
        ElMessage.error(err?.email[0] || err?.phone[0])
    }
}

const handleAddOrEdit = (formEl) => {
    if (!formEl) return
    formEl.validate((valid) => {
        if (valid) {
            if (editId.value) {
                editBranch()
            } else {
                addBranch()
            }
        } else {
            console.log('error submit!')
        }
    })
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
    z-index: 9999;
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
    /* gap: 10px; */
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

.el-form-item {
    margin-bottom: 0;
}
</style>