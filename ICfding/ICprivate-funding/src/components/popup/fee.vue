<template>
    <div class="popup">
        <div class="popup_title">
            <h1>Fees Management</h1>
            <div class="close">
                <el-icon :size="20" style="cursor: pointer; color: #7A858E;" @click="handleClose">
                    <Close />
                </el-icon>                    
            </div>
        </div>
        
        <!-- Header Actions -->
        <div class="header-actions">
            <el-button 
                type="primary" 
                size="small" 
                @click="showAddFeeDialog"
                :disabled="!applicationId"
            >
                <el-icon><Plus /></el-icon>
                Add Fee
            </el-button>
            <el-button 
                size="small" 
                @click="refreshFees"
                :loading="loading"
            >
                <el-icon><Refresh /></el-icon>
                Refresh
            </el-button>
        </div>

        <!-- Filters -->
        <div class="filters">
            <el-select 
                v-model="filterFeeType" 
                placeholder="Filter by type" 
                clearable 
                size="small"
                @change="applyFilters"
            >
                <el-option label="All Types" value="" />
                <el-option 
                    v-for="type in feeTypes" 
                    :key="type.value" 
                    :label="type.label" 
                    :value="type.value" 
                />
            </el-select>
            <el-select 
                v-model="filterPaymentStatus" 
                placeholder="Payment status" 
                clearable 
                size="small"
                @change="applyFilters"
            >
                <el-option label="All" value="" />
                <el-option label="Paid" value="true" />
                <el-option label="Unpaid" value="false" />
            </el-select>
        </div>

        <el-scrollbar class="fees-content">
            <div v-if="loading && fees.length === 0" class="loading-container">
                <el-skeleton :rows="3" animated />
            </div>
            
            <div v-else-if="fees.length === 0" class="empty-state">
                <el-empty description="No fees found" />
            </div>
            
            <div v-else>
                <div v-for="fee in filteredFees" :key="fee.id" class="fee-card">
                    <div class="fee-header">
                        <div class="fee-type">
                            <el-tag :type="getTagType(fee.fee_type)">
                                {{ fee.fee_type_display }}
                            </el-tag>
                        </div>
                        <div class="fee-status">
                            <el-tag 
                                :type="fee.status === 'paid' ? 'success' : 'warning'"
                                size="small"
                            >
                                {{ fee.status || (fee.paid_date ? 'Paid' : 'Unpaid') }}
                            </el-tag>
                        </div>
                    </div>
                    
                    <div class="fee-content">
                        <div class="fee-row">
                            <div class="item">
                                <p class="title">Fee ID</p>
                                <p class="value">#{{ fee.id }}</p>
                            </div>
                            <div class="item">
                                <p class="title">Amount</p>
                                <p class="value amount">${{ formatAmount(fee.amount) }}</p>
                            </div>
                        </div>
                        
                        <div class="fee-row" v-if="fee.description">
                            <div class="item full-width">
                                <p class="title">Description</p>
                                <p class="value">{{ fee.description }}</p>
                            </div>
                        </div>
                        
                        <div class="fee-row">
                            <div class="item">
                                <p class="title">Due Date</p>
                                <p class="value">{{ formatDate(fee.due_date) }}</p>
                            </div>
                            <div class="item" v-if="fee.paid_date">
                                <p class="title">Paid Date</p>
                                <p class="value">{{ formatDate(fee.paid_date) }}</p>
                            </div>
                        </div>
                        
                        <div class="fee-row" v-if="fee.created_by_name">
                            <div class="item">
                                <p class="title">Created By</p>
                                <p class="value">{{ fee.created_by_name }}</p>
                            </div>
                            <div class="item">
                                <p class="title">Created At</p>
                                <p class="value">{{ formatDateTime(fee.created_at) }}</p>
                            </div>
                        </div>
                    </div>
                    
                    <div class="fee-actions">
                        <el-button 
                            v-if="!fee.paid_date && fee.status !== 'paid'" 
                            type="success" 
                            size="small"
                            @click="markAsPaid(fee)"
                        >
                            <el-icon><Check /></el-icon>
                            Mark Paid
                        </el-button>
                        <el-button 
                            size="small" 
                            @click="editFee(fee)"
                        >
                            <el-icon><Edit /></el-icon>
                            Edit
                        </el-button>
                        <el-button 
                            v-if="fee.invoice_url" 
                            size="small" 
                            @click="viewInvoice(fee.invoice_url)"
                        >
                            <el-icon><Document /></el-icon>
                            Invoice
                        </el-button>
                        <el-button 
                            type="danger" 
                            size="small"
                            @click="deleteFee(fee)"
                        >
                            <el-icon><Delete /></el-icon>
                            Delete
                        </el-button>
                    </div>
                </div>
            </div>
        </el-scrollbar>
        
        <!-- Add/Edit Fee Dialog -->
        <el-dialog 
            v-model="showFeeDialog" 
            :title="editingFee ? 'Edit Fee' : 'Add New Fee'"
            width="500px"
        >
            <el-form 
                ref="feeFormRef" 
                :model="feeForm" 
                :rules="feeFormRules"
                label-width="120px"
            >
                <el-form-item label="Fee Type" prop="fee_type">
                    <el-select v-model="feeForm.fee_type" placeholder="Select fee type">
                        <el-option 
                            v-for="type in feeTypes" 
                            :key="type.value" 
                            :label="type.label" 
                            :value="type.value" 
                        />
                    </el-select>
                </el-form-item>
                
                <el-form-item label="Amount" prop="amount">
                    <el-input 
                        v-model="feeForm.amount" 
                        type="number" 
                        placeholder="0.00"
                        step="0.01"
                    >
                        <template #prepend>$</template>
                    </el-input>
                </el-form-item>
                
                <el-form-item label="Description">
                    <el-input 
                        v-model="feeForm.description" 
                        type="textarea" 
                        :rows="3"
                        placeholder="Optional description"
                    />
                </el-form-item>
                
                <el-form-item label="Due Date">
                    <el-date-picker 
                        v-model="feeForm.due_date" 
                        type="date"
                        placeholder="Select due date"
                        style="width: 100%"
                    />
                </el-form-item>
                
                <el-form-item label="Invoice" v-if="editingFee">
                    <el-upload 
                        ref="uploadRef"
                        action="#" 
                        :auto-upload="false"
                        :on-change="handleFileChange"
                        :show-file-list="false"
                    >
                        <el-button size="small">
                            <el-icon><Upload /></el-icon>
                            Upload Invoice
                        </el-button>
                    </el-upload>
                    <span v-if="feeForm.invoice" class="file-name">{{ feeForm.invoice.name }}</span>
                </el-form-item>
            </el-form>
            
            <template #footer>
                <div class="dialog-footer">
                    <el-button @click="closeFeeDialog">Cancel</el-button>
                    <el-button 
                        type="primary" 
                        @click="saveFee"
                        :loading="saving"
                    >
                        {{ editingFee ? 'Update' : 'Create' }}
                    </el-button>
                </div>
            </template>
        </el-dialog>
    </div>
