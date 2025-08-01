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
                            <el-icon style="font-size: 20px" :color="isRepaymentValid ? '#2984DE' : '#E1E1E1'">
                                <SuccessFilled />
                            </el-icon>
                            <p :style="{ color: isRepaymentValid ? '#2984DE' : '#272727' }">Overview</p>
                        </div>
                    </template>
                    <div class="form">
                        <div class="item">
                            <p>Repayment Amount</p>
                            <el-input 
                                v-model="repayment.amount" 
                                type="number"
                                placeholder="0.00"
                                step="0.01"
                                min="0"
                            >
                                <template #prepend>$</template>
                            </el-input>
                        </div>
                        <div class="item">
                            <p>Repayment Due Date</p>
                            <el-date-picker
                                v-model="repayment.due_date"
                                type="date"
                                placeholder="Pick a day"
                                value-format="YYYY-MM-DD"
                                style="width: 100%;"
                            />
                        </div>
                        <div class="item">
                            <p>Repayment Paid Date</p>
                            <el-date-picker
                                v-model="repayment.paid_date"
                                type="date"
                                placeholder="Pick a day"
                                value-format="YYYY-MM-DD"
                                style="width: 100%;"
                            />
                        </div>
                        <div class="item">
                            <p>Application</p>
                            <el-select v-model="repayment.application" placeholder="Select..." style="width: 100%">
                                <el-option 
                                    v-for="item in applications"
                                    :key="item.id"
                                    :label="item.reference_number"
                                    :value="item.id"
                                ></el-option>
                            </el-select>
                        </div>
                        <div class="item">
                            <p>Upload Invoice</p>
                            <button class="file" @click="handleUpload">Select File</button>
                            <p style="text-decoration: underline;">{{ repayment.invoice.name }}</p>
                        </div>                        
                    </div>
                </el-collapse-item>
            </el-collapse>
        </div>
        <div class="buttons">
            <Cancel @click="handleClose"></Cancel>
            <Save @click="handleAdd"></Save>
        </div>
    </div>
</template>

<script setup>
    import { ref, onMounted, computed } from 'vue'
    import { api } from '@/api'
    import Cancel from '../buttons/cancel.vue';
    import Save from '../buttons/save.vue';
    import { ElMessage } from 'element-plus';

    const { action } = defineProps({
        action: String
    })

    const activeNames = ref("1")
    const applications = ref({})
    const repayment = ref({
        amount: "",
        due_date: "",
        paid_date: "",
        invoice: {},
        application: ""
    })

    const emit = defineEmits(['close'])

    onMounted(() => {
        getApplications()
    })

    const isRepaymentValid = computed(() => {
        // Check required fields: amount and application
        return repayment.value.amount && 
               repayment.value.amount > 0 && 
               repayment.value.application
    })

    const handleClose = () => {
        emit('close')
    }
    const handleUpload = () => {
        const input = document.createElement('input')
        input.type = 'file'
        input.onchange = (e) => {
            const file = e.target.files[0]
            if (file) {
                repayment.value.invoice = file
                console.log("file", repayment.value.invoice)
            }
        }
        input.click()
    }
    const getApplications = async () => {
        const [err, res] = await api.applications()
        if (!err) {            
            applications.value = res.results
            console.log(applications.value);
        } else {
            console.log(err)
            ElMessage.error('Failed to load applications')
        }
    }
    const handleAdd = async () => {
        // Validate required fields
        if (!repayment.value.amount || repayment.value.amount <= 0) {
            ElMessage.error('Amount is required and must be greater than 0')
            return
        }
        
        if (!repayment.value.application) {
            ElMessage.error('Application is required')
            return
        }

        const formData = new FormData()
        formData.append('amount', repayment.value.amount.toString())
        
        if (repayment.value.due_date) {
            formData.append('due_date', repayment.value.due_date)
        }
        
        if (repayment.value.paid_date) {
            formData.append('paid_date', repayment.value.paid_date)
        }
        
        formData.append('application', repayment.value.application.toString())
        
        if (repayment.value.invoice && repayment.value.invoice instanceof File) {
            formData.append('invoice', repayment.value.invoice)
        }
        
        // Debug: Log what we're sending
        console.log('Sending repayment data:')
        console.log('Amount:', repayment.value.amount)
        console.log('Application:', repayment.value.application)
        console.log('Due date:', repayment.value.due_date)
        console.log('Paid date:', repayment.value.paid_date)
        console.log('Invoice:', repayment.value.invoice)
        
        // Log FormData contents
        for (let [key, value] of formData.entries()) {
            console.log(`${key}:`, value)
        }
        
        const [err, res] = await api.addRepayments(formData)
        if (!err) {
            console.log(res);
            ElMessage.success('Repayment created successfully')
            emit('close')
        } else {
            console.log('Error response:', err)
            // Show more specific error messages
            if (err.response && err.response.data) {
                const errorData = err.response.data
                console.log('Error data:', errorData)
                if (errorData.amount) {
                    ElMessage.error(`Amount error: ${errorData.amount.join(', ')}`)
                } else if (errorData.application) {
                    ElMessage.error(`Application error: ${errorData.application.join(', ')}`)
                } else if (errorData.invoice) {
                    ElMessage.error(`Invoice error: ${errorData.invoice.join(', ')}`)
                } else {
                    ElMessage.error('Failed to create repayment. Please check your input.')
                }
            } else {
                ElMessage.error('Failed to create repayment. Please try again.')
            }
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
        z-index: 999;
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
    .file {
        width: 100%;
        height: 32px;
        border: 1.5px solid #E1E1E1;
        background: #FFF;
        border-radius: 3px;
    }
</style>