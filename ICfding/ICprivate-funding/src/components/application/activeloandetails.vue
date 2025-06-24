<template>
    <div class="content" v-if="showActiveLoanSection">
        <div class="section-header">
            <h1>Active Loan Details</h1>
            <div class="header-actions">
                <el-button 
                    type="primary" 
                    size="small" 
                    @click="toggleEditMode"
                >
                    {{ isEditMode ? 'Save' : 'Edit' }}
                </el-button>
                <el-button 
                    v-if="activeLoan?.loan_expiry_date"
                    type="warning" 
                    size="small" 
                    @click="sendAlert('expiry')"
                >
                    Send Alert
                </el-button>
            </div>
        </div>

        <div class="form">
            <!-- Loan Basic Information -->
            <div class="item">
                <p class="title">Settlement Date</p>
                <el-date-picker
                    v-if="isEditMode"
                    v-model="formData.settlement_date"
                    type="date"
                    placeholder="Select settlement date"
                    format="YYYY-MM-DD"
                    value-format="YYYY-MM-DD"
                    style="width: 100%"
                />
                <p v-else>{{ formatDate(activeLoan?.settlement_date) }}</p>
            </div>
            
            <div class="item">
                <p class="title">Capitalised Interest (Months)</p>
                <el-input-number
                    v-if="isEditMode"
                    v-model="formData.capitalised_interest_months"
                    :min="0"
                    :max="120"
                    placeholder="Enter months"
                    style="width: 100%"
                />
                <p v-else>{{ activeLoan?.capitalised_interest_months || 0 }} months</p>
            </div>
            
            <div class="item">
                <p class="title">Interest Payment Required</p>
                <el-select
                    v-if="isEditMode"
                    v-model="formData.interest_payments_required"
                    placeholder="Select option"
                    style="width: 100%"
                >
                    <el-option label="Yes" :value="true"></el-option>
                    <el-option label="No" :value="false"></el-option>
                </el-select>
                <p v-else>{{ activeLoan?.interest_payments_required ? 'Yes' : 'No' }}</p>
            </div>
            
            <div class="item">
                <p class="title">Loan Expiry Date</p>
                <el-date-picker
                    v-if="isEditMode"
                    v-model="formData.loan_expiry_date"
                    type="date"
                    placeholder="Select expiry date"
                    format="YYYY-MM-DD"
                    value-format="YYYY-MM-DD"
                    style="width: 100%"
                />
                <div v-else class="expiry-info">
                    <p>{{ formatDate(activeLoan?.loan_expiry_date) }}</p>
                    <span 
                        v-if="activeLoan?.days_until_expiry !== null"
                        :class="getAlertClass(activeLoan?.days_until_expiry)"
                        class="days-remaining"
                    >
                        {{ formatDaysRemaining(activeLoan?.days_until_expiry) }}
                    </span>
                </div>
            </div>
        </div>

        <!-- Repayment Schedule Section -->
        <div class="part" v-if="formData.interest_payments_required || activeLoan?.interest_payments_required">
            <h1>Repayment Schedule</h1>
            <div class="repayment-header">
                <el-button 
                    v-if="isEditMode"
                    type="primary" 
                    size="small" 
                    @click="addPaymentDate"
                >
                    Add New
                </el-button>
            </div>

            <div class="repayment-list">
                <div 
                    v-for="(payment, index) in displayPayments" 
                    :key="index"
                    class="repayment-item"
                >
                    <div class="repayment-info">
                        <div class="repayment-date">
                            <p class="title">Repayment Due Date</p>
                            <el-date-picker
                                v-if="isEditMode"
                                v-model="payment.date"
                                type="date"
                                placeholder="Select due date"
                                format="YYYY-MM-DD"
                                value-format="YYYY-MM-DD"
                                style="width: 100%"
                            />
                            <p v-else>{{ formatDate(payment.date) }}</p>
                        </div>
                        
                        <div class="repayment-amount">
                            <p class="title">Repayment Amount</p>
                            <el-input-number
                                v-if="isEditMode"
                                v-model="payment.amount"
                                :min="0"
                                :precision="2"
                                placeholder="Enter amount"
                                style="width: 100%"
                            />
                            <p v-else>${{ formatCurrency(payment.amount) }}</p>
                        </div>
                        
                        <div class="days-remain">
                            <p class="title">Days Remain</p>
                            <p :class="getAlertClass(payment.daysRemain)">
                                {{ formatDaysRemaining(payment.daysRemain) }}
                            </p>
                        </div>
                        
                        <div class="actions">
                            <el-button 
                                type="warning" 
                                size="small" 
                                @click="sendAlert('payment', index)"
                            >
                                Send Alert
                            </el-button>
                            <el-button 
                                v-if="isEditMode"
                                type="danger" 
                                size="small" 
                                @click="removePayment(index)"
                            >
                                Remove
                            </el-button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { api } from '@/api'

const props = defineProps({
    detail: {
        type: Object,
        required: true,
        default: () => ({})
    }
})

