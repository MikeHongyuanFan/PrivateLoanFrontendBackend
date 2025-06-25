<script setup>
import { ref, onMounted } from 'vue'
import { CircleCheck, View, Upload, Delete, Edit } from '@element-plus/icons-vue'
import { api } from '@/api'
import { ElMessageBox, ElMessage } from 'element-plus'

const emit = defineEmits(['refresh'])

const { fees } = defineProps({
  fees: Array
})

const viewDialogVisible = ref(false)
const currentFee = ref(null)
const loading = ref({
  markPaid: false,
  delete: false,
  upload: false
})

onMounted(() => {
})

const upload = async (id, file) => {
  loading.value.upload = true
  const formData = new FormData()
  formData.append('invoice', file)
  const [err, res] = await api.patchFee(id, formData)
  if (!err) {
    ElMessage.success('Fee updated successfully')
    emit('refresh')
  } else {
    ElMessage.error('Failed to update fee')
    console.error(err)
  }
  loading.value.upload = false
}

const handleUpload = (row) => {
  const input = document.createElement('input')
  input.type = 'file'
  input.onchange = (e) => {
    const file = e.target.files[0]
    if (file) {
      row.file = file
      upload(row.id, row.file)
    }
  }
  input.click()  
}

const handleView = (row) => {
  currentFee.value = row
  viewDialogVisible.value = true
}

const handleDelete = (row) => {
  ElMessageBox.confirm(
    'Are you sure you want to delete this fee?',
    'Warning',
    {
      confirmButtonText: 'Delete',
      cancelButtonText: 'Cancel',
      type: 'warning',
    }
  ).then(async () => {
    loading.value.delete = true
    try {
      const [err, res] = await api.deleteFee(row.id)
      if (!err) {
        ElMessage.success('Fee deleted successfully')
        emit('refresh')
      } else {
        ElMessage.error('Failed to delete fee')
        console.error(err)
      }
    } catch (error) {
      ElMessage.error('An error occurred')
      console.error(error)
    } finally {
      loading.value.delete = false
    }
  }).catch(() => {
    // User cancelled the action
  })
}

const markAsPaid = async (row) => {
  loading.value.markPaid = row.id
  try {
    const [err, res] = await api.markFeePaid(row.id, {})
    if (!err) {
      ElMessage.success('Fee marked as paid')
      emit('refresh')
    } else {
      ElMessage.error('Failed to mark fee as paid')
      console.error(err)
    }
  } catch (error) {
    ElMessage.error('An error occurred')
    console.error(error)
  } finally {
    loading.value.markPaid = null
  }
}

const viewInvoice = async (fee) => {
  try {
    // Try to preview first, if that fails, download
    const [previewError, previewResponse] = await api.previewFeeInvoice(fee.id)
    
    if (!previewError && previewResponse) {
      // Create blob URL for preview
      const blob = new Blob([previewResponse], { type: 'application/pdf' })
      const url = window.URL.createObjectURL(blob)
      
      // Open in new tab
      const newWindow = window.open(url, '_blank')
      
      // Clean up blob URL after a delay
      setTimeout(() => {
        window.URL.revokeObjectURL(url)
      }, 1000)
    } else {
      // If preview fails, try download
      const [downloadError, downloadResponse] = await api.downloadFeeInvoice(fee.id)
      
      if (!downloadError && downloadResponse) {
        // Create blob URL for download
        const blob = new Blob([downloadResponse])
        const url = window.URL.createObjectURL(blob)
        
        // Create download link
        const link = document.createElement('a')
        link.href = url
        link.download = `fee_invoice_${fee.id}.pdf`
        document.body.appendChild(link)
        link.click()
        document.body.removeChild(link)
        
        // Clean up blob URL
        window.URL.revokeObjectURL(url)
      } else {
        ElMessage.error('Failed to access invoice file')
      }
    }
  } catch (error) {
    console.error('Error accessing invoice:', error)
    ElMessage.error('Failed to access invoice file')
  }
}

const formatAmount = (amount) => {
  return parseFloat(amount).toFixed(2)
}

const formatDate = (date) => {
  if (!date) return 'N/A'
  return new Date(date).toLocaleDateString()
}

const getStatusTag = (fee) => {
  if (fee.paid_date) {
    return { type: 'success', text: 'Paid' }
  }
  if (fee.due_date) {
    const today = new Date()
    const dueDate = new Date(fee.due_date)
    if (dueDate < today) {
      return { type: 'danger', text: 'Overdue' }
    }
  }
  return { type: 'warning', text: 'Pending' }
}
</script>