</template>

<script setup>
import { ref, onMounted, computed, watch } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { feesApi } from '@/api/fees'
import { 
    Close, Plus, Refresh, Check, Edit, Delete, Document, Upload 
} from '@element-plus/icons-vue'

const props = defineProps({
    id: {
        type: [String, Number],
        default: null
    },
    applicationId: {
        type: [String, Number], 
        default: null
    }
})

const emit = defineEmits(['close', 'minimize'])

// Reactive data
const fees = ref([])
const loading = ref(false)
const saving = ref(false)
const filterFeeType = ref('')
const filterPaymentStatus = ref('')

// Dialog states
const showFeeDialog = ref(false)
const editingFee = ref(null)
const feeFormRef = ref()

// Form data
const feeForm = ref({
    fee_type: '',
    amount: '',
    description: '',
    due_date: null,
    application: null,
    invoice: null
})

// Fee types based on schema
const feeTypes = [
    { value: 'application', label: 'Application Fee' },
    { value: 'valuation', label: 'Valuation Fee' },
    { value: 'legal', label: 'Legal Fee' },
    { value: 'broker', label: 'Broker Fee' },
    { value: 'settlement', label: 'Settlement Fee' },
    { value: 'other', label: 'Other Fee' }
]

// Form validation rules
const feeFormRules = {
    fee_type: [
        { required: true, message: 'Please select a fee type', trigger: 'change' }
    ],
    amount: [
        { required: true, message: 'Please enter an amount', trigger: 'blur' },
        { 
            pattern: /^\d+(\.\d{0,2})?$/, 
            message: 'Please enter a valid amount', 
            trigger: 'blur' 
        }
    ]
}

// Computed properties
const filteredFees = computed(() => {
    let filtered = fees.value
    
    if (filterFeeType.value) {
        filtered = filtered.filter(fee => fee.fee_type === filterFeeType.value)
    }
    
    if (filterPaymentStatus.value !== '') {
        const isPaid = filterPaymentStatus.value === 'true'
        filtered = filtered.filter(fee => {
            const hasPaidDate = !!fee.paid_date
            const isPaidStatus = fee.status === 'paid'
            return isPaid ? (hasPaidDate || isPaidStatus) : (!hasPaidDate && fee.status !== 'paid')
        })
    }
    
    return filtered
})