// Reactive data
const activeLoan = ref(null)
const isEditMode = ref(false)
const saving = ref(false)
const sendingAlert = ref(false)

// Form data for editing
const formData = ref({
    settlement_date: '',
    capitalised_interest_months: 0,
    interest_payments_required: false,
    loan_expiry_date: '',
    payments: []
})

// Computed properties
const showActiveLoanSection = computed(() => {
    return props.detail?.stage === 'settled' || activeLoan.value
})

const displayPayments = computed(() => {
    if (isEditMode.value) {
        return formData.value.payments
    }
    
    // Transform backend data for display
    if (activeLoan.value?.interest_payment_due_dates) {
        return activeLoan.value.interest_payment_due_dates.map(date => ({
            date: date,
            amount: 0,
            daysRemain: calculateDaysRemaining(date)
        }))
    }
    
    return []
})

// Methods
const loadActiveLoanData = async () => {
    try {
        console.log('Loading active loan data for application:', props.detail.id)
        const [error, data] = await api.getActiveLoanByApplication(props.detail.id)
        
        if (!error && data) {
            console.log('Active loan data loaded:', data)
            activeLoan.value = data
            
            // Populate form data with existing active loan data
            formData.value = {
                settlement_date: data.settlement_date,
                capitalised_interest_months: data.capitalised_interest_months,
                interest_payments_required: data.interest_payments_required,
                loan_expiry_date: data.loan_expiry_date,
                payments: data.interest_payment_due_dates?.map(date => ({ date })) || []
            }
        } else if (error && error.response?.status === 404) {
            console.log('No active loan found, will create new one')
            // No active loan exists, keep form data empty for creation
            activeLoan.value = null
        } else {
            console.error('Error loading active loan data:', error)
            ElMessage.error('Failed to load active loan data')
        }
    } catch (err) {
        console.error('Exception loading active loan data:', err)
        ElMessage.error('Error loading active loan data')
    }
}

const toggleEditMode = async () => {
    if (isEditMode.value) {
        await saveActiveLoanDetails()
    } else {
        isEditMode.value = true
    }
}

const addPaymentDate = () => {
    formData.value.payments.push({
        date: '',
        amount: 0,
        daysRemain: null
    })
}

const removePayment = (index) => {
    formData.value.payments.splice(index, 1)
}

const saveActiveLoanDetails = async () => {
    try {
        saving.value = true
        
        console.log('=== SAVE ACTIVE LOAN DEBUG ===')
        console.log('Application stage:', props.detail.stage)
        console.log('Application ID:', props.detail.id, 'Type:', typeof props.detail.id)
        console.log('Form data:', formData.value)
        console.log('Existing active loan:', activeLoan.value)
        
        const apiData = {
            application: parseInt(props.detail.id),
            settlement_date: formData.value.settlement_date,
            capitalised_interest_months: formData.value.capitalised_interest_months,
            interest_payments_required: formData.value.interest_payments_required,
            interest_payment_frequency: formData.value.interest_payments_required ? 'monthly' : null,
            loan_expiry_date: formData.value.loan_expiry_date,
            interest_payment_due_dates: formData.value.payments.map(p => p.date).filter(date => date)
        }
        
        console.log('API data being sent:', apiData)
        
        let result
        if (activeLoan.value?.id) {
            console.log('Updating existing active loan:', activeLoan.value.id)
            const [error, data] = await api.patchActiveLoan(activeLoan.value.id, apiData)
            result = { error, data }
        } else {
            console.log('Creating new active loan')
            const [error, data] = await api.createActiveLoan(apiData)
            result = { error, data }
        }
        
        if (!result.error) {
            activeLoan.value = result.data
            isEditMode.value = false
            ElMessage.success('Active loan details saved successfully')
        } else {
            console.error('API Error:', result.error)
            console.error('Full error response:', JSON.stringify(result.error, null, 2))
            
            // Handle specific error cases
            if (result.error.application && Array.isArray(result.error.application)) {
                if (result.error.application[0].includes('already exists')) {
                    ElMessage.error('An active loan already exists for this application. Please refresh the page.')
                } else {
                    ElMessage.error(`Application error: ${result.error.application[0]}`)
                }
            } else if (result.error.non_field_errors) {
                ElMessage.error(`Validation error: ${result.error.non_field_errors.join(', ')}`)
            } else {
                // Show all validation errors
                const errorMessages = Object.entries(result.error)
                    .map(([field, errors]) => `${field}: ${Array.isArray(errors) ? errors.join(', ') : errors}`)
                    .join('; ')
                ElMessage.error(`Validation errors: ${errorMessages}`)
            }
        }
    } catch (err) {
        console.error('Exception:', err)
        ElMessage.error('Error saving active loan details')
    } finally {
        saving.value = false
    }
}

