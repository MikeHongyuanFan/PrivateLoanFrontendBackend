<script setup>
import { ref, onMounted } from 'vue'
import { CircleCheck, View, Upload, Delete } from '@element-plus/icons-vue'
import { api } from '@/api'
import { ElMessageBox, ElMessage } from 'element-plus'

const emit = defineEmits(['refresh'])

const { repayments } = defineProps({
  repayments: Array
})

const viewDialogVisible = ref(false)
const currentRepayment = ref(null)
const loading = ref({
  markPaid: false,
  delete: false,
  upload: false
})

onMounted(() => {
})

const upload = async (id, file) => {
  loading.value.upload = true
  const [err, res] = await api.updateRepayments(id, file)
  if (!err) {
    ElMessage.success('Repayment updated successfully')
    emit('refresh')
  } else {
    ElMessage.error('Failed to update repayment')
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
  currentRepayment.value = row
  viewDialogVisible.value = true
}

const handleDelete = (row) => {
  ElMessageBox.confirm(
    'Are you sure you want to delete this repayment?',
    'Warning',
    {
      confirmButtonText: 'Delete',
      cancelButtonText: 'Cancel',
      type: 'warning',
    }
  ).then(async () => {
    loading.value.delete = true
    try {
      const [err, res] = await api.deleteRepayment(row.id)
      if (!err) {
        ElMessage.success('Repayment deleted successfully')
        emit('refresh')
      } else {
        ElMessage.error('Failed to delete repayment')
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
    const [err, res] = await api.markRepaymentAsPaid(row.id)
    if (!err) {
      ElMessage.success('Repayment marked as paid')
      emit('refresh')
    } else {
      ElMessage.error('Failed to mark repayment as paid')
      console.error(err)
    }
  } catch (error) {
    ElMessage.error('An error occurred')
    console.error(error)
  } finally {
    loading.value.markPaid = null
  }
}

const viewInvoice = async (repayment) => {
  try {
    // Try to preview first, if that fails, download
    const [previewError, previewResponse] = await api.previewRepaymentInvoice(repayment.id)
    
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
      const [downloadError, downloadResponse] = await api.downloadRepaymentInvoice(repayment.id)
      
      if (!downloadError && downloadResponse) {
        // Create blob URL for download
        const blob = new Blob([downloadResponse])
        const url = window.URL.createObjectURL(blob)
        
        // Create download link
        const link = document.createElement('a')
        link.href = url
        link.download = `repayment_invoice_${repayment.id}.pdf`
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
</script>

<template>
  <el-table :data="repayments" class="table" :header-cell-style="{ background: '#f8f8f8', color: '#272727' }">
    <el-table-column type="selection" width="50" align="center" />
    <el-table-column prop="id" label="ID" />
    <el-table-column prop="application" label="Application" />
    <el-table-column prop="amount" label="Amount" />
    <el-table-column prop="status" label="Status" />
    <el-table-column prop="due_date" label="Due Date" />
    <el-table-column prop="paid_date" label="Paid Date" />
    <el-table-column prop="created_by_name" label="Created By" />
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

  <!-- Repayment Detail Dialog -->
  <el-dialog
    v-model="viewDialogVisible"
    title="Repayment Details"
    width="50%"
  >
    <div v-if="currentRepayment" class="repayment-detail">
      <el-descriptions :column="1" border>
        <el-descriptions-item label="ID">{{ currentRepayment.id }}</el-descriptions-item>
        <el-descriptions-item label="Application">{{ currentRepayment.application }}</el-descriptions-item>
        <el-descriptions-item label="Amount">{{ currentRepayment.amount }}</el-descriptions-item>
        <el-descriptions-item label="Status">{{ currentRepayment.status }}</el-descriptions-item>
        <el-descriptions-item label="Due Date">{{ currentRepayment.due_date }}</el-descriptions-item>
        <el-descriptions-item label="Paid Date">{{ currentRepayment.paid_date || 'Not paid yet' }}</el-descriptions-item>
        <el-descriptions-item label="Created By">{{ currentRepayment.created_by_name }}</el-descriptions-item>
        <el-descriptions-item label="Created At">{{ currentRepayment.created_at }}</el-descriptions-item>
        <el-descriptions-item label="Updated At">{{ currentRepayment.updated_at }}</el-descriptions-item>
        <el-descriptions-item label="Invoice" v-if="currentRepayment.invoice">
          <el-button type="primary" size="small" @click="viewInvoice(currentRepayment)">
            <el-icon><View /></el-icon>
            View Invoice
          </el-button>
        </el-descriptions-item>
      </el-descriptions>
    </div>
    <template #footer>
      <span class="dialog-footer">
        <el-button @click="viewDialogVisible = false">Close</el-button>
        <el-button type="primary" v-if="currentRepayment && !currentRepayment.paid_date" @click="markAsPaid(currentRepayment); viewDialogVisible = false">
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
    border: 1px solid #B3BFCA;
    color: #B3BFCA;
    min-width: 70px;
    
    &:disabled {
      border-color: #c0c4cc;
      color: #c0c4cc;
    }
  }

  .delete {
    border: 1px solid #F56C6C;
    color: #F56C6C;
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

.repayment-detail {
  margin: 20px 0;
}

.dialog-footer {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
}
</style>