// Methods
const handleClose = () => {
    emit('close')
}

const getFees = async () => {
    loading.value = true
    try {
        const targetId = props.applicationId || props.id
        let response
        
        if (targetId) {
            const [err, res] = await feesApi.getFeesByApplication(targetId)
            response = [err, res]
        } else {
            const [err, res] = await feesApi.getFees()
            response = [err, res]
        }
        
        const [err, res] = response
        if (!err && res) {
            fees.value = res.results || res
        } else {
            console.error('Error fetching fees:', err)
            ElMessage.error('Failed to load fees')
        }
    } catch (error) {
        console.error('Error fetching fees:', error)
        ElMessage.error('Failed to load fees')
    } finally {
        loading.value = false
    }
}

const refreshFees = () => {
    getFees()
}

const applyFilters = () => {
    // Filters are applied via computed property
}

const showAddFeeDialog = () => {
    editingFee.value = null
    resetFeeForm()
    feeForm.value.application = props.applicationId || props.id
    showFeeDialog.value = true
}

const editFee = (fee) => {
    editingFee.value = fee
    feeForm.value = {
        fee_type: fee.fee_type,
        amount: fee.amount,
        description: fee.description || '',
        due_date: fee.due_date ? new Date(fee.due_date) : null,
        application: fee.application,
        invoice: null
    }
    showFeeDialog.value = true
}

const closeFeeDialog = () => {
    showFeeDialog.value = false
    editingFee.value = null
    resetFeeForm()
}

const resetFeeForm = () => {
    feeForm.value = {
        fee_type: '',
        amount: '',
        description: '',
        due_date: null,
        application: null,
        invoice: null
    }
    if (feeFormRef.value) {
        feeFormRef.value.resetFields()
    }
}

const handleFileChange = (file) => {
    feeForm.value.invoice = file.raw
}

const saveFee = async () => {
    if (!feeFormRef.value) return
    
    try {
        await feeFormRef.value.validate()
        saving.value = true
        
        const formData = new FormData()
        formData.append('fee_type', feeForm.value.fee_type)
        formData.append('amount', feeForm.value.amount)
        formData.append('application', feeForm.value.application)
        
        if (feeForm.value.description) {
            formData.append('description', feeForm.value.description)
        }
        
        if (feeForm.value.due_date) {
            formData.append('due_date', feeForm.value.due_date.toISOString().split('T')[0])
        }
        
        if (feeForm.value.invoice) {
            formData.append('invoice', feeForm.value.invoice)
        }
        
        let response
        if (editingFee.value) {
            const [err, res] = await feesApi.updateFee(editingFee.value.id, formData)
            response = [err, res]
        } else {
            const [err, res] = await feesApi.createFee(formData)
            response = [err, res]
        }
        
        const [err, res] = response
        if (!err) {
            ElMessage.success(`Fee ${editingFee.value ? 'updated' : 'created'} successfully`)
            closeFeeDialog()
            getFees()
        } else {
            console.error('Error saving fee:', err)
            ElMessage.error(`Failed to ${editingFee.value ? 'update' : 'create'} fee`)
        }
    } catch (error) {
        console.error('Validation failed:', error)
    } finally {
        saving.value = false
    }
}

const markAsPaid = async (fee) => {
    try {
        await ElMessageBox.confirm(
            `Mark fee #${fee.id} (${fee.fee_type_display}) as paid?`,
            'Confirm Payment',
            {
                confirmButtonText: 'Mark Paid',
                cancelButtonText: 'Cancel',
                type: 'warning'
            }
        )
        
        const paymentData = {
            paid_date: new Date().toISOString().split('T')[0]
        }
        
        const [err, res] = await feesApi.markFeePaid(fee.id, paymentData)
        if (!err) {
            ElMessage.success('Fee marked as paid successfully')
            getFees()
        } else {
            console.error('Error marking fee as paid:', err)
            ElMessage.error('Failed to mark fee as paid')
        }
    } catch (error) {
        // User cancelled or error occurred
        if (error !== 'cancel') {
            console.error('Error:', error)
        }
    }
}