const sendAlert = async (alertType, paymentIndex = null) => {
    if (!activeLoan.value?.id) {
        ElMessage.error('No active loan found')
        return
    }

    sendingAlert.value = true
    
    try {
        let message = ''
        
        // Create appropriate message based on alert type
        if (alertType === 'expiry') {
            message = `Loan expiry alert for ${activeLoan.value.application_reference}`
        } else if (alertType === 'payment' && paymentIndex !== null) {
            const payment = displayPayments.value[paymentIndex]
            if (payment) {
                message = `Payment due alert for ${activeLoan.value.application_reference} - Due: ${formatDate(payment.date)}`
            }
        }
        
        const [error, data] = await api.sendActiveLoanAlert(
            activeLoan.value.id,
            alertType,
            message
        )
        
        if (!error) {
            ElMessage.success('Alert sent successfully!')
            console.log('Alert sent:', data)
        } else {
            console.error('Error sending alert:', error)
            ElMessage.error(error.response?.data?.error || 'Failed to send alert')
        }
    } catch (err) {
        console.error('Exception sending alert:', err)
        ElMessage.error('Error sending alert')
    } finally {
        sendingAlert.value = false
    }
}

// Utility functions
const formatDate = (dateString) => {
    if (!dateString) return '-'
    return new Date(dateString).toLocaleDateString()
}

const formatCurrency = (amount) => {
    if (!amount) return '0.00'
    return amount.toFixed(2)
}

const calculateDaysRemaining = (date) => {
    if (!date) return null
    const today = new Date()
    const targetDate = new Date(date)
    const diffTime = targetDate - today
    return Math.ceil(diffTime / (1000 * 60 * 60 * 24))
}

const formatDaysRemaining = (days) => {
    if (days === null) return '-'
    if (days < 0) return `${Math.abs(days)} days overdue`
    if (days === 0) return 'Due today'
    return `${days} days remaining`
}

const getAlertClass = (days) => {
    if (days === null) return ''
    if (days <= 7) return 'alert-critical'
    if (days <= 30) return 'alert-warning'
    return ''
}

// Watch for prop changes
watch(() => props.detail, (newDetail) => {
    if (newDetail?.id) {
        loadActiveLoanData()
    }
}, { immediate: true })

// Lifecycle
onMounted(() => {
    if (props.detail?.id) {
        loadActiveLoanData()
    }
})
</script>

<style scoped>
.content {
    padding: 20px;
    border-radius: 6px;
    background: #FFF;
    display: flex;
    flex-direction: column;
    gap: 20px;
}

.section-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 20px;
    padding-bottom: 12px;
    border-bottom: 1.5px solid #E8EBEE;
}

.section-header h1 {
    color: #384144;
    font-feature-settings: 'liga' off, 'clig' off;
    font-size: 0.9rem;
    font-style: normal;
    font-weight: 600;
    line-height: normal;
    margin: 0;
}

.header-actions {
    display: flex;
    gap: 12px;
}

.form {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 20px;
}

.item {
    display: flex;
    flex-direction: column;
    gap: 10px;
}

.part {
    padding: 20px 0;
    border-top: 1.5px solid #E8EBEE;
}

.part:first-child {
    border-top: none;
    padding-top: 0;
}

.part h1 {
    color: #384144;
    font-feature-settings: 'liga' off, 'clig' off;
    font-size: 0.9rem;
    font-style: normal;
    font-weight: 600;
    line-height: normal;
    margin: 0 0 15px 0;
}

p {
    color: #384144;
    font-feature-settings: 'liga' off, 'clig' off;
    font-size: 0.75rem;
    font-style: normal;
    font-weight: 600;
    line-height: 140%;
    margin: 0;
}

.title {
    color: #7A858E;
}

.expiry-info {
    display: flex;
    flex-direction: column;
    gap: 4px;
}

.days-remaining {
    font-size: 0.7rem;
    font-weight: 500;
    padding: 2px 8px;
    border-radius: 4px;
    display: inline-block;
    width: fit-content;
}

.repayment-header {
    display: flex;
    justify-content: flex-end;
    margin-bottom: 15px;
}

.repayment-list {
    display: flex;
    flex-direction: column;
    gap: 12px;
}

.repayment-item {
    background: #FAFAFA;
    border: 1px solid #E8EBEE;
    border-radius: 6px;
    padding: 15px;
}

.repayment-info {
    display: grid;
    grid-template-columns: repeat(3, 1fr) auto;
    gap: 15px;
    align-items: end;
}

.repayment-date,
.repayment-amount,
.days-remain {
    display: flex;
    flex-direction: column;
    gap: 8px;
}

.actions {
    display: flex;
    gap: 8px;
    flex-direction: column;
}

.alert-critical {
    color: #c53030 !important;
    background-color: #fee !important;
}

.alert-warning {
    color: #d69e2e !important;
    background-color: #fff4e6 !important;
}

@media (max-width: 768px) {
    .form {
        grid-template-columns: 1fr;
    }

    .repayment-info {
        grid-template-columns: 1fr;
        
        .actions {
            flex-direction: row;
        }
    }
}
</style> 