<template>
  <el-table :data="fees" class="table" :header-cell-style="{ background: '#f8f8f8', color: '#272727' }">
    <el-table-column type="selection" width="50" align="center" />
    <el-table-column prop="id" label="ID" width="80" />
    <el-table-column prop="fee_type_display" label="Fee Type" width="150" />
    <el-table-column label="Amount" width="120">
      <template #default="scope">
        ${{ formatAmount(scope.row.amount) }}
      </template>
    </el-table-column>
    <el-table-column label="Status" width="100">
      <template #default="scope">
        <el-tag :type="getStatusTag(scope.row).type" size="small">
          {{ getStatusTag(scope.row).text }}
        </el-tag>
      </template>
    </el-table-column>
    <el-table-column label="Due Date" width="120">
      <template #default="scope">
        {{ formatDate(scope.row.due_date) }}
      </template>
    </el-table-column>
    <el-table-column label="Paid Date" width="120">
      <template #default="scope">
        {{ formatDate(scope.row.paid_date) }}
      </template>
    </el-table-column>
    <el-table-column prop="created_by_name" label="Created By" width="120" />
    <el-table-column label="Action" width="420" align="center">
      <template #default="scope">
        <div class="action-buttons">
          <el-button class="view" :icon="View" @click="handleView(scope.row)" size="small" />
          <el-button 
            class="record" 
            :disabled="!!scope.row.paid_date" 
            @click="markAsPaid(scope.row)" 
            :loading="loading.markPaid === scope.row.id"
            size="small"
          >
            <el-icon class="icon">
              <CircleCheck />
            </el-icon>
            Mark as Paid
          </el-button>
          <el-button 
            @click="handleUpload(scope.row)" 
            :loading="loading.upload"
            size="small"
          >
            <el-icon class="icon">
              <Upload />
            </el-icon>
            Upload
          </el-button>
          <el-button 
            :disabled="!scope.row.invoice" 
            @click="viewInvoice(scope.row)" 
            size="small"
          >
            <el-icon class="icon">
              <View />
            </el-icon>
            Invoice
          </el-button>
          <el-button 
            class="delete" 
            @click="handleDelete(scope.row)" 
            :loading="loading.delete"
            size="small"
          >
            <el-icon class="icon">
              <Delete />
            </el-icon>
          </el-button>
        </div>
      </template>
    </el-table-column>
  </el-table>

  <!-- Fee Detail Dialog -->
  <el-dialog
    v-model="viewDialogVisible"
    title="Fee Details"
    width="50%"
  >
    <div v-if="currentFee" class="fee-detail">
      <el-descriptions :column="1" border>
        <el-descriptions-item label="ID">{{ currentFee.id }}</el-descriptions-item>
        <el-descriptions-item label="Fee Type">{{ currentFee.fee_type_display }}</el-descriptions-item>
        <el-descriptions-item label="Amount">${{ formatAmount(currentFee.amount) }}</el-descriptions-item>
        <el-descriptions-item label="Status">
          <el-tag :type="getStatusTag(currentFee).type">
            {{ getStatusTag(currentFee).text }}
          </el-tag>
        </el-descriptions-item>
        <el-descriptions-item label="Due Date">{{ formatDate(currentFee.due_date) }}</el-descriptions-item>
        <el-descriptions-item label="Paid Date">{{ formatDate(currentFee.paid_date) || 'Not paid yet' }}</el-descriptions-item>
        <el-descriptions-item label="Description">{{ currentFee.description || 'No description' }}</el-descriptions-item>
        <el-descriptions-item label="Created By">{{ currentFee.created_by_name }}</el-descriptions-item>
        <el-descriptions-item label="Created At">{{ formatDate(currentFee.created_at) }}</el-descriptions-item>
        <el-descriptions-item label="Updated At">{{ formatDate(currentFee.updated_at) }}</el-descriptions-item>
        <el-descriptions-item label="Invoice" v-if="currentFee.invoice">
          <el-button type="primary" size="small" @click="viewInvoice(currentFee)">
            <el-icon><View /></el-icon>
            View Invoice
          </el-button>
        </el-descriptions-item>
      </el-descriptions>
    </div>
    <template #footer>
      <span class="dialog-footer">
        <el-button @click="viewDialogVisible = false">Close</el-button>
        <el-button type="primary" v-if="currentFee && !currentFee.paid_date" @click="markAsPaid(currentFee); viewDialogVisible = false">
          Mark as Paid
        </el-button>
      </span>
    </template>
  </el-dialog>
</template>

<style lang="scss" scoped>
.table {
  height: 90%;

  .number {
    font-weight: 400;
    font-size: 12px;

    ::v-deep(.el-statistic__content) {
      font-size: 12px;
    }
  }
}

.action-buttons {
  display: flex;
  gap: 6px;
  align-items: center;
  justify-content: center;
  flex-wrap: nowrap;
  min-width: 400px;
  padding: 0 8px;

  .view {
    border: 1px solid #2984DE;
    color: #2984DE;
    min-width: 32px;
    
    &:disabled {
      border-color: #c0c4cc;
      color: #c0c4cc;
    }
  }

  .record {
    border: 1px solid #1AAD0A;
    color: #1AAD0A;
    min-width: 90px;
    
    &:disabled {
      border-color: #c0c4cc;
      color: #c0c4cc;
      background-color: #f5f7fa;
    }
  }

  .upload {
    border: 1px solid #FF9800;
    color: #FF9800;
    min-width: 70px;
    
    &:disabled {
      border-color: #c0c4cc;
      color: #c0c4cc;
    }
  }

  .delete {
    border: 1px solid #F44336;
    color: #F44336;
    min-width: 32px;
    
    &:disabled {
      border-color: #c0c4cc;
      color: #c0c4cc;
    }
  }

  .icon {
    margin-right: 4px;
  }
}

.fee-detail {
  .el-descriptions {
    margin-bottom: 20px;
  }
}

.dialog-footer {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
}
</style> 