const deleteFee = async (fee) => {
    try {
        await ElMessageBox.confirm(
            `Delete fee #${fee.id} (${fee.fee_type_display})?`,
            'Confirm Delete',
            {
                confirmButtonText: 'Delete',
                cancelButtonText: 'Cancel',
                type: 'error'
            }
        )
        
        const [err, res] = await feesApi.deleteFee(fee.id)
        if (!err) {
            ElMessage.success('Fee deleted successfully')
            getFees()
        } else {
            console.error('Error deleting fee:', err)
            ElMessage.error('Failed to delete fee')
        }
    } catch (error) {
        // User cancelled or error occurred
        if (error !== 'cancel') {
            console.error('Error:', error)
        }
    }
}

const viewInvoice = (invoiceUrl) => {
    if (invoiceUrl) {
        window.open(invoiceUrl, '_blank')
    }
}

// Utility functions
const formatAmount = (amount) => {
    return parseFloat(amount).toFixed(2)
}

const formatDate = (date) => {
    if (!date) return 'N/A'
    return new Date(date).toLocaleDateString()
}

const formatDateTime = (datetime) => {
    if (!datetime) return 'N/A'
    return new Date(datetime).toLocaleString()
}

const getTagType = (feeType) => {
    const typeMap = {
        'application': 'primary',
        'valuation': 'success',
        'legal': 'warning',
        'broker': 'info',
        'settlement': 'success',
        'other': 'default'
    }
    return typeMap[feeType] || 'default'
}

// Watchers
watch(() => props.applicationId, (newVal) => {
    if (newVal) {
        getFees()
    }
}, { immediate: true })

watch(() => props.id, (newVal) => {
    if (newVal && !props.applicationId) {
        getFees()
    }
}, { immediate: true })

// Lifecycle
onMounted(() => {
    if (props.applicationId || props.id) {
        getFees()
    }
})
</script>

<style scoped>
.popup {
    position: fixed;
    top: 0;
    right: 0;
    bottom: 0;
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
    padding: 20px;
    display: flex;
    flex-direction: row;
    justify-content: space-between;
    align-items: center;
    border-bottom: 1.5px solid var(--Line, #E1E1E1);
    background: #f8f9fa;
}

h1 {
    color: #384144;
    font-feature-settings: 'liga' off, 'clig' off;
    font-size: 1.2rem;
    font-style: normal;
    font-weight: 600;
    line-height: 20px;
    margin: 0;
}

.header-actions {
    padding: 15px 20px;
    border-bottom: 1px solid #e1e1e1;
    display: flex;
    gap: 10px;
    align-items: center;
}

.filters {
    padding: 15px 20px;
    display: flex;
    gap: 15px;
    align-items: center;
    border-bottom: 1px solid #e1e1e1;
    background: #fafafa;
}

.fees-content {
    flex: 1;
    padding: 20px;
}

.loading-container {
    padding: 20px;
}

.empty-state {
    display: flex;
    justify-content: center;
    align-items: center;
    height: 200px;
}

.fee-card {
    background: white;
    border: 1px solid #e1e1e1;
    border-radius: 8px;
    margin-bottom: 15px;
    overflow: hidden;
    transition: box-shadow 0.2s;
}

.fee-card:hover {
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.fee-header {
    padding: 15px 20px 10px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    background: #f8f9fa;
    border-bottom: 1px solid #e1e1e1;
}

.fee-content {
    padding: 15px 20px;
}

.fee-row {
    display: flex;
    gap: 30px;
    margin-bottom: 15px;
}

.fee-row:last-child {
    margin-bottom: 0;
}

.item {
    flex: 1;
    min-width: 0;
}

.item.full-width {
    flex: 2;
}

.title {
    color: #666;
    font-size: 12px;
    font-weight: 500;
    margin: 0 0 5px 0;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

.value {
    color: #333;
    font-size: 14px;
    font-weight: 500;
    margin: 0;
    word-break: break-word;
}

.value.amount {
    color: #2b7cd4;
    font-weight: 600;
    font-size: 16px;
}

.fee-actions {
    padding: 15px 20px;
    border-top: 1px solid #e1e1e1;
    background: #fafafa;
    display: flex;
    gap: 10px;
    flex-wrap: wrap;
}

.dialog-footer {
    display: flex;
    justify-content: flex-end;
    gap: 10px;
}

.file-name {
    margin-left: 10px;
    color: #666;
    font-size: 12px;
}

@media (max-width: 1200px) {
    .popup {
        width: 50%;
    }
}

@media (max-width: 768px) {
    .popup {
        width: 100%;
    }
    
    .fee-row {
        flex-direction: column;
        gap: 15px;
    }
    
    .filters {
        flex-direction: column;
        align-items: stretch;
    }
    
    .header-actions {
        flex-direction: column;
        align-items: stretch;
    }
}
</style>